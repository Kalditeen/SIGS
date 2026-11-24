# 任务书：打通 LLM 策略字段到 SymPy 系数提取的执行链路

## 任务来源

本任务书由当前审计线程编写，交给本地 Codex 对话“11.23”执行。当前审计线程只负责代码审查、验收和建议，不直接修改实现代码。

## 背景

Phase 1.5 已经完成两个独立能力：

1. LLM 能读取 NetworkIR，输出结构分析和符号处理策略；
2. 三指数 CH 案例已经跑通“LLM 分组 -> 系数提取 -> 代数求解 -> 原始 PDE 验证”。

但两者目前没有连在一起。核心问题位于 `experiments/llm_ch_symbolic/src/symbolic_executor.py`：

- `execute_strategy()` 只消费 `selected_identity_rules`；
- `selected_derivative_rules` 只被验证，实际求导由 SymPy `diff` 完成；
- `generators`、`intermediate_variables`、`collection_strategy`、`rewrite_strategy`、`expected_structure` 仅被 `strategy_validator.py` 规范化保存，执行器没有使用；
- `execute_strategy()` 的返回只包含残差项数和公共项分组，不包含系数方程、代数分支或原始 PDE 验证。

因此 Phase 1.5 证明的是“LLM 能做结构识别和规则选择”，还没有证明“LLM 输出的策略能真正驱动 SymPy 完成系数约束提取”。

## 目标

在 `experiments/llm_ch_symbolic` 内实现一个可审计、可测试的策略驱动执行链路：

- 已验证的 LLM 策略字段真实参与 SymPy 残差整理；
- 整理后能提取系数约束方程；
- 所有数学正确性由 SymPy 独立验证；
- 不要求 LLM 每次都跑真实 API，确定性单元测试必须覆盖核心执行器。

## 范围

只允许修改以下目录和文件：

- `experiments/llm_ch_symbolic/src/`
- `experiments/llm_ch_symbolic/tests/`
- `experiments/llm_ch_symbolic/prompts/`，仅在字段语义确需调整时修改
- `experiments/llm_ch_symbolic/scripts/run_phase15.py`，仅用于接入新执行结果输出

禁止：

- 修改 `src/pdes/`、`src/nnsca/` 或 SIGS 主流程代码；
- 修改 Phase 1、Phase 2、Phase 3 已完成的实现；
- 覆盖 `experiments/llm_ch_symbolic/results/` 下的历史结果；
- 把 Maple 已知参数分支硬编码进求解器；
- 引入新的特殊函数规则或 Jacobi 椭圆函数；
- 在未完成本任务前接入 Gardner 方程。

## 当前代码事实

需要基于以下事实实现，不要重新猜测：

- NetworkIR 编译和拓扑摘要：`src/network_ir_adapter.py`
- CH 残差构造：`src/residual_analyzer.py::camassa_holm_residual`
- 策略验证：`src/strategy_validator.py::validate_strategy`
- 规则注册表：`src/symbolic_rule_registry.py`
- 现有执行器：`src/symbolic_executor.py::execute_strategy`
- 三指数 CH 分组和系数提取：`src/grouping_validator.py`、`src/coefficient_extractor.py`、`src/term_serializer.py`
- 三指数 CH 代数求解：`src/algebraic_solver.py`
- 原始 PDE 验证：`src/original_pde_verifier.py`

注意：现有 `coefficient_extractor.py` 写死为对 `x, t, q1, q2, q3` 做 `sp.Poly` 单项式提取。它只能处理已经被形式化为独立单项式的指数网络，不能直接处理 `sinh/cosh`、`sin/cos`、嵌套激活或未知生成元。新实现不能简单把这段代码复制进 Phase 1.5 执行器。

## 必须实现的内容

### 1. 策略字段真实驱动执行

在 `src/symbolic_executor.py` 或新增的执行模块中，让以下字段产生实际行为：

- `generators`：候选生成元必须映射到真实 IR 节点或表达式；
- `collection_strategy`：决定残差整理方式；
- `rewrite_strategy`：决定恒等重写的顺序；
- `intermediate_variables`：映射到 IR 节点，并在系数提取前用作命名中间量；
- `expected_structure`：只用于审计对比，不得替代实际 SymPy 结果；
- `selected_identity_rules`：继续通过规则注册表执行并做等价性校验；
- `selected_derivative_rules`：明确其执行角色。实际微分仍用 SymPy `diff`，但如果该字段只作为策略元数据，也必须在返回中说明“未参与数值微分”。

### 2. 确定性系数提取器

实现一个受限但正确的系数提取器，初始支持：

- 单层 exp 网络，即 `exp(w*x + v*t)` 可通过 `q_i = exp(w_i*x + v_i*t)` 替换为形式单项式；
- 单层或已通过等价重写转换为上述形式的结构；
- `sinh/cosh`、`sin/cos` 的指数或恒等重写必须通过等价性验证后才可用于生成元替换。

对无法证明代数独立性的生成元，必须返回 `unknown`，不得强行生成约束。这个判断是数学正确性要求，不是可选优化。

### 3. 端到端返回结构

`execute_strategy()` 的返回必须新增或改为包含：

- `coefficient_equations`：提取出的系数约束；
- `collection_status`：整理是否成功、生成元是否独立、哪些步骤被复杂度保护跳过；
- `algebraic_result`：在系数方程可解时，调用代数求解后的结果；
- `original_pde_verification`：对候选分支代回原始 CH 残差的验证结果；
- `strategy_consumption`：每个策略字段是否被执行、跳过或标记为审计用途。

### 4. 保持现有 Phase 1.5 指标兼容

`benchmark_runner.py` 和 `evaluation_metrics.py` 的原有统计字段不要丢失。可以新增字段，但原有 `compile_status`、`residual_terms`、`common_term_grouping` 等字段应继续存在或提供等价的兼容字段。

## 验收标准

### 验收 1：三指数 CH 回归

运行现有三指数 CH 实验，必须仍然通过：

- 提取 9 条系数约束；
- Maple 已知分支满足全部约束；
- 代回原始 CH 残差为 0；
- 代数分支集合中不存在硬编码分支。

### 验收 2：策略驱动路径与传统路径一致

对 Level 1 的 exp 网络，在不需要真实 API 的前提下，用固定策略走通新的策略驱动执行器，并得到与传统 `run_experiment.py` 三指数流程等价的系数方程。

### 验收 3：不支持生成元返回 unknown

对包含 `sinh/cosh`、`sin/cos`、`weierstrass` 或嵌套结构的案例，如果当前规则无法证明生成元独立性，执行器必须返回明确的 `unknown` 或 `unsupported`，不能返回伪系数方程。

### 验收 4：测试通过

新增确定性测试，不调用 LLM API：

- 策略字段消费测试；
- 系数提取等价性测试；
- 生成元独立性失败测试；
- 原始 PDE 验证测试；
- 历史三指数回归测试。

全部测试运行：

```bash
cd /Users/kang/SIGS
python3 -m pytest experiments/llm_ch_symbolic/tests -q
```

## 交付物

1. 修改后的实现代码和测试；
2. 新增执行结果输出文件，放在独立目录，例如 `experiments/llm_ch_symbolic/results/phase15_strategy_execution/`；
3. 一段简短实现说明，列出每个策略字段的最终执行语义；
4. 不覆盖任何历史结果。

## 审查协议

“11.23”完成实现后，将代码 diff 和测试结果交给当前审计线程。当前审计线程只做以下事情：

- 检查是否遵守本任务书范围和禁止项；
- 审查数学等价性、生成元独立性和零因子分支处理；
- 运行测试；
- 给出逐条验收结论和修改建议。

实现线程负责修改代码，审计线程不直接修改代码。
