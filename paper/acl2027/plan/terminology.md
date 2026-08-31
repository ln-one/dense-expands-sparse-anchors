# Terminology lock

| Chinese concept | Manuscript term |
|---|---|
| 本文方法 | Dense Expansion and Sparse Anchoring (DESA); define once, then DESA |
| 大语言模型查询扩展 | LLM-based query expansion |
| 通道非对称查询扩展 | channel-asymmetric query expansion |
| 互补参考文本 | complementary reference passages; generated reference passages after definition |
| dense / sparse 检索器 | dense / sparse retriever |
| dense / sparse 通道 | dense / sparse retrieval channel; channel after definition |
| Dense 正交残差扩展 | orthogonal residual expansion |
| Sparse 分数乘积锚定 | score-product anchoring |
| 逐文档分数相乘 | document-wise score product |
| 无查询扩展 | no expansion / the unexpanded query |
| 共享扩展 | shared expansion |
| 固定 top-L 截断 | fixed top-$L$ cutoff |
| 完整列表融合 | complete-list fusion |
| 有序 top-K | ordered top-$K$ |
| 每通道访问深度 | per-channel access depth |
| 回放停止深度 | replay stopping depth |
| 检索效果 | retrieval effectiveness |
| 访问深度下降 | access-depth reduction |

Use `query expansion` as the paper-wide category. Reserve `query rewriting`
for descriptions of sources that use that term. `Dense expands; sparse anchors.`
is a narrative summary rather than a separately defined algorithmic term.
The paper title is `Dense Expands, Sparse Anchors: Coordinated Query Expansion`.

Use lowercase `dense` and `sparse` in ordinary prose, following recent ACL
retrieval papers. Capitalization is reserved for the title-level slogan and
method/table labels such as `Dense only` and `Sparse only`.

Use `retriever` for the retrieval model or scoring system and `retrieval
channel` for the ranked-list path whose access is replayed. Do not use the two
terms interchangeably within the same definition.

Use source-specific generated-text names only when describing those methods:
HyDE generates a `hypothetical document`, Query2doc generates a
`pseudo-document`, and MuGI generates `pseudo-references`. DESA generates
`complementary reference passages`; after definition, use `generated reference
passages` or `generated passages`. Avoid unqualified `generated evidence`,
which can imply judged or corpus-grounded evidence.

Use `access depth` for the reported metric family and `replay stopping depth`
for the operational value returned by the certification replay. Do not use
`exact-access depth` or standalone `replay depth`. Use `fusion-side ranking
access` when counting the total rank entries consumed across channels.

Use lowercase `top-$L$`, `top-$K$`, and `top-20` in running text and captions.
Use `Original` consistently as the no-expansion baseline label; do not alternate
between `Original` and `No expansion` in tables.

Use `dataset` for a BEIR evaluation task and its judgments, and `corpus` for its
document collection. Use `retrieval effectiveness` for metric-based outcomes;
reserve `quality` for established method names or quoted source language.

Use `retrieval-augmented generation (RAG)` only for systems that retrieve
context for a generation stage. DESA is a query-construction and hybrid-
retrieval method motivated by RAG retrieval, not an end-to-end RAG system.
