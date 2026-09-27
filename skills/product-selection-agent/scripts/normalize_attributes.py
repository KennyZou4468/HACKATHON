#!/usr/bin/env python3
"""Safe post-verification attribute normalisation.

This utility never invents facts or changes a Shopee MCP verdict.  It accepts
only an explicit source quote and normalises a small registry of unambiguous
number/unit spellings.  Its output may add ``normalized_verified`` evidence;
it must never turn a confirmed failure into a pass.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
import json
import re
import sys
from typing import Any


NUMBER = r"(?P<number>\d+(?:\.\d+)?)"
UNIT = r"(?P<unit>ml|l|mg|g|kg|w|kw|mb|gb|tb)\b"
MEASUREMENT = re.compile(NUMBER + r"\s*" + UNIT, re.IGNORECASE)
DIMENSIONS = re.compile(
    r"(?P<a>\d+(?:\.\d+)?)\s*(?:x|×)\s*"
    r"(?P<b>\d+(?:\.\d+)?)\s*(?:x|×)\s*"
    r"(?P<c>\d+(?:\.\d+)?)\s*(?P<unit>mm|cm|m)\b",
    re.IGNORECASE,
)
EXPLICIT_COUNT = re.compile(
    r"(?P<count>\d+)\s*(?:[-\s]?(?:pack|pcs?|pieces?|bottles?|cans?|units?))\b",
    re.IGNORECASE,
)
MULTIPLIER_COUNT = re.compile(r"(?P<count>\d+)\s*(?:x|×)\s*\d+(?:\.\d+)?\s*(?:ml|l|g|kg)\b", re.IGNORECASE)
CURRENCY = re.compile(r"(?:(?P<s>s\$)|(?P<sgd>sgd))\s*(?P<amount>\d+(?:\.\d{1,2})?)\b", re.IGNORECASE)
SHOE_SIZE = re.compile(r"\b(?P<system>us|uk|eu)\s*(?P<size>\d+(?:\.\d+)?)\b", re.IGNORECASE)

UNIT_BASE: dict[str, tuple[str, Decimal]] = {
    "ml": ("volume_ml", Decimal("1")),
    "l": ("volume_ml", Decimal("1000")),
    "mg": ("mass_g", Decimal("0.001")),
    "g": ("mass_g", Decimal("1")),
    "kg": ("mass_g", Decimal("1000")),
    "w": ("power_w", Decimal("1")),
    "kw": ("power_w", Decimal("1000")),
    "mb": ("storage_mb", Decimal("1")),
    "gb": ("storage_mb", Decimal("1024")),
    # Storage marketing conventions vary between decimal and binary prefixes.
    # TB is deliberately omitted rather than silently equating it to GB.
}


def decimal(value: Any) -> Decimal | None:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None
    return result if result.is_finite() else None


def comparable(left: Decimal, right: Decimal, operator: str) -> bool:
    return {
        "eq": left == right,
        "gte": left >= right,
        "lte": left <= right,
        "gt": left > right,
        "lt": left < right,
    }.get(operator, False)


def parse_quote(quote: str) -> list[dict[str, Any]]:
    facts: list[dict[str, Any]] = []
    for match in MEASUREMENT.finditer(quote):
        unit = match.group("unit").lower()
        if unit not in UNIT_BASE:
            continue
        kind, multiplier = UNIT_BASE[unit]
        value = decimal(match.group("number"))
        if value is not None:
            facts.append({"kind": kind, "value": str(value * multiplier), "quote": match.group(0)})
    for match in DIMENSIONS.finditer(quote):
        unit = match.group("unit").lower()
        multiplier = {"mm": Decimal("1"), "cm": Decimal("10"), "m": Decimal("1000")}[unit]
        values = [decimal(match.group(name)) for name in ("a", "b", "c")]
        if all(value is not None for value in values):
            facts.append({"kind": "dimensions_mm", "value": [str(value * multiplier) for value in values], "quote": match.group(0)})
    for pattern in (EXPLICIT_COUNT, MULTIPLIER_COUNT):
        for match in pattern.finditer(quote):
            facts.append({"kind": "pack_count", "value": match.group("count"), "quote": match.group(0)})
    for match in CURRENCY.finditer(quote):
        facts.append({"kind": "price_sgd", "value": match.group("amount"), "quote": match.group(0)})
    for match in SHOE_SIZE.finditer(quote):
        facts.append({"kind": "shoe_size", "system": match.group("system").upper(), "value": match.group("size"), "quote": match.group(0)})
    return facts


def target_kind(target: dict[str, Any]) -> tuple[str | None, Decimal | None, str | None]:
    """Return the registry key, canonical value, and optional named system."""
    unit = target.get("unit")
    value = decimal(target.get("value"))
    if value is None:
        return None, None, None
    if unit is None:
        return "pack_count", value, None
    normalized = str(unit).strip().lower().replace(" ", "")
    if normalized in {"bottle", "bottles", "pc", "pcs", "piece", "pieces", "can", "cans", "unit", "units", "pack", "packs"}:
        # A count requirement is compatible only with the explicit-count and
        # multiplier forms accepted above. It is never derived from `24s`.
        return "pack_count", value, None
    if normalized in UNIT_BASE:
        kind, multiplier = UNIT_BASE[normalized]
        return kind, value * multiplier, None
    if normalized in {"us", "uk", "eu"}:
        return "shoe_size", value, normalized.upper()
    if normalized in {"sgd", "s$"}:
        return "price_sgd", value, None
    return None, None, None


def audit(payload: dict[str, Any]) -> dict[str, Any]:
    requirements = payload.get("requirements")
    observations = payload.get("observations")
    if not isinstance(requirements, list) or not isinstance(observations, list):
        raise ValueError("requirements and observations must be arrays")
    facts: list[dict[str, Any]] = []
    for observation in observations:
        if not isinstance(observation, dict):
            continue
        quote = observation.get("quote")
        if isinstance(quote, str) and quote.strip():
            for fact in parse_quote(quote):
                fact["source_field"] = observation.get("field")
                facts.append(fact)

    results = []
    for requirement in requirements:
        if not isinstance(requirement, dict) or not isinstance(requirement.get("target"), dict):
            raise ValueError("each requirement needs a target object")
        target = requirement["target"]
        kind, expected, system = target_kind(target)
        result = {"id": requirement.get("id"), "status": "unknown", "reason": "unsupported_or_missing_explicit_evidence"}
        if kind is None or expected is None:
            results.append(result)
            continue
        operator = target.get("operator", "eq")
        matching = [fact for fact in facts if fact["kind"] == kind and (kind != "shoe_size" or fact.get("system") == system)]
        if not matching:
            results.append(result)
            continue
        values = [decimal(fact["value"]) for fact in matching]
        values = [value for value in values if value is not None]
        if any(comparable(value, expected, operator) for value in values):
            evidence = next(fact for fact in matching if decimal(fact["value"]) is not None and comparable(decimal(fact["value"]), expected, operator))
            result.update({"status": "normalized_verified", "reason": "deterministic_format_normalization", "evidence": evidence})
        elif operator in {"eq", "gte", "lte", "gt", "lt"}:
            result.update({"status": "not_met", "reason": "deterministic_normalized_comparison", "evidence": matching[0]})
        results.append(result)
    return {"results": results, "facts": facts}


def main() -> None:
    payload = json.load(sys.stdin)
    if payload.get("mode") != "audit":
        raise ValueError("mode must be audit")
    print(json.dumps(audit(payload), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        raise SystemExit(2)
