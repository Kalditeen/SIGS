#!/usr/bin/env python3
"""Re-run only the symbolic execution stage for already-saved Phase 1.5 runs.

This preserves raw LLM API requests/responses and re-evaluates
``symbolic_executor`` after executor/rule-registry fixes. It never calls the
LLM API and only rewrites result files inside ``results/phase15/``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import benchmark_generator, symbolic_executor  # noqa: E402
from src.network_ir_adapter import NetworkIR  # noqa: E402


def _write_json(path: Path, payload) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )


def main() -> int:
    output_root = ROOT / "results" / "phase15"
    total_executions = 0
    for level in (1, 2, 3, 4):
        level_dir = output_root / f"level{level}"
        for case_dir in sorted((level_dir / "cases").iterdir()):
            ir_path = case_dir / "network_ir.json"
            if not ir_path.exists():
                continue
            ir = NetworkIR.from_dict(json.loads(ir_path.read_text(encoding="utf-8")))

            _write_json(
                case_dir / "traditional_result.json",
                symbolic_executor.execute_traditional(ir),
            )
            _write_json(
                case_dir / "manual_result.json",
                symbolic_executor.execute_manual(ir),
            )

            repeats_path = case_dir / "llm_repeats.json"
            if not repeats_path.exists():
                continue
            repeats = json.loads(repeats_path.read_text(encoding="utf-8"))
            for repeat in repeats:
                validation = repeat.get("strategy_validation") or {}
                if not validation.get("ok"):
                    continue
                repeat["execution"] = symbolic_executor.execute_strategy(
                    ir, validation.get("normalized")
                )
                total_executions += 1
            _write_json(repeats_path, repeats)

    print(f"reexecuted {total_executions} validated LLM strategies")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
