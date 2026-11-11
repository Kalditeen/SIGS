#!/usr/bin/env bash
set -uo pipefail

cd "$(dirname "$0")"
PYTHON="${PYTHON:-python}"
export PYTHONPATH="$(cd ../.. && pwd)/src${PYTHONPATH:+:${PYTHONPATH}}"
SCRIPT="${SCRIPT:-ch_nnsca_2231.py}"

run_case() {
    local config_name="$1"
    shift
    echo "===== ${config_name} ====="
    if "$PYTHON" "$SCRIPT" "$@" > "ablation_${config_name}.log" 2>&1; then
        echo "  completed"
    else
        local status=$?
        echo "  failed with exit ${status} (see ablation_${config_name}.log)"
    fi
}

run_case only_seeds --only-seeds --ablation-seed 42
run_case no_seeds --no-seeds --ablation-seed 42 --ablation-topk 3
run_case with_seeds --ablation-seed 42 --ablation-topk 3

for cfg in only_seeds no_seeds with_seeds; do
    echo "===== ${cfg} summary ====="
    grep -E "ablation config|symbolic attempts|exact:|failed:|exact solution found|result:|total elapsed" \
        "ablation_${cfg}.log" || true
done
