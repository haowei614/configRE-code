#!/usr/bin/env python3
"""Phase-0-only cross-model validation via Anthropic Claude (through LiteLLM).

Mirrors ``run_phase0_ollama_cross_model.py`` so the three backbones
(OpenAI GPT, local Ollama open-weight, Anthropic Claude) share one protocol,
ground truth, and output layout. Only runs agent selection (Tier 1-3), not the
full 5-phase pipeline, matching the GPT-4o cross-model setup reported in the paper.

Usage:
  uv run python experiments/run_phase0_claude_cross_model.py
  uv run python experiments/run_phase0_claude_cross_model.py --model claude-opus-4-5-20251101
  uv run python experiments/run_phase0_claude_cross_model.py --cases AD ATM
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from statistics import mean, pstdev
from typing import Any

from openre_bench.pipeline.phase0 import Phase0Config, run_phase0

CASES_DIR = Path("data/case_studies")
GROUND_TRUTH = Path("experiments/ground_truth/domain_relevance.json")
OUTPUT_DIR = Path("experiments/results/phase0_cross_model")
ENV_FILE = Path(".env")
SEEDS = (101, 202, 303)
DEFAULT_MODEL = "claude-sonnet-4-5-20250929"


def _load_anthropic_key() -> None:
    """Populate ANTHROPIC_API_KEY from the environment or a local .env file."""

    if os.environ.get("ANTHROPIC_API_KEY", "").strip():
        return
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        value = line.strip()
        if value.startswith("export "):
            value = value[7:].strip()
        if value.startswith("ANTHROPIC_API_KEY="):
            os.environ["ANTHROPIC_API_KEY"] = value.split("=", 1)[1].strip().strip('"').strip("'")
            return


class AnthropicLLMClient:
    """LiteLLM-backed Claude client matching the pipeline LLMContract.

    Anthropic has no ``seed`` parameter; LiteLLM's ``drop_params`` discards it so
    the shared pipeline call signature stays intact (runs are near-deterministic
    at temperature 0.0).
    """

    def __init__(self, model: str) -> None:
        self.model = model if model.startswith("anthropic/") else f"anthropic/{model}"
        self.last_token_usage: dict[str, int] = {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
        }

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.0,
        max_tokens: int | None = None,
        seed: int | None = None,
    ) -> str:
        import litellm

        litellm.drop_params = True
        request: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "timeout": 600.0,
            "num_retries": 2,
        }
        if max_tokens is not None:
            request["max_tokens"] = max_tokens
        if seed is not None:
            request["seed"] = int(seed)

        response = litellm.completion(**request)
        content = str(response.choices[0].message.content or "").strip()

        usage = getattr(response, "usage", None)
        prompt_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
        completion_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
        total_tokens = int(getattr(usage, "total_tokens", 0) or 0) or (
            prompt_tokens + completion_tokens
        )
        self.last_token_usage = {
            "input_tokens": prompt_tokens,
            "output_tokens": completion_tokens,
            "total_tokens": total_tokens,
        }
        return content


def load_cases(case_filter: list[str] | None) -> list[tuple[str, Path]]:
    cases: list[tuple[str, Path]] = []
    for path in sorted(CASES_DIR.glob("*_input.json")):
        if path.name.startswith("._"):
            continue
        case_id = path.stem.replace("_input", "")
        if case_filter and case_id not in case_filter:
            continue
        cases.append((case_id, path))
    return cases


def compute_dfs(activated: list[str], gt: set[str]) -> dict[str, float]:
    act = set(activated)
    rel = act & gt
    precision = len(rel) / len(act) if act else 0.0
    recall = len(rel) / len(gt) if gt else 0.0
    dfs = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return {"asp": precision, "asr": recall, "dfs": dfs, "n_agents": float(len(act))}


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase-0 cross-model via Anthropic Claude")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Claude model id")
    parser.add_argument("--cases", nargs="*", help="Case IDs to run (default: all)")
    parser.add_argument("--seeds", nargs="*", type=int, default=list(SEEDS))
    parser.add_argument("--tier1-threshold", type=float, default=0.6)
    args = parser.parse_args()

    _load_anthropic_key()
    if not os.environ.get("ANTHROPIC_API_KEY", "").strip():
        raise SystemExit("ANTHROPIC_API_KEY not found in environment or .env")

    model_label = args.model.replace(":", "_").replace("/", "_")
    out_root = OUTPUT_DIR / model_label
    out_root.mkdir(parents=True, exist_ok=True)

    gt_map = {
        k: set(v["relevant_agents"])
        for k, v in json.loads(GROUND_TRUTH.read_text()).items()
    }
    cases = load_cases(args.cases)
    client = AnthropicLLMClient(args.model)

    summary_rows: list[dict[str, Any]] = []
    for case_id, case_path in cases:
        case_data = json.loads(case_path.read_text())
        requirement = case_data.get("requirement", case_data.get("case_description", ""))
        seed_metrics: list[dict[str, float]] = []

        for seed in args.seeds:
            out_dir = out_root / case_id / f"seed_{seed}"
            out_file = out_dir / "phase0_agent_selection.json"
            if out_file.exists():
                print(f"SKIP {case_id} seed={seed}")
                payload = json.loads(out_file.read_text())
            else:
                print(f"RUN  {case_id} seed={seed} model={args.model}")
                out_dir.mkdir(parents=True, exist_ok=True)
                payload = run_phase0(
                    requirement,
                    Phase0Config(
                        tier1_threshold=args.tier1_threshold,
                        llm_client=client,
                        llm_model=args.model,
                        seed=seed,
                    ),
                )
                out_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")

            metrics = compute_dfs(payload.get("selected_agents", []), gt_map[case_id])
            usage = payload.get("token_usage") or {}
            metrics["input_tokens"] = float(usage.get("input_tokens", 0) or 0)
            metrics["output_tokens"] = float(usage.get("output_tokens", 0) or 0)
            metrics["total_tokens"] = float(usage.get("total_tokens", 0) or 0)
            seed_metrics.append(metrics)
            print(
                f"  -> DFS={metrics['dfs']:.2f} agents={int(metrics['n_agents'])} "
                f"tokens={int(metrics['total_tokens'])}"
            )

        row = {
            "model": args.model,
            "case_id": case_id,
            "runs": len(seed_metrics),
            "dfs_mean": mean(m["dfs"] for m in seed_metrics),
            "dfs_std": pstdev([m["dfs"] for m in seed_metrics]) if len(seed_metrics) > 1 else 0.0,
            "asp_mean": mean(m["asp"] for m in seed_metrics),
            "asr_mean": mean(m["asr"] for m in seed_metrics),
            "n_agents_mean": mean(m["n_agents"] for m in seed_metrics),
            "input_tokens_mean": mean(m["input_tokens"] for m in seed_metrics),
            "output_tokens_mean": mean(m["output_tokens"] for m in seed_metrics),
            "total_tokens_mean": mean(m["total_tokens"] for m in seed_metrics),
        }
        summary_rows.append(row)

    summary_path = out_root / "phase0_cross_model_summary.json"
    summary_path.write_text(json.dumps(summary_rows, indent=2) + "\n")

    print("\n=== Summary ===")
    for row in summary_rows:
        print(
            f"{row['case_id']:12s} DFS={row['dfs_mean']:.2f} "
            f"ASP={row['asp_mean']:.2f} ASR={row['asr_mean']:.2f} "
            f"|AG*|={row['n_agents_mean']:.1f} "
            f"tokens={row['total_tokens_mean']:.0f}"
        )
    avg_dfs = mean(r["dfs_mean"] for r in summary_rows)
    avg_tok = mean(r["total_tokens_mean"] for r in summary_rows)
    print(f"\nAverage DFS: {avg_dfs:.2f}")
    print(f"Average Phase0 tokens: {avg_tok:.0f}")
    print(f"Saved: {summary_path}")


if __name__ == "__main__":
    main()
