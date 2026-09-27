import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from audit_query_plan import audit as audit_plan
from audit_search_coverage import audit as audit_coverage


class QueryAuditTests(unittest.TestCase):
    def test_plan_accepts_distinct_semantic_routes(self):
        result = audit_plan({
            "mode": "query_plan", "category": "sunscreen", "hard_requirement_ids": ["spf", "volume"],
            "plan": {"initial_queries": [
                {"query": "face sunscreen SPF50", "purpose": "core", "included_requirement_ids": ["spf"], "omitted_requirement_ids": ["volume"]},
                {"query": "facial sunblock lightweight", "purpose": "alternative", "included_requirement_ids": [], "omitted_requirement_ids": ["spf", "volume"]},
            ], "recovery_query": {"query": "sunscreen SPF50 50ml", "purpose": "recovery", "included_requirement_ids": ["spf", "volume"], "omitted_requirement_ids": []}},
        })
        self.assertEqual(len(result["initial_queries"]), 2)

    def test_plan_rejects_duplicate_routes(self):
        payload = {
            "mode": "query_plan", "category": "laptop", "hard_requirement_ids": [],
            "plan": {"initial_queries": [
                {"query": "laptop", "purpose": "core", "included_requirement_ids": [], "omitted_requirement_ids": []},
                {"query": " laptop ", "purpose": "alternative", "included_requirement_ids": [], "omitted_requirement_ids": []},
            ], "recovery_query": {"query": "notebook", "purpose": "recovery", "included_requirement_ids": [], "omitted_requirement_ids": []}},
        }
        with self.assertRaises(ValueError):
            audit_plan(payload)

    def test_coverage_requires_recovery_for_one_plausible_candidate(self):
        result = audit_coverage({
            "mode": "search_coverage",
            "initial_query_results": [{"candidate_ids": ["a", "b"]}, {"candidate_ids": ["b", "c"]}],
            "plausible_candidate_ids": ["b"],
        })
        self.assertTrue(result["recovery_required"])

    def test_coverage_skips_recovery_for_two_plausible_candidates(self):
        result = audit_coverage({
            "mode": "search_coverage",
            "initial_query_results": [{"candidate_ids": ["a", "b"]}],
            "plausible_candidate_ids": ["a", "b"],
        })
        self.assertFalse(result["recovery_required"])


if __name__ == "__main__":
    unittest.main()
