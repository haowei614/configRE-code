"""Phase 0: Domain-Adaptive Agent Configuration.

Three-tier agent selection:
  Tier 1 - ISO/IEC 25010 relevance scoring (LLM zero-shot)
  Tier 2 - Domain-specific standard activation (deterministic mapping)
  Tier 3 - Project-level constraint extraction (LLM-based)
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from openre_bench.llm import LLMClientError
from openre_bench.llm import LLMContract
from openre_bench.llm import chat_with_optional_seed
from openre_bench.pipeline._types import QUALITY_LENS_CUES
from openre_bench.schemas import AGENT_QUALITY_METADATA


DEFAULT_TIER1_THRESHOLD = 0.6
DEFAULT_PHASE0_MAX_TOKENS = 800
DEFAULT_PHASE0_SEED = 0

DOMAIN_AGENT_MAPPING: dict[str, list[str]] = {
    "automotive": ["FunctionalSafetyAgent"],
    "medical": ["FunctionalSafetyAgent"],
    "AI/ML": ["ExplainabilityAgent"],
    "financial": ["PrivacyAgent"],
    "government": ["PrivacyAgent"],
    "IoT/embedded": [],
    "web/enterprise": [],
    "telecommunications": [],
}

DOMAIN_ALIASES = {domain.lower(): domain for domain in DOMAIN_AGENT_MAPPING}


@dataclass
class Phase0Config:
    """Configuration for domain-adaptive agent selection."""

    tier1_threshold: float = DEFAULT_TIER1_THRESHOLD
    llm_model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = DEFAULT_PHASE0_MAX_TOKENS
    seed: int = DEFAULT_PHASE0_SEED
    llm_client: LLMContract | None = None


def tier1_relevance_scoring(
    project_description: str,
    tier1_agents: dict[str, dict[str, Any]],
    llm_caller: LLMContract | None,
    token_usage: dict[str, int] | None = None,
) -> dict[str, float]:
    """Score ISO/IEC 25010 candidate agents by project relevance."""

    scores: dict[str, float] = {}
    for agent_name, metadata in tier1_agents.items():
        characteristic_name = str(metadata.get("quality_dimension", agent_name))
        lens_phrase = _lens_phrase_for_characteristic(characteristic_name)
        prompt = (
            "You are a senior requirements engineer assessing quality attribute relevance "
            "for a specific project.\n"
            "Project Description:\n"
            f"{project_description}\n"
            f"Quality Characteristic: {characteristic_name}\n"
            f"Sub-characteristics: {lens_phrase}\n"
            "Assess whether this quality characteristic is a PRIMARY concern for this "
            'specific project -- not whether it is "nice to have" or "generally relevant '
            'to software engineering."\n'
            "Scoring criteria:\n\n"
            "1.0 = This is a critical, non-negotiable quality concern explicitly demanded "
            "by the project\n"
            "0.8 = This is a major concern strongly implied by the project domain and "
            "constraints\n"
            "0.5 = This is a secondary concern that may matter but is not a primary driver\n"
            "0.3 = This has minor or indirect relevance to this specific project\n"
            "0.0 = This is irrelevant to this project\n\n"
            "Domain-specific guidance:\n\n"
            "Safety is about preventing PHYSICAL harm to humans or the environment. "
            "Software that handles financial data, manages records, or processes "
            "transactions is NOT safety-critical even if data accuracy is important. "
            "Data accuracy is Reliability, not Safety.\n"
            "Performance is about response time, throughput, and resource utilization "
            "under load. Standard CRUD applications with moderate user counts are not "
            "performance-critical.\n\n"
            "Important: Most quality characteristics will score 0.3 or below for any given "
            "project. A typical project has 4-6 primary quality concerns, not 8-10. Be "
            "selective.\n"
            "Respond in JSON only, no markdown, no explanation outside JSON:\n"
            '{"relevance_score": <float>, "reasoning": "<one sentence explaining why this '
            'is or is not a primary concern>"}'
        )
        payload = _call_json(
            llm_caller,
            prompt,
            temperature=0.0,
            max_tokens=250,
            seed=DEFAULT_PHASE0_SEED,
            token_usage=token_usage,
        )
        score = _to_float(payload.get("relevance_score") if isinstance(payload, dict) else None)
        scores[agent_name] = _clamp01(score if score is not None else 0.0)
    return scores


def tier2_domain_activation(
    project_description: str,
    llm_caller: LLMContract | None,
    token_usage: dict[str, int] | None = None,
) -> tuple[list[str], list[str]]:
    """Detect application domains and activate deterministic domain-specific agents."""

    prompt = (
        "Identify the PRIMARY application domain of the following project. Select only "
        "domains that directly determine which regulatory standards and safety "
        "certifications apply to this system.\n"
        "Project Description:\n"
        f"{project_description}\n"
        "Available domains (select only those with direct regulatory implications for this "
        "project):\n\n"
        "automotive: Vehicle systems subject to ISO 26262 functional safety\n"
        "medical: Medical devices subject to IEC 62304\n"
        "financial: Financial systems subject to data protection regulations\n"
        "AI/ML: AI systems subject to EU AI Act transparency requirements (only if AI "
        "decision-making is the primary product, not if AI is merely used as an "
        "implementation technique)\n"
        "IoT/embedded: IoT devices with specific connectivity/resource constraints\n"
        "web/enterprise: Enterprise software systems\n"
        "government: Government systems with specific compliance requirements\n"
        "telecommunications: Telecom systems with specific regulations\n\n"
        'Important: An autonomous vehicle that uses AI internally is "automotive", not '
        '"AI/ML". A medical device that connects to the internet is "medical", not '
        '"IoT/embedded". Select the domain that determines the primary regulatory '
        "framework.\n"
        "Respond in JSON only:\n"
        '{"domains": ["<primary_domain>"], "reasoning": "<one sentence>"}'
    )
    payload = _call_json(
        llm_caller,
        prompt,
        temperature=0.0,
        max_tokens=250,
        seed=DEFAULT_PHASE0_SEED + 1,
        token_usage=token_usage,
    )

    detected_domains = _normalize_domains(payload.get("domains") if isinstance(payload, dict) else [])
    if not detected_domains:
        detected_domains = _heuristic_domain_detection(project_description)

    activated: list[str] = []
    for domain in detected_domains:
        for agent_name in DOMAIN_AGENT_MAPPING.get(domain, []):
            if agent_name not in activated:
                activated.append(agent_name)
    return activated, detected_domains


def tier3_constraint_extraction(
    project_description: str,
    all_agents: dict[str, dict[str, Any]],
    llm_caller: LLMContract | None,
    token_usage: dict[str, int] | None = None,
) -> tuple[list[str], list[dict[str, Any]]]:
    """Extract explicit project-level quality constraints and mapped agents."""

    agent_list = _agent_descriptions_for_prompt(all_agents)
    prompt = (
        "Extract specific quality-related constraints from the following project description. "
        "For each constraint, identify which quality agent is most relevant.\n"
        "Project Description:\n"
        f"{project_description}\n"
        "Available quality agents and their concerns:\n"
        f"{agent_list}\n"
        "IMPORTANT constraints on agent activation:\n\n"
        "FunctionalSafetyAgent: ONLY for systems where malfunction could cause physical "
        "harm to humans (vehicles, medical devices, industrial machinery, robotics). "
        "Software correctness, data integrity, and business rule enforcement do NOT "
        "qualify as functional safety. A bookkeeping system ensuring accurate "
        "calculations is Reliability, not Functional Safety.\n"
        "FlexibilityAgent: ONLY when the project explicitly requires deployment across "
        "multiple platforms, migration between environments, or runtime adaptability. "
        "Standard feature extensibility does not qualify.\n"
        "CompatibilityAgent: ONLY when the project explicitly requires integration with "
        "external systems, standards, or protocols. Internal data format handling (like "
        "multi-currency support) is Functional Suitability, not Compatibility.\n"
        "SafetyAgent: ONLY for systems where the software's behavior could lead to "
        "physical harm, environmental damage, or loss of life. Financial data accuracy "
        "is Reliability, not Safety.\n\n"
        "Only activate agents in Tier 3 that are NOT already covered by Tier 1 and "
        "Tier 2 selections. Do not duplicate activations.\n"
        "When in doubt about whether a constraint maps to a specialized agent, DO NOT "
        "activate that agent. It is better to miss a marginal agent than to activate "
        "an irrelevant one.\n"
        "Respond in JSON only:\n"
        '{"constraints": [\n'
        '{"constraint_text": "<exact phrase from description>", "agent_name": "<AgentName>", '
        '"priority": "high|medium|low", "reasoning": "<why this agent>"}\n'
        "]}\n"
        "Only extract constraints that are explicitly stated or strongly implied in the "
        "description. Do not invent constraints."
    )
    payload = _call_json(
        llm_caller,
        prompt,
        temperature=0.0,
        max_tokens=900,
        seed=DEFAULT_PHASE0_SEED + 2,
        token_usage=token_usage,
    )

    constraints = _normalize_constraints(
        payload.get("constraints") if isinstance(payload, dict) else [],
        all_agents=all_agents,
    )
    activated: list[str] = []
    for constraint in constraints:
        priority = str(constraint.get("priority", "")).strip().lower()
        agent_name = str(constraint.get("agent_name", "")).strip()
        if priority in {"high", "medium"} and agent_name and agent_name not in activated:
            activated.append(agent_name)
    return activated, constraints


def merge_selections(
    c1: list[str],
    c2: list[str],
    c3: list[str],
    tier1_scores: dict[str, float],
) -> list[str]:
    """Merge tier selections with stable ordering and no duplicates."""

    merged: list[str] = []
    for agent_name in [*c1, *c2, *c3]:
        if agent_name in tier1_scores or agent_name in AGENT_QUALITY_METADATA:
            if agent_name not in merged:
                merged.append(agent_name)
    return merged


def run_phase0(project_description: str, config: Any) -> dict[str, Any]:
    """Run three-tier domain-adaptive agent selection."""

    phase0_config = _coerce_phase0_config(config)
    all_agents = dict(AGENT_QUALITY_METADATA)
    token_usage = _empty_token_usage()
    tier1_agents = {
        agent_name: metadata
        for agent_name, metadata in all_agents.items()
        if str(metadata.get("tier", "")).strip().lower() in {"1", "tier 1", "tier1"}
    }

    tier1_scores = tier1_relevance_scoring(
        project_description,
        tier1_agents,
        phase0_config.llm_client,
        token_usage,
    )
    tier1_selected = [
        agent_name
        for agent_name, score in tier1_scores.items()
        if score >= phase0_config.tier1_threshold
    ]

    tier2_selected, tier2_domains = tier2_domain_activation(
        project_description,
        phase0_config.llm_client,
        token_usage,
    )

    tier3_candidates, tier3_constraints = tier3_constraint_extraction(
        project_description,
        all_agents,
        phase0_config.llm_client,
        token_usage,
    )
    already_selected = set(tier1_selected) | set(tier2_selected)
    tier3_selected = [
        agent_name for agent_name in tier3_candidates if agent_name not in already_selected
    ]

    selected_agents = merge_selections(
        tier1_selected,
        tier2_selected,
        tier3_selected,
        tier1_scores,
    )

    return {
        "selected_agents": selected_agents,
        "tier1_scores": tier1_scores,
        "tier1_selected": tier1_selected,
        "tier2_domains": tier2_domains,
        "tier2_selected": tier2_selected,
        "tier3_constraints": tier3_constraints,
        "tier3_selected": tier3_selected,
        "tier1_threshold": phase0_config.tier1_threshold,
        "total_agents": len(selected_agents),
        "token_usage": token_usage,
    }


def _coerce_phase0_config(config: Any) -> Phase0Config:
    if isinstance(config, Phase0Config):
        return config
    return Phase0Config(
        tier1_threshold=float(
            getattr(config, "tier1_threshold", DEFAULT_TIER1_THRESHOLD)
            or DEFAULT_TIER1_THRESHOLD
        ),
        llm_model=str(getattr(config, "model", getattr(config, "llm_model", "gpt-4o-mini"))),
        temperature=float(getattr(config, "temperature", 0.7) or 0.7),
        max_tokens=int(getattr(config, "max_tokens", DEFAULT_PHASE0_MAX_TOKENS) or DEFAULT_PHASE0_MAX_TOKENS),
        seed=int(getattr(config, "seed", DEFAULT_PHASE0_SEED) or DEFAULT_PHASE0_SEED),
        llm_client=getattr(config, "llm_client", None),
    )


def _call_json(
    llm_caller: LLMContract | None,
    prompt: str,
    *,
    temperature: float,
    max_tokens: int,
    seed: int,
    token_usage: dict[str, int] | None = None,
) -> dict[str, Any]:
    if llm_caller is None:
        return {}

    messages = [
        {
            "role": "system",
            "content": "You return strict JSON only for OpenRE-Bench preprocessing.",
        },
        {"role": "user", "content": prompt},
    ]
    try:
        raw_text, _seed_applied = chat_with_optional_seed(
            llm_client=llm_caller,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            seed=seed,
        )
    except (LLMClientError, TypeError, ValueError, RuntimeError):
        return {}
    _add_token_usage(token_usage, _client_last_token_usage(llm_caller))

    try:
        payload = json.loads(_strip_json_markdown(raw_text))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _empty_token_usage() -> dict[str, int]:
    return {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}


def _add_token_usage(target: dict[str, int] | None, usage: dict[str, int]) -> None:
    if target is None:
        return
    for key in ("input_tokens", "output_tokens", "total_tokens"):
        target[key] = int(target.get(key, 0)) + int(usage.get(key, 0))


def _client_last_token_usage(llm_caller: LLMContract | None) -> dict[str, int]:
    usage = getattr(llm_caller, "last_token_usage", None)
    if not isinstance(usage, dict):
        return _empty_token_usage()
    return {
        "input_tokens": _to_int(usage.get("input_tokens")),
        "output_tokens": _to_int(usage.get("output_tokens")),
        "total_tokens": _to_int(usage.get("total_tokens")),
    }


def _strip_json_markdown(raw_text: str) -> str:
    text = str(raw_text or "").strip()
    fence_match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if fence_match:
        return fence_match.group(1).strip()
    return text


def _lens_phrase_for_characteristic(characteristic_name: str) -> str:
    cues = QUALITY_LENS_CUES.get(characteristic_name)
    if not cues:
        return "quality-attribute specific concerns"
    return ", ".join(cues)


def _normalize_domains(raw_domains: Any) -> list[str]:
    if isinstance(raw_domains, str):
        values = [raw_domains]
    elif isinstance(raw_domains, list):
        values = [str(item) for item in raw_domains]
    else:
        values = []

    domains: list[str] = []
    for value in values:
        domain = DOMAIN_ALIASES.get(value.strip().lower())
        if domain and domain not in domains:
            domains.append(domain)
    return domains


def _heuristic_domain_detection(project_description: str) -> list[str]:
    text = project_description.lower()
    domains: list[str] = []
    keyword_map = {
        "automotive": ("vehicle", "automotive", "autonomous driving", "iso 26262"),
        "medical": ("medical", "patient", "clinical", "healthcare"),
        "financial": ("bank", "account", "transaction", "atm", "financial"),
        "AI/ML": ("ai", "machine learning", "model", "prediction"),
        "IoT/embedded": ("embedded", "sensor", "device", "iot"),
        "web/enterprise": ("web", "enterprise", "application", "service"),
        "government": ("government", "public sector", "regulation"),
        "telecommunications": ("telecom", "network", "5g", "communication"),
    }
    for domain, keywords in keyword_map.items():
        if any(keyword in text for keyword in keywords):
            domains.append(domain)
    return domains


def _agent_descriptions_for_prompt(all_agents: dict[str, dict[str, Any]]) -> str:
    lines: list[str] = []
    for agent_name, metadata in sorted(all_agents.items()):
        quality_dimension = str(metadata.get("quality_dimension", agent_name))
        tier_description = str(metadata.get("tier_description", "quality concern"))
        lens_phrase = _lens_phrase_for_characteristic(quality_dimension)
        lines.append(
            f"- {agent_name}: {quality_dimension}; {tier_description}; concerns: {lens_phrase}"
        )
    return "\n".join(lines)


def _normalize_constraints(
    raw_constraints: Any,
    *,
    all_agents: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    if not isinstance(raw_constraints, list):
        return []

    normalized: list[dict[str, Any]] = []
    for item in raw_constraints:
        if not isinstance(item, dict):
            continue
        agent_name = str(item.get("agent_name", "")).strip()
        if agent_name not in all_agents:
            continue
        priority = str(item.get("priority", "")).strip().lower()
        if priority not in {"high", "medium", "low"}:
            priority = "medium"
        constraint_text = str(item.get("constraint_text", "")).strip()
        if not constraint_text:
            continue
        normalized.append(
            {
                "constraint_text": constraint_text,
                "agent_name": agent_name,
                "priority": priority,
                "reasoning": str(item.get("reasoning", "")).strip(),
            }
        )
    return normalized


def _to_float(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def _to_int(value: Any) -> int:
    if isinstance(value, bool) or value is None:
        return 0
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))
