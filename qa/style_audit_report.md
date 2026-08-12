# 作者表达审查报告

> 本报告是规则型写作质量检查，不是 AI 检测器，也不能预测任何检测结果。

## 规则命中

| 文件 | 类别 | 模式 | 次数 | 原因 |
|---|---|---:|---:|---|
| `chapters/ch01_introduction.tex` | transition | `同时` | 24 | 过度依赖统一连接词 |
| `chapters/ch03_benchmark.tex` | transition | `同时` | 12 | 过度依赖统一连接词 |
| `chapters/ch05_scribble_samcl.tex` | transition | `同时` | 17 | 过度依赖统一连接词 |
| `chapters/ch05_scribble_samcl.tex` | sequence | `最后` | 5 | 避免所有段落都采用固定枚举结构 |

## 重复段落开头

| 归一化开头 | 次数 |
|---|---:|
| `figure[htbp]` | 8 |
| `table[htbp]P` | 4 |
| `table[htbp]S` | 4 |
| `FedSubMerge-` | 3 |
| `figures/ch05` | 3 |

## 解释原则

命中不等于错误。技术术语可合理重复；需要人工判断是否为空泛套话、机械衔接或必要的精确表达。禁止为了消除命中而无意义替换同义词。
