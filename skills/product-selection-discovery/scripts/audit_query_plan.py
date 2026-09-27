#!/usr/bin/env python3
"""Validate a structured LLM marketplace-query plan without judging products."""

from __future__ import annotations

import json
import re
import sys
from typing import Any


PURPOSES = {"core", "specification", "alternative", "recovery"}


def normalize(query: str) -> str:
    return " ".join(query.casefold().split())


def validate_query(item: Any, requirement_ids: set[str], recovery: bool) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise ValueError("each query must be an object")
    query = item.get("query")
    purpose = item.get("purpose")
    included = item.get("included_requirement_ids", [])
    omitted = item.get("omitted_requirement_ids", [])
    if not isinstance(query, str) or not (2 <= len(query.strip()) <= 120):
        raise ValueError("query must be 2-120 characters")
    if purpose not in PURPOSES or (recovery and purpose != "recovery") or (not recovery and purpose == "recovery"):
        raise ValueError("invalid query purpose")
    if not isinstance(included, list) or not isinstance(omitted, list):
        raise ValueError("requirement ID lists are required")
    included_set, omitted_set = set(included), set(omitted)
    if not included_set.issubset(requirement_ids) or not omitted_set.issubset(requirement_ids):
        raise ValueError("query references an unknown requirement ID")
    if included_set & omitted_set:
        raise ValueError("a requirement cannot be both included and omitted")
    return {
        "query": " ".join(query.split()),
        "purpose": purpose,
        "included_requirement_ids": sorted(included_set),
        "omitted_requirement_ids": sorted(omitted_set),
    }


def audit(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("mode") != "query_plan":
        raise ValueError("mode must be query_plan")
    category = payload.get("category")
    if not isinstance(category, str) or not category.strip():
        raise ValueError("category is required")
    requirement_ids = set(payload.get("hard_requirement_ids", []))
    if not all(isinstance(item, str) and item for item in requirement_ids):
        raise ValueError("hard_requirement_ids must be non-empty strings")
    plan = payload.get("plan")
    if not isinstance(plan, dict):
        raise ValueError("plan must be an object")
    initial = plan.get("initial_queries")
    if not isinstance(initial, list) or not 1 <= len(initial) <= 2:
        raise ValueError("initial_queries must contain one or two queries")
    audited_initial = [validate_query(item, requirement_ids, False) for item in initial]
    recovery = validate_query(plan.get("recovery_query"), requirement_ids, True)
    all_queries = audited_initial + [recovery]
    normalized = [normalize(item["query"]) for item in all_queries]
    if len(set(normalized)) != len(normalized):
        raise ValueError("queries must be distinct")
    return {
        "initial_queries": audited_initial,
        "recovery_query": recovery,
        "max_live_queries": 3,
        "policy": "queries retrieve candidates only; original hard requirements remain for verification",
    }


def main() -> None:
    print(json.dumps(audit(json.load(sys.stdin)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        raise SystemExit(2)
