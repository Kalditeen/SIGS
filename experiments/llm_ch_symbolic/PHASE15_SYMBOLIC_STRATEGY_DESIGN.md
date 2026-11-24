# Phase 1.5 符号策略扩展设计：Jacobi 椭圆函数与多函数族代数关系

本文件是设计文档，不修改现有 Gardner 求解程序，也不向规则注册表添加未经验证的规则。

## 1. 目标

把 Phase 1.5 的“规则注册表 + LLM 策略规划 + SymPy 验证”机制，从当前 `exp / poly2 / sinh / cosh / sin / cos / tanh / weierstrass(占位)` 扩展到：

- Jacobi 椭圆函数 `JacobiCN / JacobiSN / JacobiDN`；
- 不同特殊函数组合；
- 多层嵌套特殊函数；
- 复合激活函数；
- 多函数族之间的代数关系。

## 2. 扩展 Jacobi 函数的微分规则

SymPy 使用椭圆参数 `m`，其 `JacobiSN(z, m)` 的偏导由 SymPy 内部定义，可直接验证并注册为 `der_jacobi_sn` 等。注册前必须用 SymPy 符号验证：

- `d/dz JacobiSN(z,m) = JacobiCN(z,m) * JacobiDN(z,m)`；
- `d/dz JacobiCN(z,m) = -JacobiSN(z,m) * JacobiDN(z,m)`；
- `d/dz JacobiDN(z,m) = -m * JacobiSN(z,m) * JacobiCN(z,m)`。

验证方式是构造 `diff(f(z,m), z)` 与预期导数的差值并用 `sp.simplify`（或 `sp.trigsimp` 无法处理时用 `sp.rewrite` 辅助）证明为零。注意 SymPy 的 `diff(JacobiSN(z,m), z)` 本身已返回闭合形式，因此这条验证只用于确认注册表表达式与 SymPy 一致。

参数角色必须记录：`m` 是椭圆参数，不是网络可训练参数；在 NetworkIR 中应作为特殊函数参数单独登记，避免与仿射权重混淆。

## 3. Jacobi 恒等式

候选恒等式（每一行都需要独立符号验证后才能注册）：

- `JacobiSN(z,m)^2 + JacobiCN(z,m)^2 = 1`；
- `JacobiDN(z,m)^2 + m * JacobiSN(z,m)^2 = 1`；
- 加法公式与平方关系仅在明确需要时引入，避免规则爆炸。

Phase 1.5 的教训是：恒等式规则的适用性必须显式编码。例如 `id_sn_cn` 只在同一 IR 同时出现 `JacobiSN` 和 `JacobiCN` 时适用，并且只有当二者共享相同参数 `m` 时才能合法合并。验证器需要把“参数一致性”纳入适用性检查，不能只看函数名。

## 4. 函数微分代数关系接口

新增一个可扩展接口 `differential_algebra.py`，为每类函数提供：

- `derivative_closure(activation, z, m) -> list[expr]`：导数如何重新表示为同族函数；
- `identity_candidates(activations) -> list[rule_id]`：给定函数集合，返回可应用的恒等式；
- `independence_status(expr1, expr2) -> independent | dependent | unknown`。

核心纪律：如果无法证明不同自变量的函数项之间线性独立，必须返回 `unknown`，不允许据此强行生成代数约束。这一点在双节点/多层网络中尤其关键，因为两个节点可能共享同一仿射输入或同一参数。

## 5. 复合激活与嵌套特殊函数

对于 `sinh(JacobiCN(...))` 这类嵌套，建议分两层处理：

1. 外层用链式法则展开成 `cosh(inner) * inner'`；
2. 内层用 Jacobi 微分规则展开。

LLM 的输出应描述这种“由外向内”的微分计划，而不是直接给最终展开式。执行器应记录每一步的规则 ID 和等价性检查。嵌套深度超过阈值时，优先用中间变量表示内层，避免符号爆炸。

## 6. 中间变量与公共子表达式

Phase 1.5 当前只做了“结构因子分组”，没有把 LLM 提出的 `generators / intermediate_variables` 真正用于约束提取。扩展设计：

- 把 LLM 声明的中间变量映射到 NetworkIR 的真实节点 ID；
- 在残差构造前按拓扑序为共享子表达式命名；
- 对残差按这些中间变量做 `collect`，再提取系数；
- 每一步 `collect` 都要做等价性校验。

公共子表达式识别应由 NetworkIR 的 `consumer_counts` 提供基准，LLM 只能提出候选，不能决定最终生成元；最终生成元必须能由 SymPy 验证。

## 7. 多层嵌套网络的策略分层

Level 3 的 1426 项残差说明“一次性展开整网”会迅速失控。建议：

- 先对每层做局部残差和局部公共项分析；
- 再按拓扑序逐层合成；
- 对过大的中间结果用未求值函数或形式变量保持可读性；
- 最终恒等验证仍然对原始 PDE 残差执行，不允许用分层近似替代。

## 8. 对验证器的增量要求

1. 规则 ID 必须存在；
2. 节点 ID 必须存在；
3. 激活函数必须与 IR 一致；
4. 导数规则必须与激活函数匹配；
5. 恒等式规则必须同时满足“函数对存在”和“参数一致”；
6. 未证明的函数独立性必须标记 `unknown`；
7. 每个符号变换必须记录变换前、变换后、规则 ID 和等价性检查结果。

## 9. 与 Gardner 主流程的接口

不修改 `src/pdes/gardner.py` 和现有 Stage2。扩展后的规则注册表和验证器作为独立模块供 Gardner 实验导入；LLM 只负责结构清点与策略规划，系数提取和原方程恒等验证继续由现有 SymPy 模块完成。
