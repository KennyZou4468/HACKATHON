#!/usr/bin/env python3
"""Build a small, deterministic marketplace search plan.

The plan broadens retrieval only.  It never proves a listing fact, changes a
hard requirement, or turns a result into a recommendation.
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any


SAFE_TEXT = re.compile(r"[^A-Za-z0-9 .+\-×x]", re.ASCII)
MEASUREMENT_UNITS = {"ml", "l", "mg", "g", "kg", "w", "kw", "mb", "gb", "tb", "hz", "cm", "mm", "m", "inch", "in"}
COUNT_UNITS = {"bottle", "bottles", "pc", "pcs", "piece", "pieces", "can", "cans", "unit", "units", "pack", "packs"}
NAMED_SYSTEMS = {"us", "uk", "eu"}
DIMENSIONS = re.compile(r"^(\d+(?:\.\d+)?)\s*(?:x|×)\s*(\d+(?:\.\d+)?)\s*(?:x|×)\s*(\d+(?:\.\d+)?)$")


def clean_text(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(SAFE_TEXT.sub(" ", value).split())


def compact_term(attribute: dict[str, Any]) -> str:
    value = attribute.get("value")
    unit = str(attribute.get("unit") or "").strip().lower()
    dimensions = DIMENSIONS.fullmatch(str(value).strip()) if value is not None else None
    if dimensions and unit in {"mm", "cm", "m"}:
        return f"{dimensions.group(1)}x{dimensions.group(2)}x{dimensions.group(3)}{unit}"
    if value is None or not re.fullmatch(r"\d+(?:\.\d+)?", str(value).strip()):
        return ""
    number = str(value).strip()
    if unit in MEASUREMENT_UNITS:
        return f"{number}{unit}"
    if unit in NAMED_SYSTEMS:
        return f"{unit.upper()} {number}"
    return ""


def alternate_term(attribute: dict[str, Any]) -> str:
    value = attribute.get("value")
    unit = str(attribute.get("unit") or "").strip().lower()
    dimensions = DIMENSIONS.fullmatch(str(value).strip()) if value is not None else None
    if dimensions and unit in {"mm", "cm", "m"}:
        return f"{dimensions.group(1)} x {dimensions.group(2)} x {dimensions.group(3)} {unit}"
    if value is None or not re.fullmatch(r"\d+(?:\.\d+)?", str(value).strip()):
        return ""
    number = str(value).strip()
    if unit in NAMED_SYSTEMS:
        return f"{unit.upper()}{number}"
    if unit in MEASUREMENT_UNITS:
        return f"{number} {unit}"
    return ""


def build(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("mode") != "search_plan":
        raise ValueError("mode must be search_plan")
    category = clean_text(payload.get("category"))
    if not category:
        raise ValueError("category must be a non-empty ASCII search phrase")
    aliases = [clean_text(item) for item in payload.get("aliases", []) if clean_text(item)]
    attributes = [item for item in payload.get("attributes", []) if isinstance(item, dict)]
    primary = next((item for item in attributes if item.get("priority") == "primary" and compact_term(item)), None)
    primary = primary or next((item for item in attributes if compact_term(item)), None)
    primary_term = compact_term(primary or {})
    queries = [" ".join(part for part in (category, primary_term) if part)]

    count_gte = any(
        str(item.get("unit") or "").strip().lower() in COUNT_UNITS
        and item.get("operator") in {"gte", "gt"}
        for item in attributes
    )
    if count_gte:
        for packaging in ("multipack", "carton"):
            queries.append(" ".join(part for part in (category, primary_term, packaging) if part))
    else:
        alternative = alternate_term(primary or {})
        if alternative and alternative != primary_term:
            queries.append(" ".join(part for part in (category, alternative) if part))
        for alias in aliases:
            queries.append(" ".join(part for part in (alias, primary_term) if part))

    unique: list[str] = []
    for query in queries:
        query = " ".join(query.split())
        if query and query.lower() not in {item.lower() for item in unique}:
            unique.append(query)
    return {"queries": unique[:3], "policy": "retrieval_only; validate original requirements separately"}


def main() -> None:
    print(json.dumps(build(json.load(sys.stdin)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        raise SystemExit(2)
