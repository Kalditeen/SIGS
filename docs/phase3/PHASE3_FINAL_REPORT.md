# Phase 3 Final Report

**项目：** SIGS / SFG-NNSCA  
**阶段：** Phase 3 - 复杂网络自动求解与 Gardner 精确解搜索  
**结果：** 自动求解链路完整运行；基准回归通过；六类代表性网络已端到端测试；非行波结构与行波判别接口可用。

## 1. 结论摘要

| 问题 | 结论 |
|---|---|
| Phase 2 复杂网络能否进入 Stage2 | 能。所有代表候选都从 `NetworkIR` 重新编译并进入真实 `Stage2Adapter`。 |
| 哪些结构能成功求解 | 单节点 JacobiCN/JacobiSN/JacobiDN 均恢复为 `EXACT_VERIFIED`；复杂多节点代表候选本阶段未通过原始 PDE 验证。 |
| 哪些结构造成困难 | 多节点、异构激活、多层嵌套候选主要卡在约束提取或参数求解阶段。 |
| 求解失败主因 | 系数方程规模超过现有保护阈值，以及异构相位/嵌套复合导致约束系统过大或非多项式。 |
| 是否发现真正多节点精确解 | 否。所有已验证分支均退化为单节点解。 |
| 是否发现标准非行波精确解 | 否。非行波结构只建立了生成与判别基础，没有发现 `EXACT_VERIFIED` 的非行波分支。 |
| 不同随机种子是否有结构差异 | 是。三组 seed 的签名交集均为 0。 |
| Stage2 主要瓶颈 | 多节点/嵌套网络的系数提取和参数求解，而不是单个 Jacobi 函数的残差验证。 |
| 下一阶段优先方向 | 优先增强符号约束求解器，而不是盲目扩大网络搜索空间。 |

## 2. 各实验结果

### E1 基准回归

使用 `NetworkIR -> AnsatzCompiler -> Stage2Adapter -> gardner_residual` 的真实链路，对单节点 Jacobi 函数分别回归：

- `JacobiCN`: `EXACT_VERIFIED`
- `JacobiSN`: `EXACT_VERIFIED`
- `JacobiDN`: `EXACT_VERIFIED`

三个候选共得到 4 个验证分支，其中 JacobiDN 的两个相位符号分支均为同一函数族。结果保存在 `results/phase3_benchmark/`。

### E2 六类复杂网络

从 Phase 2 真实候选中选出 A-F 六类代表：

| 类别 | 候选 | 节点 | 深度 | 激活 |
|---|---|---|---|---|
| A 单节点 | candidate_0057 | 1 | 1 | tan |
| B 双节点异构 | candidate_0046 | 2 | 1 | sech, tanh |
| C 双分支汇合 | candidate_0002 | 5 | 2 | JacobiCN, exp, sech, square, tanh |
| D 双层 | candidate_0003 | 5 | 2 | JacobiCN, cosh, exp, identity, square |
| E 跳连 | candidate_0041 | 6 | 3 | JacobiCN, cosh, exp, identity, square, tanh |
| F 多 phase | candidate_0001 | 3 | 1 | cosh, identity, square |

结果：

- `CONSTRAINT_FAILED`: 5
- `VERIFICATION_FAILED`: 1
- `EXACT_VERIFIED`: 0

`candidate_0057` 单节点 tan 候选求解器返回了分支，但回代原始 Gardner 残差未恒等于零，因此保持 `VERIFICATION_FAILED`。其余候选主要因“coefficient solve system too large”而停在约束/求解阶段。完整表见 [PHASE3_COMPLEX_NETWORK_AUDIT.md](/Users/kang/SIGS/docs/phase3/PHASE3_COMPLEX_NETWORK_AUDIT.md)。

### E3 多 seed 搜索

seed = 101, 202, 303，每个生成 8 个候选，生成器配置一致：

- 三组生成候选均为 8 个唯一候选，无重复；
- 三组间结构签名交集均为 0；
- 每组编译成功 8/8；
- 每组挑 1 个最简候选进入 Stage2；
- seed 101: `VERIFICATION_FAILED`；
- seed 202: `CONSTRAINT_FAILED`；
- seed 303: 自动生成的单节点 `JacobiSN` 候选达到 `EXACT_VERIFIED`。

完整结果见 `results/phase3_multiseed/`。

### E4 非行波导向结构

四类模板均成功编译并进入 Stage2：

- `SPACE_TIME_SEPARATED`
- `SPACE_TIME_COMPOSITE`
- `MULTI_PHASE`
- `TRAVELING_WAVE_ORIENTED`

三类非行波结构在 Stage2 中未得到 `EXACT_VERIFIED` 分支，失败阶段已记录。结果见 [PHASE3_NONTRAVELING_ANALYSIS.md](/Users/kang/SIGS/docs/phase3/PHASE3_NONTRAVELING_ANALYSIS.md)。

### E5 退化分析

所有 `EXACT_VERIFIED` 分支经有效网络分析后均为 `DEGENERATE`（实际有效节点为单节点）。这说明当前已验证精确解没有真正利用多节点结构，不能据此宣称发现了双节点复合解。

### E6 标准行波判别

已对每个 `EXACT_VERIFIED` 分支执行 `u_t + c u_x = 0` 的符号判别：

- JacobiCN/JacobiSN/JacobiDN 基准解均为 `TRAVELING_WAVE_CONFIRMED`；
- `traveling_wave_baseline` 模板为 `TRAVELING_WAVE_CONFIRMED`；
- 三类非行波模板为 `NON_TRAVELING_WAVE_CANDIDATE`。

判别接口只做标准线性行波排除，不对一般变量变换下的等价性作结论。

## 3. 当前求解器瓶颈

主要瓶颈不是 PDE 残差验证，而是复杂网络进入系数提取和参数求解时：

1. 多节点和嵌套激活会产生大量未知参数和耦合项；
2. `_solve_equations` 对超过 200 个方程或 12 个未知数的系统直接返回“system too large”；
3. 异构函数组合的残差不是关于这些参数的简单多项式系统；
4. 系数提取对纸面模板 `(2-2-3-1)` 等嵌套结构可能超时。

这些是求解器能力边界，不是数学上不存在解的证明。

## 4. 测试结果

- 新增 Phase 3-A/B/C/D 测试：26 项全部通过；
- 全量回归（排除已知环境问题的 `tests/test_hf_data.py`）：`183 passed`；
- `tests/test_hf_data.py` 仍因 `pyarrow requires NumPy 2.0 or newer, found 1.26.4` 无法收集，单独记录，不计入代码测试通过数。

## 5. 下一阶段建议

下一阶段优先做有边界的符号求解器增强，而不是立即扩大网络搜索空间：

1. 对多节点网络先识别并求解线性子空间，再做非线性回代；
2. 增加可证明的函数微分代数恒等式接口，优先覆盖 `sech`、`tanh`、`tan` 和 Jacobi 函数；
3. 对非多项式系统明确记录不可直接使用 Groebner/多项式方法的原因；
4. 将系数提取的超时保护细化到每个候选阶段，保留中间残差和约束表达式。

不建议未经讨论直接启动 Phase 4 深层网络搜索。
