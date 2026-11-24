"""Deterministic benchmark generation for the four Phase 1.5 levels."""

from __future__ import annotations

from itertools import count

from .network_ir_adapter import NetworkIR

SEED_LEVELS = {"1": 101, "2": 202, "3": 303, "4": 404}


def _make_names(prefix: str):
    counter = count(1)
    return lambda: f"{prefix}{next(counter)}"


def _make_exp_network(n: int, index: int) -> NetworkIR:
    w = _make_names("w")
    a = _make_names("wx")
    b = _make_names("wt")
    nodes = [
        {"id": "x", "op": "input", "symbol": "x", "inputs": []},
        {"id": "t", "op": "input", "symbol": "t", "inputs": []},
    ]
    parameters: list[str] = ["b4"]
    hidden_ids: list[str] = []
    for i in range(1, n + 1):
        amp = w()
        wx = a()
        wt = b()
        parameters.extend([amp, wx, wt])
        affine_id = f"a{i}"
        act_id = f"q{i}"
        nodes.append({
            "id": affine_id,
            "op": "affine",
            "inputs": ["x", "t"],
            "coeffs": {"x": wx, "t": wt},
        })
        nodes.append({
            "id": act_id,
            "op": "activation",
            "activation": "exp",
            "inputs": [affine_id],
        })
        hidden_ids.append(act_id)
    coeffs = {hidden_id: f"w{i + 1}" for i, hidden_id in enumerate(hidden_ids)}
    parameters.extend(coeffs.values())
    nodes.append({
        "id": "out",
        "op": "affine",
        "inputs": hidden_ids,
        "coeffs": coeffs,
        "bias": "b4",
    })
    return NetworkIR(
        network_id=f"level1_exp_{n}",
        level=1,
        signature=f"[2,{n},1]",
        input_vars=["x", "t"],
        parameters=parameters,
        nodes=nodes,
        output_node="out",
        reference={
            "family": "exponential",
            "n_exponentials": n,
            "seed_index": index,
        },
    )


def _make_single_layer_hetero(index: int) -> NetworkIR:
    choices = [
        ["exp", "sinh"],
        ["sin", "cos", "poly2"],
        ["sinh", "cosh", "tanh"],
        ["exp", "poly2", "sin", "cos"],
        ["tanh", "cosh", "sin"],
        ["poly2", "sinh", "cos"],
    ]
    activations = choices[index % len(choices)]
    nodes = [
        {"id": "x", "op": "input", "symbol": "x", "inputs": []},
        {"id": "t", "op": "input", "symbol": "t", "inputs": []},
    ]
    parameters: list[str] = ["b_out"]
    hidden_ids: list[str] = []
    w = _make_names(f"w{index + 1}")
    a = _make_names(f"a{index + 1}")
    b = _make_names(f"b{index + 1}")
    c = _make_names(f"c{index + 1}")
    for j, activation in enumerate(activations, start=1):
        wx = a()
        wt = b()
        bias = c()
        amp = w()
        parameters.extend([wx, wt, bias, amp])
        affine_id = f"z{index}_{j}"
        act_id = f"h{index}_{j}"
        nodes.append({
            "id": affine_id,
            "op": "affine",
            "inputs": ["x", "t"],
            "coeffs": {"x": wx, "t": wt},
            "bias": bias,
        })
        nodes.append({
            "id": act_id,
            "op": "activation",
            "activation": activation,
            "inputs": [affine_id],
        })
        hidden_ids.append(act_id)
    coeffs = {hidden_id: w() for hidden_id in hidden_ids}
    parameters.extend(coeffs.values())
    nodes.append({
        "id": "out",
        "op": "affine",
        "inputs": hidden_ids,
        "coeffs": coeffs,
        "bias": "b_out",
    })
    return NetworkIR(
        network_id=f"level2_hetero_{index + 1}",
        level=2,
        signature=f"[2,{len(activations)},1]",
        input_vars=["x", "t"],
        parameters=parameters,
        nodes=nodes,
        output_node="out",
        reference={"family": "heterogeneous_single_layer", "activations": activations},
    )


def _make_mlp(signature: list[int], activations: list[list[str]], index: int) -> NetworkIR:
    nodes = [
        {"id": "x", "op": "input", "symbol": "x", "inputs": []},
        {"id": "t", "op": "input", "symbol": "t", "inputs": []},
    ]
    parameters: list[str] = ["b_out"]
    prev_ids = ["x", "t"]
    hidden_size = len(signature) - 2
    for layer_index in range(hidden_size):
        size = signature[layer_index + 1]
        layer_acts = activations[layer_index]
        if len(layer_acts) != size:
            raise ValueError("activation list length must match hidden layer size")
        current_ids: list[str] = []
        for j in range(size):
            affine_id = f"a{index}_{layer_index}_{j}"
            act_id = f"h{index}_{layer_index}_{j}"
            coeffs = {}
            for i, input_id in enumerate(prev_ids):
                coeff_name = f"w{index}_{layer_index}_{j}_{i}"
                coeffs[input_id] = coeff_name
                parameters.append(coeff_name)
            bias_name = f"b{index}_{layer_index}_{j}"
            parameters.append(bias_name)
            nodes.append({
                "id": affine_id,
                "op": "affine",
                "inputs": prev_ids,
                "coeffs": coeffs,
                "bias": bias_name,
            })
            nodes.append({
                "id": act_id,
                "op": "activation",
                "activation": layer_acts[j],
                "inputs": [affine_id],
            })
            current_ids.append(act_id)
        prev_ids = current_ids

    output_coeffs = {}
    for i, input_id in enumerate(prev_ids):
        coeff_name = f"wo{index}_{i}"
        output_coeffs[input_id] = coeff_name
        parameters.append(coeff_name)
    nodes.append({
        "id": "out",
        "op": "affine",
        "inputs": prev_ids,
        "coeffs": output_coeffs,
        "bias": "b_out",
    })
    return NetworkIR(
        network_id=f"level3_mlp_{index}",
        level=3,
        signature="[" + ",".join(str(s) for s in signature) + "]",
        input_vars=["x", "t"],
        parameters=parameters,
        nodes=nodes,
        output_node="out",
        reference={"family": "multilayer_mlp", "layers": signature, "activations": activations},
    )


def _make_level3_cases() -> list[NetworkIR]:
    return [
        _make_mlp([2, 3, 1], [["exp", "sinh", "tanh"]], 1),
        _make_mlp([2, 1, 3, 1], [["tanh"], ["exp", "sinh", "cos"]], 2),
        _make_mlp([2, 2, 3, 1], [["sin", "cos"], ["exp", "sinh", "tanh"]], 3),
        _make_mlp([2, 2, 2, 1], [["sinh", "cosh"], ["sin", "cos"]], 4),
        _make_mlp([2, 1, 2, 1], [["poly2"], ["exp", "tanh"]], 5),
        _make_mlp([2, 2, 2, 2, 1], [["sinh", "cosh"], ["sin", "cos"], ["exp", "tanh"]], 6),
    ]


def _make_branch_network(index: int) -> NetworkIR:
    """Build a small multi-branch DAG with shared and nested activations."""
    nodes = [
        {"id": "x", "op": "input", "symbol": "x", "inputs": []},
        {"id": "t", "op": "input", "symbol": "t", "inputs": []},
    ]
    parameters: list[str] = ["b_out", "a0", "b0", "c0"]
    nodes.append({
        "id": "z_shared",
        "op": "affine",
        "inputs": ["x", "t"],
        "coeffs": {"x": "a0", "t": "b0"},
        "bias": "c0",
    })

    branch_outputs: list[str] = []

    def add_branch(prefix: str, activations: list[str], own_affine: bool) -> None:
        prev = "z_shared"
        if own_affine:
            wx = f"{prefix}_wx"
            wt = f"{prefix}_wt"
            bias = f"{prefix}_bias"
            parameters.extend([wx, wt, bias])
            affine_id = f"{prefix}_z"
            nodes.append({
                "id": affine_id,
                "op": "affine",
                "inputs": ["x", "t"],
                "coeffs": {"x": wx, "t": wt},
                "bias": bias,
            })
            prev = affine_id
        current = prev
        for pos, activation in enumerate(activations):
            act_id = f"{prefix}_act{pos}"
            nodes.append({
                "id": act_id,
                "op": "activation",
                "activation": activation,
                "inputs": [current],
            })
            current = act_id
        branch_outputs.append(current)

    if index == 1:
        add_branch("brA", ["exp"], False)
        add_branch("brB", ["sinh"], False)
    elif index == 2:
        add_branch("brA", ["cos"], False)
        add_branch("brB", ["poly2"], False)
    elif index == 3:
        add_branch("brA", ["exp"], False)
        add_branch("brB", ["sinh"], False)
        add_branch("brC", ["cos"], False)
    elif index == 4:
        add_branch("brA", ["sinh", "tanh"], True)
        add_branch("brB", ["poly2", "cos"], True)
    elif index == 5:
        add_branch("brA", ["exp"], False)
        add_branch("brB", ["sinh"], False)
        mul_id = "shared_mul"
        nodes.append({
            "id": mul_id,
            "op": "mul",
            "inputs": [branch_outputs[-2], branch_outputs[-1]],
        })
        branch_outputs.append(mul_id)
    else:
        add_branch("brA", ["exp"], False)
        add_branch("brB", ["weierstrass"], False)

    output_coeffs = {}
    for i, input_id in enumerate(branch_outputs):
        coeff_name = f"wo_{i}"
        output_coeffs[input_id] = coeff_name
        parameters.append(coeff_name)
    nodes.append({
        "id": "out",
        "op": "affine",
        "inputs": branch_outputs,
        "coeffs": output_coeffs,
        "bias": "b_out",
    })
    return NetworkIR(
        network_id=f"level4_branch_{index}",
        level=4,
        signature=f"branch_{index}",
        input_vars=["x", "t"],
        parameters=parameters,
        nodes=nodes,
        output_node="out",
        reference={"family": "multibranch_hybrid", "index": index},
    )


def generate_benchmarks(level: int | str) -> list[NetworkIR]:
    level = int(level)
    if level == 1:
        return [_make_exp_network(n, n) for n in [2, 3, 4, 5]]
    if level == 2:
        return [_make_single_layer_hetero(i) for i in range(6)]
    if level == 3:
        return _make_level3_cases()
    if level == 4:
        return [_make_branch_network(i) for i in range(1, 7)]
    raise ValueError(f"unsupported benchmark level {level!r}")
