import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from build_search_plan import build


class SearchPlanTests(unittest.TestCase):
    def test_water_quantity_uses_packaging_routes_not_exact_count(self):
        result = build({
            "mode": "search_plan", "category": "drinking water",
            "attributes": [
                {"value": 500, "unit": "ml", "operator": "eq", "priority": "primary"},
                {"value": 20, "unit": "bottles", "operator": "gte"},
            ],
        })
        self.assertEqual(result["queries"], [
            "drinking water 500ml",
            "drinking water 500ml multipack",
            "drinking water 500ml carton",
        ])
        self.assertNotIn("20", " ".join(result["queries"]))

    def test_shoe_system_gets_spacing_variant_without_conversion(self):
        result = build({
            "mode": "search_plan", "category": "running shoes",
            "attributes": [{"value": 9, "unit": "US", "operator": "eq", "priority": "primary"}],
        })
        self.assertEqual(result["queries"], ["running shoes US 9", "running shoes US9"])

    def test_laptop_uses_safe_storage_spacing_variant(self):
        result = build({
            "mode": "search_plan", "category": "laptop", "aliases": ["gaming laptop"],
            "attributes": [{"value": 16, "unit": "GB", "operator": "gte", "priority": "primary"}],
        })
        self.assertEqual(result["queries"], ["laptop 16gb", "laptop 16 gb", "gaming laptop 16gb"])

    def test_dimension_gets_spacing_variant_without_unit_conversion(self):
        result = build({
            "mode": "search_plan", "category": "desk",
            "attributes": [{"value": "120x60x75", "unit": "cm", "operator": "eq", "priority": "primary"}],
        })
        self.assertEqual(result["queries"], ["desk 120x60x75cm", "desk 120 x 60 x 75 cm"])


if __name__ == "__main__":
    unittest.main()
