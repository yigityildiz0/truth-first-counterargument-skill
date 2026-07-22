#!/usr/bin/env python3
"""Heuristic consistency check for evidence-ledger confidence estimates.

This tool does not discover facts and does not produce a statistical posterior.
It converts already-audited evidence metadata into a bounded, explainable
estimate so repeated case-file updates use the same anchors.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


VALID_STANCES = {"supports", "contradicts", "mixed", "context"}
RANGES = {
    "source_quality": (0, 4),
    "directness": (0, 4),
    "relevance": (0, 3),
    "transparency": (0, 3),
    "materiality": (0, 3),
}
TRACKING_QUERY_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid"}


def _bounded_number(value: Any, field: str, index: int) -> float:
    low, high = RANGES[field]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"evidence[{index}].{field} must be numeric")
    number = float(value)
    if not math.isfinite(number) or number < low or number > high:
        raise ValueError(
            f"evidence[{index}].{field} must be between {low} and {high}"
        )
    return number


def _weight(item: dict[str, Any], index: int) -> float:
    quality = _bounded_number(item.get("source_quality", 0), "source_quality", index)
    directness = _bounded_number(item.get("directness", 0), "directness", index)
    relevance = _bounded_number(item.get("relevance", 0), "relevance", index)
    transparency = _bounded_number(item.get("transparency", 0), "transparency", index)
    materiality = _bounded_number(item.get("materiality", 0), "materiality", index)
    return (
        1
        + 3 * quality
        + 3 * directness
        + 2 * relevance
        + transparency
        + 2 * materiality
    )


def _direction(item: dict[str, Any], index: int) -> float:
    stance = item.get("stance")
    if stance not in VALID_STANCES:
        allowed = ", ".join(sorted(VALID_STANCES))
        raise ValueError(f"evidence[{index}].stance must be one of: {allowed}")
    if stance == "supports":
        return 1.0
    if stance == "contradicts":
        return -1.0
    if stance == "context":
        return 0.0
    mixed = item.get("mixed_direction", 0.0)
    if isinstance(mixed, bool) or not isinstance(mixed, (int, float)):
        raise ValueError(f"evidence[{index}].mixed_direction must be numeric")
    mixed = float(mixed)
    if not math.isfinite(mixed) or mixed < -1 or mixed > 1:
        raise ValueError(
            f"evidence[{index}].mixed_direction must be between -1 and 1"
        )
    return mixed


def _round_to_five(value: float) -> int:
    return int(math.floor((value + 2.5) / 5.0) * 5)


def _canonical_url(value: Any) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    parts = urlsplit(raw)
    if not parts.scheme or not parts.netloc:
        return raw.casefold()
    query = [
        (key, item_value)
        for key, item_value in parse_qsl(parts.query, keep_blank_values=True)
        if key.casefold() not in TRACKING_QUERY_KEYS
        and not key.casefold().startswith("utm_")
    ]
    path = parts.path.rstrip("/") or "/"
    return urlunsplit(
        (
            parts.scheme.casefold(),
            parts.netloc.casefold(),
            path,
            urlencode(query, doseq=True),
            "",
        )
    )


def _band(score: int) -> str:
    if score >= 85:
        return "strongly supported"
    if score >= 65:
        return "mostly supported"
    if score >= 55:
        return "weakly supported"
    if score >= 45:
        return "unresolved or mixed"
    if score >= 35:
        return "weakly unsupported"
    if score >= 15:
        return "mostly unsupported"
    return "strongly unsupported"


def _route(score: int) -> str:
    if score >= 85:
        return "concede the core claim; challenge only a proven material overreach"
    if score >= 65:
        return "concede and narrow"
    if score >= 45:
        return "clarify, ask the decisive question, or mark unresolved"
    if score >= 20:
        return "rebut the load-bearing weakness with calibrated language"
    return "strong rebuttal is evidence-supported"


def score_case(payload: dict[str, Any], claim_id: str | None = None) -> dict[str, Any]:
    evidence = payload.get("evidence", [])
    if not isinstance(evidence, list):
        raise ValueError("evidence must be a list")

    selected: list[tuple[int, dict[str, Any]]] = []
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            raise ValueError(f"evidence[{index}] must be an object")
        claim_ids = item.get("claim_ids", [])
        if claim_id is None or claim_id in claim_ids:
            selected.append((index, item))

    warnings: list[str] = []
    if not selected:
        warnings.append("No evidence items matched; 50 means unresolved, not half true.")

    groups: dict[str, list[tuple[float, float, dict[str, Any]]]] = defaultdict(list)
    seen_urls: dict[str, str] = {}

    for index, item in selected:
        weight = _weight(item, index)
        direction = _direction(item, index)
        group = str(item.get("independence_group", "")).strip()
        if not group:
            if direction != 0:
                raise ValueError(
                    f"evidence[{index}].independence_group is required for "
                    "directional evidence"
                )
            group = "__unknown_context_origin"
            warnings.append(
                f"Evidence {item.get('id', index)} has no independence_group; "
                "kept as non-directional context only."
            )

        url = _canonical_url(item.get("url", ""))
        if url:
            prior_group = seen_urls.get(url)
            if prior_group is not None and prior_group != group:
                warnings.append(
                    f"The same canonical URL appears in multiple independence groups; "
                    f"merged into {prior_group}: {url}"
                )
                group = prior_group
            else:
                seen_urls[url] = group
        groups[group].append((weight, direction, item))

    group_contributions: dict[str, float] = {}
    for group, entries in groups.items():
        signed_total = sum(weight * direction for weight, direction, _ in entries)
        cap = max((weight for weight, _, _ in entries), default=0.0)
        group_contributions[group] = max(-cap, min(cap, signed_total))

    directional = [value for value in group_contributions.values() if value != 0]
    directional_group_count = len(directional)
    support = sum(value for value in directional if value > 0)
    contradiction = -sum(value for value in directional if value < 0)

    group_quality: list[float] = []
    group_directness: list[float] = []
    group_relevance: list[float] = []
    high_direct_group_count = 0
    directional_stances: set[str] = set()
    for group, contribution in group_contributions.items():
        if contribution == 0:
            continue
        directional_stances.add("supports" if contribution > 0 else "contradicts")
        entries = groups[group]
        aligned = [
            entry for entry in entries if entry[1] * contribution > 0
        ] or entries
        _, _, representative = max(
            aligned, key=lambda entry: entry[0] * abs(entry[1])
        )
        quality = float(representative.get("source_quality", 0))
        directness = float(representative.get("directness", 0))
        relevance = float(representative.get("relevance", 0))
        group_quality.append(quality)
        group_directness.append(directness)
        group_relevance.append(relevance)
        if quality >= 3 and directness >= 3:
            high_direct_group_count += 1

    if support + contradiction == 0:
        raw = 50.0
    else:
        raw = 50.0 + 50.0 * (support - contradiction) / (
            support + contradiction + 20.0
        )

    if directional_group_count == 0:
        lower, upper = 50.0, 50.0
    elif directional_group_count == 1:
        lower, upper = 35.0, 65.0
    elif directional_group_count == 2:
        lower, upper = 20.0, 80.0
    else:
        lower, upper = 5.0, 95.0

    if directional_group_count == 0 and selected:
        warnings.append("No directional evidence matched; 50 means unresolved, not half true.")

    if directional_group_count > 0 and high_direct_group_count == 0:
        lower, upper = max(lower, 30.0), min(upper, 70.0)
        warnings.append(
            "No independent directional origin is both high-quality and direct; "
            "estimate was capped."
        )

    if group_relevance and max(group_relevance) < 2:
        lower, upper = max(lower, 35.0), min(upper, 65.0)
        warnings.append(
            "All independent directional origins have weak claim relevance; "
            "estimate was capped."
        )

    if directional_group_count >= 2 and len(directional_stances) < 2:
        warnings.append(
            "The ledger contains only one directional stance; run a disconfirmation search."
        )

    bounded = max(lower, min(upper, raw))
    score = max(5, min(95, _round_to_five(bounded)))

    avg_quality = sum(group_quality) / len(group_quality) if group_quality else 0.0
    avg_directness = (
        sum(group_directness) / len(group_directness) if group_directness else 0.0
    )
    if (
        directional_group_count >= 3
        and high_direct_group_count >= 2
        and avg_quality >= 2.5
        and avg_directness >= 2.5
    ):
        research_confidence = "high"
    elif directional_group_count >= 2 and avg_quality >= 1.5:
        research_confidence = "medium"
    else:
        research_confidence = "low"

    return {
        "claim_id": claim_id,
        "truth_estimate_percent": score,
        "evidence_band": _band(score),
        "research_confidence": research_confidence,
        "recommended_route": _route(score),
        "support_weight": round(support, 2),
        "contradiction_weight": round(contradiction, 2),
        "independent_directional_origins": directional_group_count,
        "high_quality_direct_origins": high_direct_group_count,
        "coverage_bounds": [int(lower), int(upper)],
        "warnings": list(dict.fromkeys(warnings)),
        "disclaimer": (
            "Heuristic consistency check only; not a statistical probability. "
            "Source interpretation, claim decomposition, and adversarial review control the verdict."
        ),
    }


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calibrate a truth estimate from an audited case-file evidence ledger."
    )
    parser.add_argument("case_file", type=Path, help="Path to the case-file JSON")
    parser.add_argument("--claim-id", help="Score only evidence linked to this atomic claim")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv or sys.argv[1:])
    try:
        payload = json.loads(args.case_file.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("case file root must be an object")
        result = score_case(payload, args.claim_id)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
