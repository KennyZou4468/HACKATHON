import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from normalize_attributes import audit, parse_quote


class AttributeNormalizationTests(unittest.TestCase):
    def test_water_pack_and_volume_are_verified(self):
        result = audit({
            "mode": "audit",
            "requirements": [
                {"id": "count", "target": {"value": 20, "unit": "bottles", "operator": "gte"}},
                {"id": "volume", "target": {"value": 500, "unit": "ml", "operator": "eq"}},
            ],
            "observations": [{"field": "title", "quote": "Cactus Natural Mineral Water 24 x 500ml"}],
        })
        self.assertEqual([item["status"] for item in result["results"]], ["normalized_verified", "normalized_verified"])

    def test_safe_physical_unit_conversions(self):
        facts = parse_quote("0.5 L bottle, 1.5 kW appliance, 65 w adapter")
        self.assertIn({"kind": "volume_ml", "value": "500.0", "quote": "0.5 L"}, facts)
        self.assertIn({"kind": "power_w", "value": "1500.0", "quote": "1.5 kW"}, facts)
        self.assertIn({"kind": "power_w", "value": "65", "quote": "65 w"}, facts)

    def test_bare_24s_is_not_a_pack_count(self):
        self.assertFalse(any(item["kind"] == "pack_count" for item in parse_quote("Natural water 24s")))
        result = audit({
            "mode": "audit",
            "requirements": [{"id": "count", "target": {"value": 20, "unit": "bottles", "operator": "gte"}}],
            "observations": [{"field": "title", "quote": "Natural water 24s"}],
        })
        self.assertEqual(result["results"][0]["status"], "unknown")

    def test_shoe_system_is_not_converted(self):
        payload = {
            "mode": "audit",
            "requirements": [{"id": "size", "target": {"value": 9, "unit": "US", "operator": "eq"}}],
            "observations": [{"field": "title", "quote": "Running shoe US9"}],
        }
        result = audit(payload)
        self.assertEqual(result["results"][0]["status"], "normalized_verified")
        payload["requirements"][0]["target"]["unit"] = "EU"
        self.assertEqual(audit(payload)["results"][0]["status"], "unknown")

    def test_storage_tb_is_intentionally_unknown(self):
        result = audit({
            "mode": "audit",
            "requirements": [{"id": "storage", "target": {"value": 1024, "unit": "GB", "operator": "eq"}}],
            "observations": [{"field": "title", "quote": "Laptop with 1TB SSD"}],
        })
        self.assertEqual(result["results"][0]["status"], "unknown")

    def test_normalisation_does_not_turn_a_real_shortfall_into_a_pass(self):
        result = audit({
            "mode": "audit",
            "requirements": [{"id": "count", "target": {"value": 20, "operator": "gte"}}],
            "observations": [{"field": "title", "quote": "Drinking water 12-pack 500 ml"}],
        })
        self.assertEqual(result["results"][0]["status"], "not_met")


if __name__ == "__main__":
    unittest.main()
