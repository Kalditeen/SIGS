# Phase 3-A 修订任务书：NetworkIR 到 Gardner Stage2 自动求解集成

## 一、任务目标

基于现有 Phase 1、Phase 2 和 Stage2 实现，建立一个 IR-aware 自动求解调度层。

核心目标：

实现 Phase 2 生成的 NetworkIR 候选自动进入现有 Gardner Stage2，完成：

1. 试探函数编译；
2. 参数注册；
3. Gardner PDE 残差构造；
4. 约束提取；
5. 参数分支求解；
6. 原始 Gardner PDE 恒等验证；
7. 有效网络分析；
8. 实验结果保存。

本任务不要求重写 Stage2，不要求立即优化复杂网络求解能力。

## 二、开发前置要求：再次核对实际接口

以 `PHASE3_INTERFACE_AUDIT.md` 为基础，核对以下接口：

- `CandidateManager.load`
- `CandidateManager.records`
- `AnsatzCompiler.compile_ir`
- `CompiledAnsatz`
- `Stage2Adapter.process`
- `_extract_coefficient_equations`
- `_solve_equations`
- `_residual_is_zero`
- `analyze_effective_network`

特别核对编译结果对象的真实类型、字段和符号身份，不要仅依靠旧报告中的类名和字段描述。

输出：

`docs/phase3/PHASE3_IMPLEMENTATION_PLAN.md`

## 三、实现自动求解调度器

建议新增：

`src/nnsca/search/automatic_solver.py`

如项目现有包结构有更合理的位置，可以调整。

调度器应完成以下流程：

CandidateManager
→ CandidateRecord
→ AnsatzCompiler.compile_ir
→ CompiledAnsatz
→ Gardner residual
→ constraint extraction
→ parameter solver
→ original PDE identity verification
→ effective network analysis
→ result persistence

要求：

1. 重新编译 `record.network_ir`，不要将 JSON 中的 expression 字符串作为主要符号计算输入。
2. 使用 `src/pdes/gardner.py` 中的 Gardner 方程定义，避免复制一份方程实现。
3. 复用现有 Stage2 的约束提取、参数求解和恒等验证函数。
4. 优先通过现有 `Stage2Adapter.process` 完成求解。
5. 如果现有 Adapter 的接口不足，只进行最小范围扩展。
6. 不要为了使用 `Stage2Input` 而强行重构 Adapter；先判断它是否有必要。
7. 单候选异常不能中止整个批次。

## 四、未知参数及角色管理

保留 Stage2 当前从表达式 `free_symbols` 提取未知参数的逻辑。

同时从 NetworkIR 获取：

- `parameter_symbols()`
- `parameter_roles()`

建立一致性检查：

- 编译表达式中的未知参数是否都能在 IR 参数注册表中找到；
- IR 中的参数是否全部实际出现在表达式中；
- 是否存在特殊函数参数；
- 参数符号是否因重复创建而发生身份不一致。

对于未出现在表达式中的 IR 参数，应记录为未使用参数，不应强行添加到 Stage2 方程组。

将参数角色信息传入最终结果记录，用于后续退化分析。

## 五、Gardner 残差和约束求解

使用现有 Gardner 残差函数：

`src/pdes/gardner.py::gardner_residual`

使用现有约束提取和参数求解函数。

不得在本阶段重写：

- `_extract_coefficient_equations`
- `_solve_equations`
- `_residual_is_zero`

如果遇到不支持的非多项式 phase 或嵌套激活：

1. 记录候选 ID；
2. 保存完整残差；
3. 保存约束提取错误；
4. 保存网络结构；
5. 记录失败阶段；
6. 继续执行其他候选。

不允许把约束提取失败直接记为无解。

## 六、求解状态与异常隔离

在自动求解层建立统一状态映射，同时保留 Stage2 原始返回结果。

至少区分：

- GENERATED
- COMPILED
- RESIDUAL_FAILED
- CONSTRAINT_FAILED
- SOLVER_TIMEOUT
- NO_SOLUTION
- SOLUTION_FOUND
- VERIFICATION_FAILED
- EXACT_VERIFIED

有效网络分析单独记录：

- DEGENERATE
- NONDEGENERATE
- UNKNOWN

注意：退化不代表数学解无效。

检查现有 timeout 是否能够真正中断 SymPy 阻塞任务。如果外层异常捕获无法实现超时隔离，采用最小范围的进程级隔离方案。

不得通过线程超时假装已经终止仍在运行的符号求解任务。

## 七、有效网络分析

对于通过原始 PDE 恒等验证的参数分支，调用：

`src/nnsca/analysis/effective_network.py`

记录：

- 不可达节点；
- 零权重；
- 常数化节点；
- 无效连接；
- 有效节点数量；
- 实际有效深度；
- 可疑的网络降阶情况。

不要把参数非零直接作为非退化证明。

不能自动确定的情况标记为 UNKNOWN。

本阶段不推广旧的 `_solve_equations_active_nondegenerate`，也不增加强制非退化约束。

## 八、实验

建立独立脚本：

`scripts/run_phase3_automatic_solving.py`

先使用小规模候选集完成端到端测试。

至少包含：

1. 一个已有 Jacobi 基准候选；
2. 一个双节点候选；
3. 一个双节点异构激活候选；
4. 一个双层候选。

如果候选池中缺少某类，必须记录，不得手工伪造候选。

所有测试必须通过实际 CandidateManager 和 NetworkIR 加载流程执行。

Jacobi 基准结果只能用于回归验证，不允许硬编码参数关系或解析解。

## 九、结果记录

建立：

`results/phase3_automatic_solving/`

每次运行使用独立目录，不覆盖历史结果。

至少保存：

- run_config.json
- candidate_results.json
- exact_solutions.json
- statistics.json
- run_report.md

对每个候选保存：

- candidate_id
- structure_signature
- random_seed
- NetworkIR
- 编译表达式
- 未知参数
- 参数角色
- 约束方程
- 求解分支
- 原始 PDE 残差
- 恒等验证结果
- 有效网络分析
- 各阶段耗时
- 失败原因

## 十、测试要求

新增自动求解器测试，至少覆盖：

1. 单候选成功；
2. 多候选批量执行；
3. 一个候选失败不影响其他候选；
4. 编译失败；
5. 约束提取失败；
6. 参数求解超时；
7. 找到参数分支但原始 PDE 验证失败；
8. 精确解通过原始 PDE 验证；
9. 参数角色一致性；
10. 有效网络分析。

运行 Phase 1、Phase 2 相关回归测试。

已知 `test_hf_data.py` 的 NumPy/pyarrow 环境问题单独报告，不得将其算作代码测试通过。

## 十一、禁止事项

- 不重写 Stage2 核心；
- 不修改 Gardner 方程定义；
- 不硬编码 Jacobi 精确解；
- 不强制非退化参数约束；
- 不放宽未知参数数量保护；
- 不把求解失败解释为不存在解；
- 不删除或覆盖历史 results；
- 不跳过原始 PDE 恒等验证。

## 十二、交付报告

生成：

`docs/phase3/PHASE3_A_INTEGRATION_REPORT.md`

报告必须回答：

1. NetworkIR 是否成功进入 Stage2？
2. 是否完整恢复已有 Jacobi 基准？
3. 哪些候选能够完成完整求解？
4. 哪些候选在编译、约束提取、参数求解阶段失败？
5. 是否发生超时？
6. 是否发现网络退化？
7. 参数角色是否完整保留？
8. 当前自动求解器的主要瓶颈是什么？

完成后暂停，不要自动开始 Phase 3-B 或 Phase 3-C。

最终输出：

`PHASE3_A_INTEGRATION_COMPLETED`

只有所有验收项目通过时，才能输出该标志。