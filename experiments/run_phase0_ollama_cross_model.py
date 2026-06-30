#!/usr/bin/env python3
"""Phase-0-only cross-model validation via local Ollama (Llama/Qwen/etc.).

Lightweight: only runs agent selection (Tier 1-3), not the full 5-phase pipeline.
Typical runtime: ~3-5 min/case on GPU server, ~15-20 min on CPU.

Usage:
  uv run python experiments/run_phase0_ollama_cross_model.py --model llama3.1:8b
  uv run python experiments/run_phase0_ollama_cross_model.py --model qwen3.5:9b --think
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean, pstdev
from typing import Any

import httpx

from openre_bench.pipeline.phase0 import Phase0Config, run_phase0

CASES_DIR = Path("data/case_studies")
GROUND_TRUTH = Path("experiments/ground_truth/domain_relevance.json")
OUTPUT_DIR = Path("experiments/results/phase0_cross_model")
SEEDS = (101, 202, 303)
OLLAMA_HOST = "http://localhost:11434"


class OllamaLLMClient:
    """Native Ollama HTTP client with think=false support for Qwen3."""

    def __init__(self, model: str, *, host: str = OLLAMA_HOST, think: bool = False) -> None:
        self.model = model
        self.host = host.rstrip("/")
        self.think = think
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
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "think": self.think,
            "options": {"temperature": temperature},
        }
        if max_tokens is not None:
            payload["options"]["num_predict"] = max_tokens
        if seed is not None:
            payload["options"]["seed"] = int(seed)

        with httpx.Client(timeout=600.0) as client:
            resp = client.post(f"{self.host}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()

        message = data.get("message", {})
        content = str(message.get("content", "")).strip()
        if not content and message.get("thinking"):
            content = str(message.get("thinking", "")).strip()

        self.last_token_usage = {
            "input_tokens": int(data.get("prompt_eval_count", 0) or 0),
            "output_tokens": int(data.get("eval_count", 0) or 0),
            "total_tokens": int(data.get("prompt_eval_count", 0) or 0)
            + int(data.get("eval_count", 0) or 0),
        }
        return content


def load_cases(case_filter: list[str] | None) -> list[tuple[str, Path]]:
    cases: list[tuple[str, Path]] = []
    for path in sorted(CASES_DIR.glob("*_input.json")):
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


def check_ollama(model: str, host: str) -> None:
    with httpx.Client(timeout=30.0) as client:
        resp = client.get(f"{host.rstrip('/')}/api/tags")
        resp.raise_for_status()
        names = {m.get("name", "") for m in resp.json().get("models", [])}
    available = names | {n.split(":")[0] for n in names}
    if model not in names and model not in available and f"{model}:latest" not in names:
        print(f"Model '{model}' not found. Available: {sorted(names)}")
        print(f"Pull with: ollama pull {model}")
        raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase-0 cross-model via Ollama")
    parser.add_argument("--model", default="llama3.1:8b", help="Ollama model tag")
    parser.add_argument("--host", default=OLLAMA_HOST, help="Ollama API base URL")
    parser.add_argument("--think", action="store_true", help="Enable thinking mode (Qwen3)")
    parser.add_argument("--cases", nargs="*", help="Case IDs to run (default: all)")
    parser.add_argument("--seeds", nargs="*", type=int, default=list(SEEDS))
    parser.add_argument("--tier1-threshold", type=float, default=0.6)
    args = parser.parse_args()

    model_label = args.model.replace(":", "_").replace("/", "_")
    out_root = OUTPUT_DIR / model_label
    out_root.mkdir(parents=True, exist_ok=True)

    check_ollama(args.model, args.host)
    gt_map = {
        k: set(v["relevant_agents"])
        for k, v in json.loads(GROUND_TRUTH.read_text()).items()
    }
    cases = load_cases(args.cases)
    client = OllamaLLMClient(args.model, host=args.host, think=args.think)

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
            seed_metrics.append(metrics)
            print(f"  -> DFS={metrics['dfs']:.2f} agents={int(metrics['n_agents'])}")

        row = {
            "model": args.model,
            "case_id": case_id,
            "runs": len(seed_metrics),
            "dfs_mean": mean(m["dfs"] for m in seed_metrics),
            "dfs_std": pstdev(seed_metrics) if len(seed_metrics) > 1 else 0.0,
            "asp_mean": mean(m["asp"] for m in seed_metrics),
            "asr_mean": mean(m["asr"] for m in seed_metrics),
            "n_agents_mean": mean(m["n_agents"] for m in seed_metrics),
        }
        summary_rows.append(row)

    summary_path = out_root / "phase0_cross_model_summary.json"
    summary_path.write_text(json.dumps(summary_rows, indent=2) + "\n")

    print("\n=== Summary ===")
    for row in summary_rows:
        print(
            f"{row['case_id']:12s} DFS={row['dfs_mean']:.2f} "
            f"ASP={row['asp_mean']:.2f} ASR={row['asr_mean']:.2f} "
            f"|AG*|={row['n_agents_mean']:.1f}"
        )
    avg_dfs = mean(r["dfs_mean"] for r in summary_rows)
    print(f"\nAverage DFS: {avg_dfs:.2f}")
    print(f"Saved: {summary_path}")


if __name__ == "__main__":
    main()
