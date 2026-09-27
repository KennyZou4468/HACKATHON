#!/usr/bin/env python3
"""Decide deterministically whether a third recovery query is needed."""

from __future__ import annotations

import json
import sys
from typing import Any


def audit(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("mode") != "search_coverage":
        raise ValueError("mode must be search_coverage")
    results = payload.get("initial_query_results")
    plausible = payload.get("plausible_candidate_ids")
    if not isinstance(results, list) or not isinstance(plausible, list):
        raise ValueError("initial_query_results and plausible_candidate_ids must be arrays")
    source_ids: set[str] = set()
    for result in results:
        if not isinstance(result, dict) or not isinstance(result.get("candidate_ids"), list):
            raise ValueError("each result needs candidate_ids")
        source_ids.update(str(item) for item in result["candidate_ids"])
    plausible_ids = sorted({str(item) for item in plausible if str(item) in source_ids})
    recovery_required = len(plausible_ids) < 2
    return {
        "recovery_required": recovery_required,
        "reason": "fewer_than_two_distinct_plausible_candidates" if recovery_required else "initial_coverage_sufficient",
        "distinct_initial_candidates": len(source_ids),
        "distinct_plausible_candidates": len(plausible_ids),
        "plausible_candidate_ids": plausible_ids,
    }


def main() -> None:
    print(json.dumps(audit(json.load(sys.stdin)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        raise SystemExit(2)
