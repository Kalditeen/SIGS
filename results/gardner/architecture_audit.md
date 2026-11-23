# Gardner 架构适配审计

本报告只读检查当前 `SFG + NNSCA` 实现，不包含 Gardner 代码修改。结论基于 `/Users/kang/SIGS` 当前工作区。

## 1. 可直接复用的模块

- SFG 候选生成器：`scripts/pdes/sfg_bbm_21.py` 中的 `generate_candidates`、`_atom_pool`、`_random_entries`、`_exhaustive_entries`、`Candidate` 和 `_candidate_from_expr` 均与 PDE 无关。它们只生成一元函数 `f(z)`，不带 BBM 假设。
- NNSCA 网络构造：`build_trial` 支持 `[2,1]`、`[2,2,1]` 和深层 `[2,3,2,1]`。网络参数命名和仿射输入与前一个阶段一致，可直接用于 Gardner。
- 符号处理公共件：`_sympify_f`、`_extract_coefficient_equations`、`_normalise_residual`、`_solve_equations`、`_residual_is_zero`、`_solution_set_to_dicts`、Jacobi 椭圆函数支持均与 PDE 无关。
- 状态记录与等价性工具：`_classify_branch` 中单/双节点分支的基本判定可复用；`_solution_equivalence_key` 的 `(x,t) -> (-x,-t)` 反射等价逻辑可复用。
- 现有结果目录和 BBM 测试均保持不动。

## 2. BBM 特定假设

- `sfg_bbm_21.py` 中的 `_bbm_residual` 硬编码：
  `R = u_t + u_x + u*u_x - u_{xxt}`。
  这是当前最大 PDE 绑定点。
- `_process_candidate` 在残余计算、回代验证和 Maple 任务文本中直接调用 `_bbm_residual`。
- `_validate_branch` 直接调用 `_bbm_residual` 做最终原始 PDE 验证。
- `audit_exact_solution` 和 `_solution_notes` 的 BBM 特定注释只适用于 BBM，不能直接套到 Gardner。
- 报告模板中关于 `u_t+u_x+uu_x-u_{xxt}` 的固定文字也不能直接复用。

## 3. 网络结构是否可直接支持 Gardner

可以。`build_trial` 的输入输出结构与 PDE 无关。Gardner 只需要换残余函数。`[2,1]`、`[2,2,1]`、`[2,3,2,1]` 均无需修改数学定义。

## 4. 符号求解器能否处理三次非线性项

约束提取模块 `_extract_coefficient_equations` 把底层函数替换为独立基符号，然后按多项式系数提取约束。Gardner 的 `u^2 u_x` 会带来基符号三次项，但求解器面对的仍是关于网络参数的代数方程，因此机制上可以处理。主要风险是表达式规模和 `sp.solve` 分支增长；已有 `200` 方程上限和 `12` 未知数上限可以控制。

## 5. 残差验证机制能否正确验证 Gardner

可以，只要：
- Gardner 残余定义使用 `u_t + alpha*u*u_x + beta*u**2*u_x + gamma*u_{xxx}`；
- 最终验证调用 Gardner 的原始残余，而不是 `_bbm_residual`；
- 三次项写作 `u**2 * sp.diff(u, X)`，避免写成 `u * (u_x)**2`。

## 6. 建议的最小改动路径

1. 将 `_process_candidate` 和 `_validate_branch` 的残余函数参数化，默认仍为 `_bbm_residual`，保持 BBM 行为兼容。
2. 新增 `scripts/pdes/sfg_gardner.py`，复用 `sfg_bbm_21` 的生成器和网络构造。
3. 为 Gardner 实现独立残余函数、独立审核函数和独立报告输出。
4. 不修改 BBM 方程、网络结构或 SFG 函数原子库。
