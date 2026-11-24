#!/usr/bin/env python3
"""Unified entry point for the Phase 1.5 comparison experiments."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
if str(EXPERIMENT_ROOT) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT_ROOT))

from src import benchmark_runner, llm_client  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 1.5 LLM vs traditional benchmark")
    parser.add_argument("--level", type=str, default="1", help="1, 2, 3, 4, or all")
    parser.add_argument(
        "--method",
        choices=benchmark_runner.METHODS,
        default="all",
        help="which comparison method(s) to run",
    )
    parser.add_argument("--repeat", type=int, default=3, help="independent LLM repeats per case")
    parser.add_argument(
        "--config",
        type=Path,
        default=EXPERIMENT_ROOT / "config" / "llm_config.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=EXPERIMENT_ROOT / "results" / "phase15",
    )
    args = parser.parse_args(argv)

    levels = [1, 2, 3, 4] if args.level == "all" else [int(args.level)]
    config = None
    if args.method in ("llm", "all"):
        config = llm_client.load_config(args.config)
        if not config.is_configured:
            print(
                "LLM_API_NOT_CONFIGURED: set LLM_API_KEY or DEEPSEEK_API_KEY, "
                "or fill config/llm_config.json",
                file=sys.stderr,
            )
            return 2

    summaries = []
    for level in levels:
        print(f"running level {level} method={args.method} repeat={args.repeat}")
        stats = benchmark_runner.run_benchmarks(
            level=level,
            method=args.method,
            repeat=args.repeat,
            config=config,
            output_root=args.output_dir,
        )
        summaries.append(stats)

    print("phase15 run complete")
    for stats in summaries:
        print(
            f"level={stats['level']} cases={stats['case_count']} "
            f"traditional={len(stats['traditional'])} manual={len(stats['manual'])} "
            f"llm_repeats={sum(len(item['repeats']) for item in stats['llm_repeat_results'])}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
