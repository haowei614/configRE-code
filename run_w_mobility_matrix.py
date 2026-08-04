#!/usr/bin/env python3
"""Run the full W-Mobility comparison matrix (4 configs x 3 seeds) under QUARE.

Records per-run runtime and token usage; writes a rolling summary CSV/JSON.
"""
import json
import os
import time
from pathlib import Path

# Patch httpx default timeout before any OpenAI/litellm import.
os.environ.setdefault("HTTPX_TIMEOUT", "120")

import httpx

_TIMEOUT = httpx.Timeout(180.0, connect=15.0)
_orig_client_init = httpx.Client.__init__


def _patched_client_init(self, *args, **kwargs):
    kwargs.setdefault("timeout", _TIMEOUT)
    _orig_client_init(self, *args, **kwargs)


httpx.Client.__init__ = _patched_client_init

import litellm  # noqa: E402

litellm.request_timeout = 180

from openre_bench.pipeline import PipelineConfig  # noqa: E402
from openre_bench.pipeline._core import run_case_pipeline  # noqa: E402

CASE = Path("data/case_studies/W-Mobility_input.json")
MODEL = "gpt-4o-mini-2024-07-18"
SEEDS = [101, 202, 303]
OUTROOT = Path("experiment_outputs/w-mobility")
SUMMARY = OUTROOT / "w-mobility_run_summary.csv"

POOL_15 = [
    "SafetyAgent",
    "EfficiencyAgent",
    "PerformanceAgent",
    "ReliabilityAgent",
    "UsabilityAgent",
    "SecurityAgent",
    "MaintainabilityAgent",
    "CompatibilityAgent",
    "FlexibilityAgent",
    "TrustworthinessAgent",
    "FunctionalSafetyAgent",
    "ExplainabilityAgent",
    "PrivacyAgent",
    "GreenAgent",
    "ResponsibilityAgent",
]
FIXED_5 = [
    "SafetyAgent",
    "EfficiencyAgent",
    "GreenAgent",
    "TrustworthinessAgent",
    "ResponsibilityAgent",
]
DOMAIN_OPT = [
    "SafetyAgent",
    "PerformanceAgent",
    "EfficiencyAgent",
    "ReliabilityAgent",
    "UsabilityAgent",
    "FunctionalSafetyAgent",
    "PrivacyAgent",
]  # Aisin expert GT

CONFIGS = [
    ("fixed5", FIXED_5),
    ("full15", POOL_15),
    ("domainopt", DOMAIN_OPT),
    ("auto", "auto"),
]


def main():
    OUTROOT.mkdir(parents=True, exist_ok=True)
    rows = []
    if not SUMMARY.exists():
        SUMMARY.write_text(
            "config,seed,runtime_s,total_tokens,input_tokens,output_tokens,"
            "n_selected,artifacts_dir\n"
        )
    t_all = time.time()
    total_runs = len(CONFIGS) * len(SEEDS)
    idx = 0
    for cfg_name, cfg_val in CONFIGS:
        for seed in SEEDS:
            idx += 1
            run_id = f"w-mobility-{cfg_name}-s{seed}"
            adir = OUTROOT / cfg_name / f"seed_{seed}"
            adir.mkdir(parents=True, exist_ok=True)
            rr_path = adir / "run_record.json"
            if rr_path.exists() and (adir / "phase5_software_materials.json").exists():
                print(
                    f"[{idx}/{total_runs}] SKIP  {cfg_name} seed={seed} (already done)",
                    flush=True,
                )
                continue
            print(f"[{idx}/{total_runs}] START {cfg_name} seed={seed}", flush=True)
            t0 = time.time()
            pc = PipelineConfig(
                case_input=CASE,
                artifacts_dir=adir,
                run_record_path=adir / "run_record.json",
                run_id=run_id,
                setting="negotiation_integration_verification",
                seed=seed,
                model=MODEL,
                temperature=0.7,
                round_cap=3,
                max_tokens=4000,
                system="quare",
                rag_enabled=True,
                rag_backend="chroma",
                rag_corpus_dir=Path("data/knowledge_base"),
                agent_config=cfg_val,
                tier1_threshold=0.6,
            )
            try:
                run_case_pipeline(pc)
            except Exception as e:
                print(
                    f"[{idx}/{total_runs}] FAIL {cfg_name} seed={seed}: {e}",
                    flush=True,
                )
                continue
            dt = time.time() - t0
            rec = json.load(open(adir / "run_record.json"))
            tok = rec.get("token_usage", {}).get("total", {})
            try:
                sel = json.load(open(adir / "phase0_agent_selection.json")).get(
                    "selected_agents"
                )
                nsel = (
                    len(sel)
                    if sel
                    else (len(cfg_val) if isinstance(cfg_val, list) else None)
                )
            except Exception:
                nsel = len(cfg_val) if isinstance(cfg_val, list) else None
            line = (
                f"{cfg_name},{seed},{dt:.1f},{tok.get('total_tokens','')},"
                f"{tok.get('input_tokens','')},{tok.get('output_tokens','')},"
                f"{nsel},{adir}\n"
            )
            with open(SUMMARY, "a") as f:
                f.write(line)
            print(
                f"[{idx}/{total_runs}] DONE  {cfg_name} seed={seed} | "
                f"{dt:.1f}s | tokens={tok.get('total_tokens')} | agents={nsel}",
                flush=True,
            )
            rows.append(line)
    print(
        f"ALL DONE in {(time.time() - t_all) / 60:.1f} min. Summary: {SUMMARY}",
        flush=True,
    )


if __name__ == "__main__":
    main()
