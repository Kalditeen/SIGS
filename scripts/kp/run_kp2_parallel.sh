#!/usr/bin/env bash
set -uo pipefail

cd "$(dirname "$0")"

export PYTHONPATH="$(cd ../.. && pwd)/src${PYTHONPATH:+:${PYTHONPATH}}"

if [[ -x ../../.venv/bin/python ]]; then
    PYTHON="${PYTHON:-../../.venv/bin/python}"
else
    PYTHON="${PYTHON:-python}"
fi

# Space-separated structure suffixes.  Override with:
#   CASES="231 2321" ./run_kp2_parallel.sh

scripts=()
seeds=()

if [[ -n "${SCRIPT:-}" ]]; then
    # One script, many random seeds:
    #   SCRIPT=kp_nnsca_231.py SEEDS="42 43 44 45" ./run_kp2_parallel.sh
    for seed in ${SEEDS:-42 43 44 45}; do
        scripts+=("$SCRIPT")
        seeds+=("$seed")
    done
else
    # All KP-II structures in parallel:
    #   CASES="231 2321" SEED_START=42 ./run_kp2_parallel.sh
    CASES="${CASES:-2221 2231 231 2321 23211}"
    seed_start="${SEED_START:-42}"
    idx=0
    for case in $CASES; do
        script="kp_nnsca_${case}.py"
        if [[ ! -f "$script" ]]; then
            echo "missing script: $script" >&2
            continue
        fi
        scripts+=("$script")
        seeds+=("$((seed_start + idx))")
        idx=$((idx + 1))
    done
fi

if [[ ${#scripts[@]} -eq 0 ]]; then
    echo "no runnable KP-II scripts" >&2
    exit 1
fi

# Extra CLI args shared by every launched script, e.g.
#   EXTRA_ARGS="--n-samples 20 --screen-x 16 --screen-y 16 --screen-t 8" ...
if [[ -n "${EXTRA_ARGS:-}" ]]; then
    read -r -a extra_args <<< "$EXTRA_ARGS"
else
    extra_args=()
fi

pids=()
status=0
for i in "${!scripts[@]}"; do
    script="${scripts[$i]}"
    seed="${seeds[$i]}"
    echo "start $script seed=$seed"
    "$PYTHON" "$script" --seed "$seed" "${extra_args[@]}" &
    pids+=("$!")
done
for i in "${!pids[@]}"; do
    if wait "${pids[$i]}"; then
        echo "done ${scripts[$i]} seed=${seeds[$i]}"
    else
        echo "failed ${scripts[$i]} seed=${seeds[$i]}"
        status=1
    fi
done


exit "$status"
