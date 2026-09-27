import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from assert_session_contract import assert_route


class AcceptanceHarnessTests(unittest.TestCase):
    def test_all_nine_scenarios_have_a_route_and_assertions(self):
        scenarios = json.loads((ROOT / "acceptance_scenarios.json").read_text())
        self.assertEqual(len(scenarios), 9)
        self.assertEqual({item["id"] for item in scenarios}, {
            "vague_need", "conflict", "budget_update", "unbound_variant_price", "no_match",
            "wrong_category", "multilingual", "sales_handoff", "technical_route",
        })
        self.assertTrue(all(item["route"] and item["assertions"] for item in scenarios))

    def test_technical_route_rejects_shopee(self):
        events = [{"message": {"content": [{"type": "toolCall", "name": "shopee__search_products"}]}}]
        self.assertEqual(assert_route(events, "technical"), ["technical route called Shopee"])

    def test_discovery_route_requires_shopee(self):
        self.assertEqual(assert_route([], "discovery"), ["shopping route did not call Shopee"])

    def test_handoff_rejects_order_action(self):
        events = [{"message": {"content": [{"type": "toolCall", "name": "shopee__order_product"}]}}]
        self.assertEqual(assert_route(events, "handoff"), ["handoff attempted an order action"])


if __name__ == "__main__":
    unittest.main()
