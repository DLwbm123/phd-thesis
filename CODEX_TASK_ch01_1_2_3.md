# Codex Task: integrate Chapter 1, Section 1.2.3

Read and obey `AGENTS.md`, `THESIS_CONTRACT.md`, `AUTHORSHIP_PROTOCOL.md`, `AUTHOR_VOICE.md`, `STATE.md`, `PROJECT_CONFIG.md`, and `chapter_cards/ch01.md` before editing.

## Goal

Integrate the GPT Pro-approved draft for Section 1.2.3 “联邦持续医学影像学习研究现状” into the thesis repository. Add only the verified references, evidence records, and terminology updates supplied below; compile and inspect the complete thesis; run all required audits; push the verified work to `origin/main`; and synchronize the compilable LaTeX subset to Overleaf.

This is the third and final task for Section 1.2. It assumes that 1.2.1 and 1.2.2 have already been completed and verified. Stop after 1.2.3. Do not draft Section 1.3.

## Evidence policy

The user-provided Yang et al. survey supplies the broad federated continual learning framework and knowledge-fusion taxonomy. Concrete method claims must rely on the cited original papers. The medical discussion is grounded in original histopathology, thoracic-infection, and chest-radiograph studies.

The term “spatial catastrophic forgetting” was explicitly introduced by Yang et al. in their survey. If mentioned, it must be attributed to that paper. The thesis-preferred description for its own problem is “跨客户端全局灾难性遗忘” or “全局灾难性遗忘”, depending on context.

## Strict scientific boundaries

- Do not state that federated learning automatically provides a formal privacy guarantee.
- “Raw data remain local” describes data flow only. Parameters, gradients, prototypes, features, public surrogate data, and auxiliary mechanisms must be discussed separately.
- Only differential privacy mechanisms with an explicit privacy definition may be described as providing a formal differential-privacy guarantee, and only within their reported assumptions.
- Do not claim that all medical institutions prohibit replay or delete historical data.
- Do not equate client heterogeneity with catastrophic forgetting without a sequential or aggregation-induced performance-loss definition.
- Do not treat Yang et al.’s “SpatialCF” term as universal consensus.
- Do not assume all FCL systems are synchronous, class-incremental, or use the same task order.
- Do not compare methods as if their public-data, replay, task-identity, client-participation, and privacy assumptions were identical.
- Do not describe FedSubMerge as providing formal privacy protection.
- Do not disclose the thesis method’s full equations, experimental numbers, or contribution list in this subsection.
- Do not draft Section 1.3 or later sections.
- Do not modify `sources/` or import content from `sources/reference_thesis/`.

## Strict file scope

Files that may be modified or added:

- `CODEX_TASK_ch01_1_2_3.md`
- `chapters/ch01_introduction.tex`
- `bibliography/references.bib`
- `config/build_flags.tex` — only if needed to preserve `\thesisbibliographytrue`
- `evidence/claims.csv`
- `qa/terminology.csv`
- `qa/chapter_status.csv`
- `qa/style_audit_report.md`
- `qa/reference_overlap_report.md`
- `STATE.md`
- `handoff/LATEST_CODEX_REPORT.md`

Do not change another chapter, template/class file, figure, table, script, bibliography style, or any file under `sources/`. Do not rewrite approved prose outside 1.2.3.

## Step 0: repository and baseline preflight

1. Run:

   ```bash
   git status --short
   git branch --show-current
   git fetch origin
   ```

2. Require a clean worktree except this untracked task file.
3. Confirm `main`, no divergence, and fast-forward only if required.
4. Record baseline SHA.
5. Confirm:
   - Section 1.1 complete;
   - 1.2.1 and 1.2.2 are `drafted_and_verified`;
   - 1.2.3 title and label exist with an empty body;
   - Section 1.3 remains body-empty.
6. Save byte-for-byte hashes of Section 1.1, 1.2.1, 1.2.2, and the empty Section 1.3 body.
7. Confirm claims through `C1-059` and all prior terminology records.
8. Record actual bibliography count; the expected sequential baseline is 36 entries if every prior task entry was newly added.
9. Confirm `\thesisbibliographytrue`.
10. Snapshot `sources/` file count and SHA-256.

If 1.2.1 or 1.2.2 is incomplete, stop rather than combining tasks.

## Step 1: integrate the approved draft exactly

Preserve:

```latex
\subsection{联邦持续医学影像学习研究现状}
\label{subsec:intro-federated-continual-learning}
```

Insert immediately after the label and before Section 1.3:

```latex
联邦学习通过在各参与方本地训练并在服务器端聚合更新，使多个医疗中心能够在不集中原始影像的条件下协同建模\cite{mcmahan2017fedavg,rieke2020future,sheller2020federated}。既有医学联邦学习主要研究固定任务下的数据异质性、优化收敛和跨中心泛化；当各中心还需要依次学习新的类别、域或诊断任务时，客户端本地数据流和服务器聚合过程同时具有时间维度，问题由静态联邦学习扩展为联邦持续学习。

联邦持续学习要求各客户端从私有任务序列中更新模型，并通过通信形成能够覆盖多个客户端历史知识的共享模型。Yang 等将现有系统概括为同步和异步两类：同步设定中客户端按照共同任务顺序推进，异步设定中各客户端的任务内容、顺序或进度可以不同\cite{yang2024fclsurvey}。这一划分有助于说明服务器何时接收知识，但不能替代对标签空间、客户端参与、任务身份和历史数据访问条件的具体说明。

该问题包含两类相互耦合的知识损失。客户端在学习后续任务时可能降低旧任务性能，形成时间维度的灾难性遗忘；服务器聚合异质客户端更新时，又可能覆盖只存在于部分中心的任务知识。Yang 等将后一现象类比为“空间灾难性遗忘”，并据此讨论空间—时间遗忘\cite{yang2024fclsurvey}。由于这一术语由该综述提出，本文仅在介绍其分类时加以引用；对于多中心历史任务在聚合后发生的整体性能下降，本文统一使用跨客户端全局灾难性遗忘进行描述。

早期联邦持续学习方法主要从参数分解和跨客户端知识选择入手。FedWeIT 将模型分为全局共享参数和稀疏任务特定参数，并根据任务相关性选择性接收其他客户端知识\cite{yoon2021fedweit}。这种设计可以减少不相关任务之间的直接干扰，但需要保存和管理任务相关状态，其效果也依赖任务关系估计和客户端通信条件。

知识蒸馏提供了另一类融合方式。CFeD 在客户端和服务器两侧分别使用无标签代理数据进行蒸馏，并让部分客户端学习新任务、部分客户端复习旧任务\cite{ma2022cfed}。在类别增量场景中，GLFC 结合类别感知梯度补偿、类别关系蒸馏、代理服务器和原型梯度通信，分别缓解本地类别不平衡与全局模型遗忘\cite{dong2022glfc}。这类方法减少了对完整旧图像的直接访问，但引入了代理数据、旧模型选择或原型构造等附加假设。

从更广的知识融合角度看，Yang 等将相关方法整理为回放、聚类、参数正则、参数隔离、动态结构、原型和知识蒸馏等路线\cite{yang2024fclsurvey}。不同路线传递的数据、模型或输出信息不同：回放方法保留样本或替代数据，参数方法直接约束或选择模型更新，原型和蒸馏方法则以压缩表示或预测关系传递知识。这一分类描述了融合载体，但不能据此推断某一方法在不同医疗任务、客户端数量和通信预算下具有统一优势。

联邦环境中的信息交换还需要与隐私机制区分。原始数据留在本地并不意味着共享梯度、参数、特征或原型不含训练信息，使用公共代理数据也会改变适用条件\cite{rieke2020future,yang2024fclsurvey}。因此，评价联邦持续医学影像方法时，应同时报告传输对象、历史数据或替代信息、可信参与方和附加保护机制，而不能仅以“数据不出中心”宣称形式化隐私。

医学影像中的联邦持续研究开始同时处理空间异质性和时间变化。DynBC 在病理图像分割中使用公共参考数据评价候选更新的连续性，以联合缓解客户端漂移和顺序学习遗忘\cite{babendererde2025dynbc}。该方法表明，服务器可以利用独立参考信息筛选跨中心更新；其适用性同时依赖公共参考数据能否获得以及参考数据对目标分布变化的代表程度。

在医学图像分类中，Zhou 和 Wang 将多种持续学习算法与联邦训练结合，用于顺序胸部感染类别识别，并比较不同网络结构在其公开数据设定下的表现\cite{zhou2025thoracicfcl}。该研究说明，通用持续学习机制在联邦医疗分类中的效果会受到模型结构、客户端数量和非独立同分布划分影响。由于其客户端和中心由公开数据模拟，相关结果不应直接等同于真实医院部署结论。

近期研究还将显式隐私机制加入联邦持续医疗分类。DP-FedEPC 在胸部X射线分类中结合弹性权重巩固、潜在原型和客户端差分隐私随机梯度下降，并报告对应的隐私预算\cite{sinhal2026dpfedepc}。其中，形式化差分隐私来自梯度裁剪、噪声机制和隐私核算，而不是联邦聚合本身；潜在原型仍属于历史信息的压缩保存，也不等同于完全无回放。

无回放方法试图在不保存旧图像或生成样本的条件下保护历史任务。梯度投影记忆通过奇异值分解保存旧任务的重要梯度方向，并将新梯度投影到其正交补空间\cite{saha2021gpm}。该方法最初面向观察完整任务序列的单一学习器；在联邦环境中，各客户端独立构建的保护子空间只能覆盖本地历史，无法直接包含仅由其他中心学习的任务知识。因而，如何在服务器端汇集跨客户端历史保护信息，并避免无差别保护对新任务造成过强约束，成为无回放联邦持续医学影像学习的进一步问题。

总体来看，联邦持续学习已从参数分解、蒸馏和类别增量补偿，扩展至更新筛选、显式差分隐私和无回放梯度空间保护。现有研究的任务顺序、同步方式、公共数据依赖、回放形式、通信对象和隐私假设差异较大，方法结果不能在忽略这些条件时直接横向排序。对于多中心无回放医学图像分类，仍需解决跨客户端历史知识如何形成全局保护，以及统一保护如何避免压低异质客户端的新任务学习能力。上述问题将在下一节作为本文的关键技术挑战进一步归纳。
```

After insertion verify:

- Section 1.1, 1.2.1, and 1.2.2 byte-for-byte unchanged.
- Section 1.3 remains body-empty.
- 1.2.3 title and label unique.
- “空间灾难性遗忘” is explicitly attributed to Yang et al.
- no formal-privacy claim is attached to FL itself;
- no claim that compressed prototypes equal no replay;
- no detailed FedSubMerge method, equations, or results are disclosed;
- the final paragraph transitions to 1.3 without drafting it.

## Step 2: add verified bibliography entries

Deduplicate by key, DOI, and normalized title. Add or reuse only cited entries:

```bibtex
@inproceedings{mcmahan2017fedavg,
  author    = {McMahan, H. Brendan and Moore, Eider and Ramage, Daniel and Hampson, Seth and {Ag{\"u}era y Arcas}, Blaise},
  title     = {Communication-Efficient Learning of Deep Networks from Decentralized Data},
  booktitle = {Proceedings of the 20th International Conference on Artificial Intelligence and Statistics},
  series    = {Proceedings of Machine Learning Research},
  volume    = {54},
  pages     = {1273--1282},
  publisher = {PMLR},
  year      = {2017}
}

@article{yang2024fclsurvey,
  author  = {Yang, Xin and Yu, Hao and Gao, Xin and Wang, Hao and Zhang, Junbo and Li, Tianrui},
  title   = {Federated Continual Learning via Knowledge Fusion: A Survey},
  journal = {IEEE Transactions on Knowledge and Data Engineering},
  volume  = {36},
  number  = {8},
  pages   = {3832--3850},
  year    = {2024},
  doi     = {10.1109/TKDE.2024.3363240}
}

@inproceedings{yoon2021fedweit,
  author    = {Yoon, Jaehong and Jeong, Wonyong and Lee, Giwoong and Yang, Eunho and Hwang, Sung Ju},
  title     = {Federated Continual Learning with Weighted Inter-client Transfer},
  booktitle = {Proceedings of the 38th International Conference on Machine Learning},
  series    = {Proceedings of Machine Learning Research},
  volume    = {139},
  pages     = {12073--12086},
  publisher = {PMLR},
  year      = {2021}
}

@inproceedings{ma2022cfed,
  author    = {Ma, Yuhang and Xie, Zhongle and Wang, Jue and Chen, Ke and Shou, Lidan},
  title     = {Continual Federated Learning Based on Knowledge Distillation},
  booktitle = {Proceedings of the Thirty-First International Joint Conference on Artificial Intelligence},
  pages     = {2182--2188},
  year      = {2022},
  doi       = {10.24963/ijcai.2022/303}
}

@inproceedings{dong2022glfc,
  author    = {Dong, Jiahua and Wang, Lixu and Fang, Zhen and Sun, Gan and Xu, Shichao and Wang, Xiao and Zhu, Qi},
  title     = {Federated Class-Incremental Learning},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  pages     = {10164--10173},
  year      = {2022}
}

@inproceedings{babendererde2025dynbc,
  author    = {Babendererde, Niklas and Zhu, Haozhe and Fuchs, Moritz and Stieber, Jonathan and Mukhopadhyay, Anirban},
  title     = {Federated-Continual Dynamic Segmentation of Histopathology Guided by Barlow Continuity},
  booktitle = {Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision},
  pages     = {3752--3761},
  year      = {2025}
}

@article{zhou2025thoracicfcl,
  author  = {Zhou, Tianshuo and Wang, Boyuan},
  title   = {Cross Paradigm Fusion of Federated and Continual Learning on Multilayer Perceptron Mixer Architecture for Incremental Thoracic Infection Diagnosis},
  journal = {Scientific Reports},
  volume  = {15},
  pages   = {24449},
  year    = {2025},
  doi     = {10.1038/s41598-025-06077-8}
}

@article{sinhal2026dpfedepc,
  author  = {Sinhal, Anay and Sinhal, Amit and Sinhal, Arpana},
  title   = {Federated Continual Learning for Privacy-Preserving Chest Radiograph Classification},
  journal = {Scientific Reports},
  year    = {2026},
  doi     = {10.1038/s41598-026-55211-7}
}

@inproceedings{saha2021gpm,
  author    = {Saha, Gobinda and Garg, Isha and Roy, Kaushik},
  title     = {Gradient Projection Memory for Continual Learning},
  booktitle = {International Conference on Learning Representations},
  year      = {2021}
}
```

Existing `rieke2020future` and `sheller2020federated` must be reused. Keep `\thesisbibliographytrue`.

## Step 3: append evidence records

```csv
C1-060,1,1.2.3,联邦学习通过本地训练和服务器聚合支持不集中原始数据的协同建模,primary federated learning paper,Algorithm and setting,mcmahan2017fedavg,method,confirmed,drafted,数据流描述不等于形式化隐私保证
C1-061,1,1.2.3,联邦持续学习结合客户端私有任务序列和跨客户端知识融合,DOI:10.1109/TKDE.2024.3363240,Abstract and framework,yang2024fclsurvey,literature,confirmed,drafted,用于定义通用FCL框架
C1-062,1,1.2.3,同步与异步FCL由客户端任务顺序和更新进度关系区分,DOI:10.1109/TKDE.2024.3363240,Framework taxonomy,yang2024fclsurvey,literature,confirmed,drafted,仍需另行说明标签和数据访问条件
C1-063,1,1.2.3,空间灾难性遗忘是Yang等在其综述中提出的跨客户端聚合类比概念,DOI:10.1109/TKDE.2024.3363240,Introduction and problem definition,yang2024fclsurvey,author_attributed_term,confirmed,drafted,本文自身优先使用跨客户端全局灾难性遗忘
C1-064,1,1.2.3,FedWeIT分解全局参数和任务特定参数并选择性转移其他客户端知识,primary paper,Abstract and method,yoon2021fedweit,method,confirmed,drafted,用于参数分解与选择传输路线
C1-065,1,1.2.3,CFeD在客户端和服务器两侧使用无标签代理数据进行知识蒸馏,DOI:10.24963/ijcai.2022/303,Abstract and method,ma2022cfed,method,confirmed,drafted,明确记录代理数据依赖
C1-066,1,1.2.3,GLFC结合类别梯度补偿关系蒸馏代理服务器和原型梯度通信处理联邦类增量遗忘,primary paper,Abstract and method,dong2022glfc,method,confirmed,drafted,结论限于其类别增量设定
C1-067,1,1.2.3,FCL知识融合方法可按回放聚类正则参数隔离动态结构原型和蒸馏等载体组织,DOI:10.1109/TKDE.2024.3363240,Knowledge fusion taxonomy,yang2024fclsurvey,literature,confirmed,drafted,分类不代表统一性能排序
C1-068,1,1.2.3,原始数据留在本地不代表梯度参数特征或原型交换自动获得形式化隐私,DOI:10.1038/s41746-020-00323-1;DOI:10.1109/TKDE.2024.3363240,Security discussion,rieke2020future;yang2024fclsurvey,literature,confirmed,drafted,用于限制隐私表述
C1-069,1,1.2.3,DynBC使用公共参考数据评价更新连续性以联合处理客户端漂移和时间遗忘,primary paper,Abstract and method,babendererde2025dynbc,method,confirmed,drafted,依赖公共参考数据代表性
C1-070,1,1.2.3,公开胸部X射线与CT研究比较多种模型和持续学习算法的联邦组合,DOI:10.1038/s41598-025-06077-8,Abstract and experimental design,zhou2025thoracicfcl,primary_experiment,confirmed,drafted,模拟客户端结果不等同真实医院部署
C1-071,1,1.2.3,DP-FedEPC结合EWC潜在原型和客户端DP-SGD处理胸片FCL,DOI:10.1038/s41598-026-55211-7,Abstract,sinhal2026dpfedepc,method,confirmed,drafted,形式化差分隐私来自DP机制而非联邦聚合
C1-072,1,1.2.3,潜在原型属于历史信息的压缩保存而不等同完全无回放,author scope definition,Section distinction,sinhal2026dpfedepc,author_definition,confirmed,drafted,用于统一回放边界
C1-073,1,1.2.3,GPM保存旧任务重要梯度子空间并将新梯度投影到正交补空间,primary paper,Method formulation,saha2021gpm,method,confirmed,drafted,原始方法面向单一学习器
C1-074,1,1.2.3,无回放医学FCL仍需跨客户端汇集历史保护并控制统一保护对新任务可塑性的约束,author synthesis based on section sources,Section synthesis,yoon2021fedweit;saha2021gpm;yang2024fclsurvey,author_analysis,confirmed,drafted,用于过渡至1.3.4且不提前展开FedSubMerge
```

Validate exactly 11 columns, unique IDs `C1-060`--`C1-074`, unchanged prior rows, and active citation keys.

## Step 4: terminology and status

### Add non-duplicate terminology rows

```csv
synchronous federated continual learning,同步联邦持续学习,第一章与第六章,同步持续联邦学习（避免混用）,客户端按照共同任务顺序或共同阶段推进
asynchronous federated continual learning,异步联邦持续学习,第一章与第六章,异步持续联邦学习（避免混用）,客户端任务顺序进度或上传时刻可以不同
cross-client global catastrophic forgetting,跨客户端全局灾难性遗忘,第一章与第六章,空间灾难性遗忘（仅在归因Yang等术语时使用）,聚合和后续训练导致分散于不同客户端的历史任务能力下降
client drift,客户端漂移,第一章与第六章,客户漂移（避免混用）,本地异质更新偏离共享优化目标的现象
knowledge fusion,知识融合,第一章与第六章,知识聚合（机制不同不得等同）,对样本参数特征原型或输出关系进行跨阶段或跨客户端整合
surrogate dataset,代理数据集,第一章与第六章,公共数据集（不一定等同）,用于蒸馏评估或重建知识的附加数据
prototype communication,原型通信,第一章与第六章,原型共享（按具体协议使用）,客户端与服务器交换类别或特征原型
differential privacy,差分隐私,第一章与第六章,隐私保护（范围更宽）,只有明确机制参数与核算时才表述形式化保证
```

Update existing scopes:

- `federated continual learning` → `第一章与第六章`
- `replay-free` → `第一章与第六章`
- `principal gradient subspace` → `第一章与第六章`
- `subspace merging` → `第一章与第六章`

Do not add `spatial catastrophic forgetting` as the thesis-preferred term. If it is registered for traceability, its note must explicitly say it is Yang et al.’s introduced term and not the preferred thesis term; otherwise omit it.

### Status

Set:

- `1.2` → `drafted_and_verified`, artifact `chapters/ch01_introduction.tex`
- `1.2.1` → `drafted_and_verified`
- `1.2.2` → `drafted_and_verified`
- `1.2.3` → `drafted_and_verified`, artifact `chapters/ch01_introduction.tex`
- `1.3` → `queued`

Update `STATE.md`:

- Section 1.2 complete at current draft stage;
- all three subsections integrated and verified;
- next target is 1.3.1 “稀疏标注下监督不足与结构信息缺失”;
- Section 1.3 remains undrafted;
- exact build, audits, PDF, GitHub, Overleaf, and warnings.

## Step 5: compile and audit

Run the complete build, style audit, and overlap audit. Check:

1. all Chapter 1 citations resolve;
2. no duplicate key/DOI/title;
3. no undefined citation/reference, duplicate label, missing file, or placeholder;
4. claims and terminology CSV schemas and uniqueness;
5. Section 1.1, 1.2.1, and 1.2.2 unchanged;
6. Section 1.3 body-empty;
7. attribution of Yang et al.’s term;
8. privacy-language boundary;
9. replay/prototype distinction;
10. no detailed FedSubMerge method/results;
11. unchanged `sources/`;
12. visual inspection of every 1.2.3 and updated bibliography page;
13. final PDF page count, size, SHA-256, and warning comparison.

## Step 6: handoff report

Replace `handoff/LATEST_CODEX_REPORT.md` with a complete report including:

- preflight and baseline SHA;
- exact changed files;
- exact prose integration and preserved hashes;
- bibliography additions/reuse and duplicate checks;
- evidence/terminology/status changes;
- full build and citation integrity;
- style/overlap/CSV checks;
- PDF pages visually inspected;
- `sources/` before/after snapshot;
- unresolved scientific/source/layout issues;
- explicit privacy and terminology-boundary confirmations;
- GitHub content and report commit SHAs;
- Overleaf deployment SHA;
- confirmation that Section 1.2 is complete and Section 1.3 is undrafted;
- next target 1.3.1.

## Step 7: commit, push, and sync

Create and push a content commit such as:

```bash
git commit -m "Draft Chapter 1 Section 1.2.3"
git push origin main
```

After remote verification and a clean worktree:

```bash
bash scripts/sync_latex_to_overleaf.sh "Sync Chapter 1 Section 1.2.3"
```

Record the deployment. Push a report-only commit if necessary without re-running Overleaf sync. Never force-push.

Final checks:

```bash
git status --short
git rev-parse HEAD
git rev-parse origin/main
```

## Definition of done

- 1.2.3 integrated exactly;
- Sections 1.1, 1.2.1, and 1.2.2 unchanged;
- Section 1.3 body-empty;
- all cited verified references added/reused without duplicates;
- `C1-060`--`C1-074` present exactly once;
- terminology and scope updates valid;
- all of Section 1.2 marked verified;
- full compile, audits, CSV checks, and PDF visual inspection completed;
- privacy, replay, and terminology boundaries preserved;
- `sources/` unchanged;
- GitHub and Overleaf synchronized or exact failure reported;
- clean worktree;
- Section 1.2 complete and next target 1.3.1;
- no Section 1.3 prose drafted.

Do not continue beyond Section 1.2.3.
