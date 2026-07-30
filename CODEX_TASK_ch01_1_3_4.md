# Codex Task: integrate Chapter 1, Section 1.3.4

Read and obey `AGENTS.md`, `WORKFLOW_MODES.md`, `THESIS_CONTRACT.md`, `AUTHORSHIP_PROTOCOL.md`, `AUTHOR_VOICE.md`, `STATE.md`, `PROJECT_CONFIG.md`, and `chapter_cards/ch01.md` before editing.

## Workflow mode

Use Mode A fast subsection integration. Section 1.3 completion is not yet the Chapter 1 milestone because Sections 1.4 and 1.5 remain.

Run:

```bash
bash scripts/verify_fast_section.sh --quiet chapters/ch01_introduction.tex
```

Do not run chapter-level `build_and_audit.sh`, full PDF inspection, or context-packet rebuild in this task. Those are required after the complete Chapter 1 draft, not after Section 1.3 alone.

After the verified content push:

```bash
bash scripts/sync_latex_to_overleaf.sh --skip-local-build "Sync Chapter 1 Section 1.3.4"
```

Report the deployment SHA; do not create a receipt-only commit.

## Goal

Integrate the approved draft for Section 1.3.4 “无回放联邦环境中的跨中心知识保护”.

This subsection must synthesize 1.2.3 into the fourth thesis challenge. It should explain why replay-free FCL requires more than local anti-forgetting: historical task knowledge is distributed across clients, aggregation can reduce global retention, and indiscriminate protection can over-constrain heterogeneous clients’ new-task learning.

The subsection must motivate Chapter 6 without revealing the full FedSubMerge algorithm, equations, results, or contribution list.

Stop after 1.3.4. Do not draft 1.4 or 1.5.

## Evidence basis

Reuse verified entries:

- `yang2024fclsurvey`
- `yoon2021fedweit`
- `dong2022glfc`
- `saha2021gpm`
- `rieke2020future`

No new bibliography entry is expected.

## Strict scientific boundaries

- Do not claim federated learning or the exchange of compact subspaces provides a formal privacy guarantee.
- Do not claim all hospitals prohibit replay or delete old images.
- Define replay-free here as no access to historical raw training samples during later task updates; do not imply that every compact statistic is prohibited.
- Do not equate general client heterogeneity with catastrophic forgetting. Performance loss must be tied to sequential learning or aggregation.
- Attribute Yang et al.’s “spatial catastrophic forgetting” only when discussing that survey; the thesis-preferred term is “跨客户端全局灾难性遗忘”.
- Do not claim local GPM protects tasks learned only at other clients.
- Do not assume merging every client’s protective direction is always beneficial.
- Do not present client-specific or layer-wise selection as already solved in this subsection.
- Do not introduce FedSubMerge/FedSubMerge-AD formulas, singular-value operations, experimental numbers, rankings, or contribution bullets.
- Do not modify `sources/` or import reference-thesis material.

## Strict file scope

Files that may be modified or added:

- `CODEX_TASK_ch01_1_3_4.md`
- `chapters/ch01_introduction.tex`
- `evidence/claims.csv`
- `qa/terminology.csv`
- `qa/chapter_status.csv`
- `qa/style_audit_report.md`
- `qa/reference_overlap_report.md`
- `STATE.md`
- `handoff/LATEST_CODEX_REPORT.md`

Bibliography and build flags are read-only verification targets.

## Step 0: preflight

1. Check clean `main`, remote sync, and fast-forward safety.
2. Record baseline SHA.
3. Confirm Sections 1.1, 1.2, and 1.3.1--1.3.3 are verified.
4. Confirm 1.3.4 body is empty and Sections 1.4/1.5 are body-empty.
5. Hash all content through 1.3.3 and later empty sections.
6. Confirm claims through `C1-098`, terminology/status from prior tasks, and all five citation keys.
7. Confirm `\thesisbibliographytrue`.
8. Record session-start `sources/` file count and SHA-256.

Stop if 1.3.3 is incomplete.

## Step 1: integrate approved prose exactly

Preserve:

```latex
\subsection{无回放联邦环境中的跨中心知识保护}
\label{subsec:intro-challenge-fedsubmerge}
```

Insert immediately after the label and before Section 1.4:

```latex
无回放联邦持续学习同时具有时间和机构两个维度。每个客户端按本地任务序列更新模型，可能在学习新任务时损失自身历史能力；服务器又需要把来自不同客户端的更新整合为共享模型。Yang 等将这两类现象概括为时间与空间维度的遗忘\cite{yang2024fclsurvey}。本文关注其中更具体的跨客户端全局灾难性遗忘，即聚合和后续训练使共享模型在参与机构已经学习的历史任务上发生性能下降。

客户端本地的抗遗忘机制只能利用该客户端能够访问的历史。FedWeIT 等方法通过任务特定参数和跨客户端知识选择减少任务干扰\cite{yoon2021fedweit}，GLFC 则在联邦类增量场景中使用蒸馏、原型和类别补偿保护已见类别\cite{dong2022glfc}。然而，当一个任务只在部分中心出现时，未观察该任务的客户端无法独立估计其重要参数、特征或梯度方向。仅在本地保护历史因而不能保证共享模型覆盖整个联邦中的任务知识。

无回放条件使这一缺口更加突出。这里的无回放是指后续任务训练不重新调用历史原始样本，而不是声称医疗机构必须删除全部旧影像，也不是禁止保存任何模型统计。缺少旧图像后，服务器不能通过集中重训直接恢复各中心历史分布，客户端也不能用其他机构的原始样本构造回放。跨中心知识保护需要依赖参数、输出、原型或梯度结构等紧凑信息，但不同载体保留的历史内容和通信代价并不相同。

梯度投影为无样本保护提供了可行思路。GPM 保存单一学习器旧任务的重要梯度子空间，并把新梯度投影到其正交补空间\cite{saha2021gpm}。在联邦环境中，客户端独立形成的子空间只概括本地任务历史，无法包含仅在其他中心出现的方向。因此，关键问题不是简单地把单机投影复制到每个客户端，而是如何在服务器端形成能够代表跨客户端历史的保护信息，并将其用于后续本地更新。

全局保护也不能等同于无差别叠加所有历史方向。不同中心在标签构成、设备、采集条件和任务顺序上存在差异，同一保护方向对不同客户端及不同网络层的重要性可能不同。若所有客户端被要求避开全部历史子空间，可行更新空间会随任务累积而收缩，当前任务学习受到过强限制；若保护范围过窄，又会遗漏其他中心的历史知识。跨中心保护因此同时包含全局覆盖与客户端可塑性两个目标。

服务器需要处理的保护信息还受到通信和信任边界约束。传输完整梯度或参数可能带来较高通信成本，并可能包含与本地数据相关的信息\cite{rieke2020future,yang2024fclsurvey}。即使只交换低秩基、原型或其他压缩摘要，也只能说明原始数据未被直接传输，不能据此宣称形式化隐私保证。方法设计需要明确共享对象、更新频率、服务器能力和附加保护机制。

由此，无回放联邦持续医学影像学习需要解决三项相互关联的挑战：以紧凑形式汇集分散于不同客户端的历史任务信息，构建能够降低跨客户端全局遗忘的共享保护，并依据客户端和网络层差异避免统一保护造成过度约束。该问题要求在全局稳定性、本地可塑性、通信代价和信息暴露边界之间进行协调，构成第六章研究的核心出发点。
```

Verify:

- all prose through 1.3.3 is byte-for-byte unchanged;
- 1.3.4 title/label unique;
- Sections 1.4 and 1.5 remain body-empty;
- only five approved keys appear;
- Yang et al.’s terminology is attributed;
- replay-free and privacy boundaries are explicit;
- no FedSubMerge implementation or result is disclosed.

## Step 2: bibliography verification

Do not add entries. Verify all keys resolve, no duplicates exist, and the bibliography flag remains true.

## Step 3: append evidence records

```csv
C1-099,1,1.3.4,联邦持续学习同时面临客户端顺序学习和服务器跨客户端融合中的知识损失,DOI:10.1109/TKDE.2024.3363240,Problem definition and framework,yang2024fclsurvey,literature,confirmed,drafted,本文使用更具体的跨客户端全局灾难性遗忘表述
C1-100,1,1.3.4,只利用客户端本地历史的保护机制不能直接覆盖仅在其他客户端出现的任务知识,primary FCL methods and author synthesis,Section challenge analysis,yoon2021fedweit;dong2022glfc,author_analysis,confirmed,drafted,用于区分本地遗忘与全局知识保护
C1-101,1,1.3.4,本文无回放设定指后续任务不重新调用历史原始样本而非禁止所有压缩统计,author scope definition,Section definition,yang2024fclsurvey;saha2021gpm,author_definition,confirmed,drafted,不作机构删除义务或形式化隐私断言
C1-102,1,1.3.4,GPM保存单一学习器的旧任务重要梯度子空间并在正交补中更新,primary paper,Method formulation,saha2021gpm,method,confirmed,drafted,原始方法未覆盖跨客户端历史融合
C1-103,1,1.3.4,联邦无回放保护需要在服务器端形成代表跨客户端任务历史的紧凑信息,author synthesis based on FCL and GPM,Section challenge analysis,yang2024fclsurvey;saha2021gpm,author_analysis,confirmed,drafted,不提前指定FedSubMerge实现
C1-104,1,1.3.4,无差别保护全部客户端历史方向可能收缩可行更新空间并降低当前任务可塑性,author analysis based on gradient-subspace constraints,Section challenge analysis,saha2021gpm,author_analysis,confirmed,drafted,采用条件性机制分析
C1-105,1,1.3.4,跨中心保护需考虑不同客户端和网络层对历史方向的相关性差异,author synthesis based on client heterogeneity,Section challenge synthesis,yang2024fclsurvey,author_analysis,confirmed,drafted,用于提出客户端特定保护需求而不提前给出算法
C1-106,1,1.3.4,交换参数梯度原型或压缩子空间不自动构成形式化隐私保证,DOI:10.1038/s41746-020-00323-1;DOI:10.1109/TKDE.2024.3363240,Security and privacy discussion,rieke2020future;yang2024fclsurvey,literature,confirmed,drafted,仅描述原始数据未直接传输
C1-107,1,1.3.4,无回放医学FCL需协调跨客户端全局稳定性本地可塑性通信代价和信息暴露边界,author synthesis based on section sources,Section synthesis,yang2024fclsurvey;yoon2021fedweit;dong2022glfc;saha2021gpm;rieke2020future,author_analysis,confirmed,drafted,用于形成第六章问题入口
```

Validate 11 columns, unique IDs `C1-099`--`C1-107`, unchanged prior rows, and valid citation keys.

## Step 4: terminology and status

### Add terminology rows

```csv
local-history protection,本地历史知识保护,第一章与第六章,本地知识保护（范围更宽）,仅基于单个客户端已观察任务形成的保护
cross-client history,跨客户端历史知识,第一章与第六章,全局历史（可能包含服务器历史）,分散在不同客户端任务序列中的既有知识
global protective subspace,全局保护子空间,第一章与第六章,共享子空间（用途不明确）,用于约束后续更新以保护跨客户端历史的梯度子空间
over-constraint,过度约束,第一章与第六章,过保护（避免混用）,保护条件过强导致当前任务可行更新空间过度收缩
layer-wise relatedness,逐层相关性,第一章与第六章,层相关性（避免混用）,客户端历史子空间在不同网络层上的相关程度
subspace distance,子空间距离,第一章与第六章,空间距离（避免混用）,衡量两个线性子空间关系的距离量
compact gradient summary,紧凑梯度摘要,第一章与第六章,梯度压缩（机制不同）,由低秩基或相关统计概括历史梯度方向的信息
```

Validate 5 columns and unique keys.

### Status

Set:

- `1.3` → `drafted_and_verified`, artifact `chapters/ch01_introduction.tex`
- `1.3.1`--`1.3.4` → `drafted_and_verified`
- `1.4` → `queued`
- preserve `1.5` as `not_started`

Update concise `STATE.md`:

- Sections 1.1, 1.2, and 1.3 are complete at the current draft stage;
- all four 1.3 subsections are verified;
- next target is 1.4 “本文主要研究内容与创新点”;
- Sections 1.4 and 1.5 remain undrafted;
- fast verification result and unresolved warnings;
- `sources/` unchanged.

Do not rebuild the GPT context packet; Chapter 1 is not yet complete.

## Step 5: fast verification

Run the quiet fast-section script and verify citation/reference/label/file/placeholder/BibTeX/CSV/hash/diff/source integrity. Confirm no new warning. No routine PDF inspection unless an anomaly requires targeted inspection.

## Step 6: concise report

Update `handoff/LATEST_CODEX_REPORT.md` in the content commit with:

- task and baseline;
- exact integration;
- prior hash preservation;
- no-new-bibliography result;
- evidence/terminology/status changes;
- fast verification;
- privacy/replay/terminology boundary confirmations;
- `sources/` unchanged;
- unresolved issues;
- Section 1.3 completion;
- next target 1.4;
- confirmation that 1.4/1.5 remain undrafted.

Do not create a deployment-receipt commit.

## Step 7: commit and sync

Create one content commit, for example:

```bash
git commit -m "Draft Chapter 1 Section 1.3.4"
git push origin main
```

After remote verification:

```bash
bash scripts/sync_latex_to_overleaf.sh --skip-local-build "Sync Chapter 1 Section 1.3.4"
```

Report GitHub and Overleaf SHAs in the terminal. No force-push; no second receipt-only commit; final worktree clean and local `HEAD == origin/main`.

## Definition of done

- exact 1.3.4 integration;
- prior prose unchanged;
- 1.4/1.5 body-empty;
- no new bibliography entry;
- `C1-099`--`C1-107` unique;
- terminology/status valid;
- Section 1.3 marked complete;
- fast verification passes;
- privacy and replay boundaries preserved;
- `sources/` unchanged;
- GitHub/Overleaf synchronized or exact failure reported;
- clean worktree;
- next target 1.4;
- no 1.4 prose drafted.

Do not continue beyond Section 1.3.4.
