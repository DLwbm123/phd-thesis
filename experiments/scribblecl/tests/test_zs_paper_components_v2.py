import numpy as np
import torch

from scribblecl.losses import soft_partial_cross_entropy
from scribblecl.protocol import IGNORE_INDEX
from scribblecl.zs_components import (
    LAMBDA_GLOBAL,
    OCCLUSION_SIZE,
    PUZZLEMIX_CONFIG,
    SPATIAL_WARMUP_EPOCH,
    active_probabilities,
    apply_occlusion,
    apply_shared_geometry,
    classwise_shape_loss,
    classwise_largest_component_labels,
    em_ratios,
    puzzlemix_native,
    spatial_prior_loss,
    spatial_enabled,
    symmetric_global_consistency,
)


def test_paper_constants_and_warmup_are_locked():
    assert LAMBDA_GLOBAL == 0.05
    assert OCCLUSION_SIZE == 32
    assert SPATIAL_WARMUP_EPOCH == 15
    assert not spatial_enabled(14)
    assert spatial_enabled(15)
    assert PUZZLEMIX_CONFIG == {
        "transport": True,
        "graph": True,
        "box": False,
        "mixup_alpha": 0.5,
        "neigh_size": 4,
        "n_labels": 3,
        "beta": 1.2,
        "gamma": 0.5,
        "eta": 0.2,
        "t_eps": 0.8,
        "t_size": 4,
        "adv_p": 0.0,
    }


def test_future_logits_cannot_enter_active_probabilities():
    logits = torch.randn(2, 8, 8, 8)
    changed = logits.clone()
    changed[:, 4:] = torch.randn_like(changed[:, 4:]) * 1_000
    left = active_probabilities(logits, (0, 1, 2, 3))
    right = active_probabilities(changed, (0, 1, 2, 3))
    assert torch.equal(left, right)


def test_shared_geometry_is_deterministic_and_paired():
    image = torch.zeros(2, 1, 32, 32)
    sparse = torch.full((2, 32, 32), IGNORE_INDEX, dtype=torch.long)
    image[:, :, 8:12, 9:14] = 1
    sparse[:, 8:12, 9:14] = 1
    first = apply_shared_geometry(image, sparse, seed=42000)
    second = apply_shared_geometry(image, sparse, seed=42000)
    assert torch.equal(first[0], second[0])
    assert torch.equal(first[1], second[1])
    assert first[2] == second[2]
    assert torch.equal(first[0][:, 0].gt(0), first[1].eq(1))


def test_occlusion_sets_image_hole_and_target_to_background():
    image = torch.ones(2, 1, 64, 64)
    target = torch.zeros(2, 5, 64, 64)
    target[:, -1] = 1
    occluded, target_out, keep, boxes = apply_occlusion(image, target, seed=42)
    assert len(boxes) == 2
    assert int(keep.eq(0).sum()) == 2 * 32 * 32
    assert torch.equal(occluded, image * keep)
    assert torch.equal(target_out.sum(1), torch.ones_like(target_out[:, 0]))
    hole = keep[:, 0].eq(0)
    assert target_out[:, 0][hole].eq(1).all()
    assert target_out[:, 1:][hole.unsqueeze(1).expand_as(target_out[:, 1:])].eq(0).all()


def test_occlusion_ignore_is_explicit_diagnostic_semantics():
    image = torch.ones(1, 1, 64, 64)
    target = torch.zeros(1, 5, 64, 64)
    target[:, 1] = 1
    _, target_out, keep, _ = apply_occlusion(image, target, seed=1, mode="ignore")
    hole = keep[:, 0].eq(0)
    assert target_out[:, -1][hole].eq(1).all()
    assert target_out[:, :-1][hole.unsqueeze(1).expand_as(target_out[:, :-1])].eq(0).all()


def _formal_occlusion_output():
    image = torch.ones(1, 1, 64, 64)
    target = torch.zeros(1, 5, 64, 64)
    target[:, -1] = 1
    return apply_occlusion(image, target, seed=42)


def test_occlusion_background_sets_bg_channel():
    _, target, keep, _ = _formal_occlusion_output()
    assert target[:, 0][keep[:, 0].eq(0)].eq(1).all()


def test_occlusion_target_is_onehot():
    _, target, _, _ = _formal_occlusion_output()
    assert torch.equal(target.sum(1), torch.ones_like(target[:, 0]))


def test_occlusion_does_not_create_unknown_inside_hole():
    _, target, keep, _ = _formal_occlusion_output()
    assert target[:, -1][keep[:, 0].eq(0)].eq(0).all()


def test_occlusion_mask_size_is_32():
    _, _, keep, _ = _formal_occlusion_output()
    assert int(keep.eq(0).sum()) == 32 * 32


def test_soft_pce_ignores_unknown_and_has_finite_gradients():
    logits = torch.randn(1, 4, 4, 4, requires_grad=True)
    probabilities = torch.softmax(logits, 1)
    target = torch.zeros(1, 5, 4, 4)
    target[:, -1] = 1
    target[:, -1, 0, 0] = 0
    target[:, 2, 0, 0] = 1
    loss = soft_partial_cross_entropy(probabilities, target)
    assert torch.allclose(loss, -torch.log(probabilities[0, 2, 0, 0]))
    loss.backward()
    assert torch.isfinite(logits.grad).all()


def test_global_consistency_is_symmetric_negative_cosine():
    tensors = [torch.randn(2, 3, 4, 4) for _ in range(4)]
    u12, v12, u21, v21 = tensors
    expected = -0.5 * (
        torch.nn.functional.cosine_similarity(u12.flatten(1), v12.flatten(1)).mean()
        + torch.nn.functional.cosine_similarity(u21.flatten(1), v21.flatten(1)).mean()
    )
    actual = symmetric_global_consistency(u12, v12, u21, v21)
    assert torch.allclose(actual, expected)
    assert torch.allclose(actual, symmetric_global_consistency(u21, v21, u12, v12))


def test_global_consistency_is_symmetric():
    test_global_consistency_is_symmetric_negative_cosine()


def test_swapping_pair_order_preserves_loss():
    values = [torch.randn(2, 3, 4, 4) for _ in range(4)]
    assert torch.allclose(
        symmetric_global_consistency(*values),
        symmetric_global_consistency(values[2], values[3], values[0], values[1]),
    )


def test_global_consistency_weight_is_0_05():
    assert LAMBDA_GLOBAL == 0.05


def test_global_consistency_gradient_is_finite():
    source = torch.randn(2, 3, 4, 4, requires_grad=True)
    loss = symmetric_global_consistency(source, torch.randn_like(source), source, torch.randn_like(source))
    loss.backward()
    assert torch.isfinite(source.grad).all()


def test_em_uses_unlabeled_predictions_and_zeroes_absent_classes():
    sparse = torch.tensor([[[0, 1], [IGNORE_INDEX, IGNORE_INDEX]]])
    first = torch.tensor(
        [[[[0.5, 0.5], [0.9, 0.9]], [[0.5, 0.5], [0.1, 0.1]], [[0, 0], [0, 0]]]],
        dtype=torch.float32,
    )
    second = first.clone()
    second[:, 0, 1] = 0.1
    second[:, 1, 1] = 0.9
    first_ratio = em_ratios(first, sparse, (0, 1, 2))
    second_ratio = em_ratios(second, sparse, (0, 1, 2))
    assert first_ratio[0] > second_ratio[0]
    assert first_ratio[2] == 0 and second_ratio[2] == 0
    assert torch.allclose(first_ratio.sum(), torch.tensor(1.0))
    assert torch.allclose(second_ratio.sum(), torch.tensor(1.0))


def test_em_uses_unlabeled_predictions():
    test_em_uses_unlabeled_predictions_and_zeroes_absent_classes()


def test_em_no_unlabeled_is_safe():
    test_em_no_unlabeled_is_labeled_frequency_and_safe()


def test_em_no_unlabeled_is_labeled_frequency_and_safe():
    sparse = torch.tensor([[[0, 0], [1, 2]]])
    probs = torch.full((1, 3, 2, 2), 1 / 3)
    ratio = em_ratios(probs, sparse, (0, 1, 2))
    assert torch.allclose(ratio, torch.tensor([0.5, 0.25, 0.25]))


def test_em_absent_class_ratio_is_zero():
    sparse = torch.tensor([[[0, 1], [2, IGNORE_INDEX]]])
    probabilities = torch.full((1, 4, 2, 2), 0.25)
    ratio = em_ratios(probabilities, sparse, (0, 1, 2, 3))
    assert ratio[3] == 0


def test_em_present_priors_sum_to_one():
    sparse = torch.tensor([[[0, 1], [2, IGNORE_INDEX]]])
    probabilities = torch.full((1, 4, 2, 2), 0.25)
    ratio = em_ratios(probabilities, sparse, (0, 1, 2, 3))
    assert torch.allclose(ratio[:3].sum(), torch.tensor(1.0))


def test_em_hand_computed_two_class():
    sparse = torch.tensor([[[0, 1], [IGNORE_INDEX, IGNORE_INDEX]]])
    probabilities = torch.tensor(
        [[[[0.5, 0.5], [0.8, 0.8]], [[0.5, 0.5], [0.2, 0.2]]]]
    )
    ratio = em_ratios(probabilities, sparse, (0, 1), iterations=1, tol=0)
    assert torch.allclose(ratio, torch.tensor([0.8, 0.2]))


def test_shape_filter_is_classwise_not_union():
    prediction = np.zeros((8, 8), dtype=np.int64)
    prediction[1:4, 1:4] = 1
    prediction[7, 7] = 1
    prediction[4:6, 4:6] = 2
    prediction[0, 7] = 2
    prediction[6, 0] = 3
    filtered = classwise_largest_component_labels(prediction, (1, 2))
    assert filtered[7, 7] == 0
    assert filtered[0, 7] == 0
    assert filtered[6, 0] == 3
    assert (filtered == 1).sum() == 9
    assert (filtered == 2).sum() == 4


def test_shape_does_not_delete_disconnected_other_class():
    prediction = np.zeros((8, 8), dtype=np.int64)
    prediction[1:4, 1:4] = 1
    prediction[7, 7] = 1
    prediction[0, 0] = 2
    prediction[7, 0] = 2
    filtered = classwise_largest_component_labels(prediction, (1,))
    assert filtered[7, 7] == 0
    assert filtered[0, 0] == 2 and filtered[7, 0] == 2


def test_shape_only_applies_to_eligible_classes():
    probabilities = torch.zeros(1, 4, 8, 8)
    probabilities[:, 0] = 0.01
    probabilities[:, 2, 0, 0] = 1
    probabilities[:, 2, 7, 7] = 1
    probabilities[:, 1, 2:5, 2:5] = 1
    probabilities = (probabilities + 1e-3) / (probabilities + 1e-3).sum(1, keepdim=True)
    sparse = torch.full((1, 8, 8), IGNORE_INDEX)
    result = classwise_shape_loss(probabilities, sparse, (1,))
    assert result["valid_pixel_count"] == 9


def test_shape_empty_prediction_is_safe():
    probabilities = torch.zeros(1, 4, 8, 8, requires_grad=True)
    normalized = torch.softmax(probabilities, 1)
    sparse = torch.full((1, 8, 8), IGNORE_INDEX)
    result = classwise_shape_loss(normalized, sparse, (1, 2, 3))
    assert result["valid_pixel_count"] == 0
    assert result["loss"] == 0
    result["loss"].backward()
    assert torch.isfinite(probabilities.grad).all()


def test_shape_removed_component_is_excluded_by_equation_9_mask():
    probabilities = torch.full((1, 4, 4, 4), 0.01)
    probabilities[:, 0] = 0.09
    probabilities[:, 1, 0:2, 0:2] = 0.90
    probabilities[:, 1, 3, 3] = 0.80
    probabilities[:, 0, 3, 3] = 0.19
    probabilities = probabilities / probabilities.sum(1, keepdim=True)
    sparse = torch.full((1, 4, 4), IGNORE_INDEX)
    result = classwise_shape_loss(probabilities, sparse, (1,))
    kept = -torch.log(probabilities[0, 1, 0:2, 0:2]).sum()
    assert result["valid_pixel_count"] == 4
    assert torch.allclose(result["loss"], kept / 4)


def test_shape_gt_oracle_retention():
    prediction = np.zeros((8, 8), dtype=np.int64)
    prediction[1:4, 1:4] = 1
    prediction[7, 7] = 1
    filtered = classwise_largest_component_labels(prediction, (1,))
    assert (filtered == 1).sum() / (prediction == 1).sum() == 0.9


def test_spatial_loss_matches_registered_normalization(monkeypatch):
    class FakeSpatial:
        def __call__(self, probabilities, *_args, **_kwargs):
            return torch.zeros_like(probabilities)

    monkeypatch.setattr(
        "scribblecl.vendor.zscribble.spatial_function.ModelWeightGatedCRF",
        FakeSpatial,
    )
    probabilities = torch.tensor(
        [[[[1.0, 0.8], [0.7, 0.6]], [[0.0, 0.2], [0.3, 0.4]]]],
        requires_grad=True,
    )
    sparse = torch.tensor([[[0, IGNORE_INDEX], [IGNORE_INDEX, IGNORE_INDEX]]])
    image = torch.zeros(1, 1, 2, 2)
    result = spatial_prior_loss(probabilities, image, sparse, (0, 1))
    expected = -(torch.log(torch.tensor(0.8)) + torch.log(torch.tensor(0.7)) + torch.log(torch.tensor(0.6))) / 4
    assert result["normalization"] == "full_image"
    assert torch.allclose(result["loss"], expected)


def test_spatial_loss_disabled_before_epoch_15():
    assert not spatial_enabled(14)


def test_spatial_loss_enabled_at_epoch_15():
    assert spatial_enabled(15)


def test_puzzlemix_passes_checkpoint_args_on_native_grid(monkeypatch):
    captured = {}

    def fake_mixup(out, target, args, grad, noise):
        captured.update(vars(args))
        captured["noise"] = noise
        captured["shape"] = tuple(out.shape[-2:])
        indices = np.arange(out.shape[0])[::-1].copy()
        mask = torch.full_like(out[:, :1], 0.5)
        mixed = out * mask + out[indices] * (1 - mask)
        mixed_target = target * mask + target[indices] * (1 - mask)
        reverse = out[indices] * mask + out * (1 - mask)
        return mixed, mixed_target, indices, mask, reverse

    monkeypatch.setattr(
        "scribblecl.vendor.zscribble.mixup.mixup_process", fake_mixup
    )
    model = torch.nn.Conv2d(1, 4, 1)
    image = torch.rand(2, 1, 256, 256)
    sparse = torch.full((2, 256, 256), IGNORE_INDEX, dtype=torch.long)
    sparse[:, 0, :16] = 0
    sparse[:, 1, :16] = 1
    result = puzzlemix_native(model, image, sparse, (0, 1, 2, 3), seed=42)
    assert captured["shape"] == (256, 256)
    assert captured["transport"] is True
    assert captured["graph"] is True
    assert captured["box"] is False
    assert captured["noise"] is None
    assert captured["t_eps"] == 0.8
    assert captured["t_size"] == 4
    assert result["native_shape"] == (256, 256)
    assert result["adversarial_noise_enabled"] is False
    assert torch.allclose(result["mixed_target"].sum(1), torch.ones(2, 256, 256))


def test_puzzlemix_uses_native_256_grid(monkeypatch):
    test_puzzlemix_passes_checkpoint_args_on_native_grid(monkeypatch)


def test_no_extra_padding_for_mmwhs(monkeypatch):
    test_puzzlemix_passes_checkpoint_args_on_native_grid(monkeypatch)


def test_puzzlemix_target_channels_sum_to_one(monkeypatch):
    test_puzzlemix_passes_checkpoint_args_on_native_grid(monkeypatch)


def test_puzzlemix_unknown_channel_preserved(monkeypatch):
    captured = {}

    def fake_mixup(out, target, args, grad, noise):
        captured["target"] = target.detach().clone()
        indices = np.arange(out.shape[0])
        mask = torch.ones_like(out[:, :1])
        return out, target, indices, mask, out

    monkeypatch.setattr("scribblecl.vendor.zscribble.mixup.mixup_process", fake_mixup)
    model = torch.nn.Conv2d(1, 4, 1)
    image = torch.rand(2, 1, 256, 256)
    sparse = torch.full((2, 256, 256), IGNORE_INDEX, dtype=torch.long)
    sparse[:, 0, :8] = 0
    puzzlemix_native(model, image, sparse, (0, 1, 2, 3), seed=42)
    assert captured["target"][:, -1, 1:, :].eq(1).all()


def test_puzzlemix_is_deterministic_under_seed(monkeypatch):
    def fake_mixup(out, target, args, grad, noise):
        value = float(np.random.random())
        indices = np.arange(out.shape[0])[::-1].copy()
        mask = torch.full_like(out[:, :1], value)
        return (
            out * mask + out[indices] * (1 - mask),
            target * mask + target[indices] * (1 - mask),
            indices,
            mask,
            out[indices] * mask + out * (1 - mask),
        )

    monkeypatch.setattr("scribblecl.vendor.zscribble.mixup.mixup_process", fake_mixup)
    model = torch.nn.Conv2d(1, 4, 1)
    image = torch.rand(2, 1, 256, 256)
    sparse = torch.full((2, 256, 256), IGNORE_INDEX, dtype=torch.long)
    sparse[:, 0, :8] = 0
    first = puzzlemix_native(model, image, sparse, (0, 1, 2, 3), seed=9)
    second = puzzlemix_native(model, image, sparse, (0, 1, 2, 3), seed=9)
    assert torch.equal(first["mask"], second["mask"])


def test_puzzlemix_rejects_legacy_padded_shape():
    model = torch.nn.Conv2d(1, 4, 1)
    image = torch.rand(2, 1, 300, 300)
    sparse = torch.full((2, 300, 300), IGNORE_INDEX, dtype=torch.long)
    try:
        puzzlemix_native(model, image, sparse, (0, 1, 2, 3), seed=1)
    except ValueError as error:
        assert "native 256x256" in str(error)
    else:
        raise AssertionError("legacy padded grid was accepted")


def test_transport_chunking_matches_released_batched_math():
    from scribblecl.vendor.zscribble.mixup import mask_transport, transport_image

    torch.manual_seed(4)
    batch, block_number, block_size = 2, 2, 2
    image = torch.rand(batch, 1, block_number * block_size, block_number * block_size)
    mask = torch.rand(batch, 1, block_number, block_number)
    gradient = torch.rand(batch, block_number, block_number)
    target = torch.rand(batch, block_number, block_number)
    batched_plan = mask_transport(mask, gradient, target, "cpu", eps=0.8)
    batched = transport_image(
        image, batched_plan, batch, block_number, block_size
    )
    chunked = []
    for index in range(batch):
        plan = mask_transport(
            mask[index : index + 1],
            gradient[index : index + 1],
            target[index : index + 1],
            "cpu",
            eps=0.8,
        )
        chunked.append(
            transport_image(
                image[index : index + 1], plan, 1, block_number, block_size
            )
        )
    assert torch.equal(batched, torch.cat(chunked))
