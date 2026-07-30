# Codex Task: integrate Chapter 1, Section 1.3.3

Read and obey `AGENTS.md`, `WORKFLOW_MODES.md`, `THESIS_CONTRACT.md`, `AUTHORSHIP_PROTOCOL.md`, `AUTHOR_VOICE.md`, `STATE.md`, `PROJECT_CONFIG.md`, and `chapter_cards/ch01.md` before editing.

## Workflow mode

Use Mode A fast subsection integration.

Run:

```bash
bash scripts/verify_fast_section.sh --quiet chapters/ch01_introduction.tex
```

Do not duplicate routine full audits or pure-text PDF inspection. After the verified content push, use:

```bash
bash scripts/sync_latex_to_overleaf.sh --skip-local-build "Sync Chapter 1 Section 1.3.3"
```

Report the deployment SHA without creating a second receipt-only commit.

## Goal

Integrate the approved draft for Section 1.3.3 “顺序任务中的知识保持与跨任务泛化”.

This subsection must identify the coupled challenge addressed by Chapter 5: a continual medical image registration model must preserve performance on learned registration tasks, acquire a new task under limited replay, and form representations or initialization that generalize across tasks, including tasks not used in continual optimization.

It must not present SAMCL’s full method, formulas, experiments, or contributions.

Stop after 1.3.3. Do not draft 1.3.4, 1.4, or 1.5.

## Evidence basis

Reuse verified entries:

- `delange2022continual`
- `hadsell2020embracing`
- `wang2024continualsurvey`
- `wang2024samcl`

No new bibliography entry is expected.

## Strict scientific boundaries

- Do not classify medical image registration mechanically as class-incremental learning.
- Do not treat image-registration output as a discrete disease class.
- Do not claim that limited replay fully reconstructs historical distributions.
- Do not claim that replay is universally permitted or prohibited in medicine.
- Do not reduce continual registration to old-task retention.
- Do not use forward transfer and cross-task/forward generalization as synonyms.
- Do not claim that loss-landscape flatness alone guarantees universal registration.
- Do not introduce SAMCL formulas, algorithm boxes, hyperparameters, datasets, quantitative results, or superiority claims.
- Do not present the future/unknown-task generalization objective as clinical deployment.
- Do not modify `sources/` or import reference-thesis content.

## Strict file scope

Files that may be modified or added:

- `CODEX_TASK_ch01_1_3_3.md`
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

1. Check clean worktree, `main`, and `origin/main` with `git status --short`, `git branch --show-current`, and `git fetch origin`.
2. Fast-forward only; stop on divergence or unrelated changes.
3. Record baseline SHA.
4. Confirm Sections 1.1, 1.2, 1.3.1, and 1.3.2 are complete and unchanged.
5. Confirm the 1.3.3 body is empty; 1.3.4, 1.4, and 1.5 are body-empty.
6. Hash all content through 1.3.2 and the later empty bodies.
7. Confirm claims through `C1-090`, preceding terminology/status updates, and all four citation keys.
8. Confirm `\thesisbibliographytrue`.
9. Record session-start `sources/` file count and SHA-256.

Stop if 1.3.2 is incomplete.

## Step 1: integrate approved prose exactly

Preserve:

```latex
\subsection{顺序任务中的知识保持与跨任务泛化}
\label{subsec:intro-challenge-samcl}
```

Insert before 1.3.4:

```latex
医学图像配准的持续学习问题不同于类别逐步扩展。配准模型接收固定图像和移动图像，并输出描述空间对应关系的形变场；任务变化可以来自解剖区域、模态组合、扫描条件或数据来源，而不一定改变离散标签集合\cite{wang2024samcl}。当这些配准任务顺序到达时，模型需要在更新共享参数的同时保持先前建立的空间匹配能力。

有限经验回放为历史知识提供了直接参照，但只能利用受限样本近似旧任务分布。三维医学图像的输入空间和形变模式具有较高复杂性，少量回放图像难以覆盖旧任务中的全部解剖差异和配准难例。回放样本的选择、各任务所占比例及其与当前任务的相似性都会影响保护效果\cite{delange2022continual,wang2024continualsurvey}。因此，有限回放能够缓解历史信息完全缺失，却不能把顺序训练转化为完整联合训练。

知识保持与当前任务学习之间还存在直接张力。较强的参数或函数约束可以降低旧任务性能变化，但也会限制模型调整至新的图像分布和形变关系；只依据当前任务自由更新则可能破坏旧任务表示。这一稳定性—可塑性权衡是持续学习的基本困难\cite{hadsell2020embracing,delange2022continual}。对于任务差异较大的配准序列，统一的保护强度尤其难以同时适配所有阶段。

持续配准还要求超越已见任务上的平均性能。不同器官和模态之间既存在共享的空间匹配规律，也包含任务特定的外观与形变特征。若模型只记忆已见任务的局部最优解，即使遗忘较小，也未必能够快速适应新的配准对象。跨任务泛化关注已有任务学习是否形成了对未参与持续优化的任务仍有用的表示和初始化，这与仅衡量后续训练速度的前向迁移不同\cite{wang2024samcl}。

元学习为跨任务适应提供了问题视角：模型需要从多个已见任务中学习一个能够经过少量更新适配新任务的初始化。然而，在持续环境中，元目标本身也会受任务顺序和有限回放影响；若内外层更新过度偏向近期任务，获得的初始化仍可能失去历史任务信息。因而，元持续学习需要同时控制任务内适应、任务间知识积累和历史任务保持，而不能只把多个任务依次放入普通元学习流程。

优化解的局部几何也会影响跨任务鲁棒性。Wang 等指出，较平坦的损失区域通常对参数扰动和任务分布差异更不敏感\cite{wang2024continualsurvey}；SAMCL 据此把锐度感知优化引入元持续配准\cite{wang2024samcl}。但平坦性不是独立目标：若优化忽略当前任务精度、旧任务约束或任务间差异，仅追求局部平坦也不能保证有效泛化。关键在于使优化景观、元初始化和有限回放共同服务于稳定性、可塑性与跨任务泛化。

由此，顺序医学图像配准需要联合解决三项挑战：在有限回放下保存已见任务的配准能力，在当前任务上保持充分可塑性，并形成可迁移至未见配准任务的初始化。三者共享同一组模型参数和优化过程，不能通过彼此独立的目标简单叠加。这构成第五章所研究的核心问题。
```

Verify prior hashes, unique title/label, empty later sections, exactly four approved citation keys, and absence of method formulas/results.

## Step 2: bibliography verification

Do not add entries. Verify all four keys, `.bbl` resolution, duplicate status, and active bibliography flag.

## Step 3: append evidence records

```csv
C1-091,1,1.3.3,持续医学图像配准任务由图像域解剖对象模态组合和空间映射共同定义而非离散类别扩展,DOI:10.1007/978-3-031-72069-7_69,Problem setting and task construction,wang2024samcl,author_synthesis,confirmed,drafted,用于限制类增量术语的机械套用
C1-092,1,1.3.3,有限经验回放只能以受限样本近似旧任务分布而不等同完整联合训练,DOI:10.1109/TPAMI.2021.3057446;DOI:10.1109/TPAMI.2024.3367329,Replay taxonomy and resource analysis,delange2022continual;wang2024continualsurvey,author_synthesis,confirmed,drafted,不作法律或机构政策的一般断言
C1-093,1,1.3.3,过强历史保护可能限制当前配准任务学习而自由更新可能破坏旧任务能力,DOI:10.1016/j.tics.2020.09.004;DOI:10.1109/TPAMI.2021.3057446,Stability-plasticity discussion,hadsell2020embracing;delange2022continual,literature,confirmed,drafted,用于界定稳定性可塑性张力
C1-094,1,1.3.3,配准任务差异会改变共享参数更新中的任务干扰和知识迁移关系,DOI:10.1109/TPAMI.2024.3367329,Inter-task generalizability analysis,wang2024continualsurvey,author_analysis,confirmed,drafted,不声称任务相似性影响方向始终一致
C1-095,1,1.3.3,跨任务泛化关注模型在未参与持续优化的配准任务上的直接适应基础,DOI:10.1007/978-3-031-72069-7_69,Abstract motivation and evaluation scope,wang2024samcl,author_definition,confirmed,drafted,与前向迁移术语区分
C1-096,1,1.3.3,元持续学习需要在任务内适应任务间积累和历史保持之间协调更新,DOI:10.1007/978-3-031-72069-7_69,Method motivation,wang2024samcl,author_analysis,confirmed,drafted,不提前写入具体内外层公式
C1-097,1,1.3.3,较平坦损失区域通常对参数扰动和任务分布差异更不敏感但平坦性本身不保证全部目标,DOI:10.1109/TPAMI.2024.3367329;DOI:10.1007/978-3-031-72069-7_69,Generalizability analysis and SAMCL motivation,wang2024continualsurvey;wang2024samcl,author_synthesis,confirmed,drafted,采用审慎表述
C1-098,1,1.3.3,持续配准需联合优化有限回放知识保持当前任务可塑性和未见任务跨任务泛化,author synthesis based on section sources,Section synthesis,delange2022continual;wang2024continualsurvey;wang2024samcl,author_analysis,confirmed,drafted,用于形成第五章问题入口
```

Validate 11 columns, IDs `C1-091`--`C1-098`, unchanged prior rows, and valid keys.

## Step 4: terminology and status

### Add terminology rows

```csv
registration task sequence,配准任务序列,第一章与第五章,配准数据序列（范围不完全等同）,按解剖模态数据源或映射目标顺序组织的配准任务
task interference,任务干扰,第一章与第四至六章,任务冲突（可作机制解释）,不同任务更新在共享参数或表示上产生的不利相互作用
cross-task generalization,跨任务泛化,第一章与第五章,跨域泛化（范围不同）,已见任务学习形成对未参与持续优化任务的适应能力
meta-initialization,元初始化,第一章与第五章,元模型（不完全等同）,通过元学习获得并可经少量更新适应新任务的初始参数
loss-landscape flatness,损失景观平坦性,第一章与第五章,平坦最小值（仅指具体解时使用）,模型损失对邻域参数扰动的敏感程度
```

Validate 5 columns and unique keys.

### Status

Set:

- `1.3` → `in_progress`
- `1.3.1` and `1.3.2` → `drafted_and_verified`
- `1.3.3` → `drafted_and_verified`, artifact `chapters/ch01_introduction.tex`
- `1.3.4` → `queued`

Update concise `STATE.md`: next target 1.3.4; no 1.3.4 prose.

## Step 5: fast verification

Run the quiet fast-section script. Verify all citations, metadata, CSVs, hashes, empty later sections, `git diff --check`, unchanged `sources/`, and no new warning. No routine PDF inspection unless a new anomaly is reported.

## Step 6: concise report

Update `handoff/LATEST_CODEX_REPORT.md` in the content commit with the required concise evidence, build, preservation, and next-target record. No receipt-only commit.

## Step 7: commit and deploy

Use one content commit such as:

```bash
git commit -m "Draft Chapter 1 Section 1.3.3"
git push origin main
```

Then:

```bash
bash scripts/sync_latex_to_overleaf.sh --skip-local-build "Sync Chapter 1 Section 1.3.3"
```

Report both SHAs, no force-push, clean worktree, no second report commit.

## Definition of done

- exact 1.3.3 integration;
- prior prose unchanged;
- 1.3.4/1.4/1.5 empty;
- no new bibliography entry;
- `C1-091`--`C1-098` unique;
- valid terminology/status;
- fast verification passes;
- `sources/` unchanged;
- GitHub/Overleaf synchronized or exact failure reported;
- clean worktree;
- 1.3.4 undrafted.

Do not continue beyond Section 1.3.3.
