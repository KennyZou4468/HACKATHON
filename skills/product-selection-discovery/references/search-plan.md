# Marketplace search plan

Build this deterministic plan before live retrieval. It increases recall; it is not evidence and never changes the user's hard requirements.

1. Write one JSON payload to `/workspace/product-selection-search-plan.json` with `mode="search_plan"`, an English marketplace `category`, optional `aliases`, and measurable user attributes. Preserve the user's original values, units, and operators.
2. Run `python3 /workspace/.openclaw/sandbox-skills/skills/product-selection-discovery/scripts/build_search_plan.py < /workspace/product-selection-search-plan.json` exactly once.
3. Search every returned query on page 1 with limit 10. Merge and deduplicate by item ID or canonical URL before the single budget-gate run.

For an at-least quantity on packaged goods, the plan uses neutral packaging words such as `multipack` and `carton`; it never uses the requested count as a search constraint. The count remains a hard verifier condition. For named sizing systems, it may vary spacing (`US 9` / `US9`) but never changes systems. It never converts capacity, power, storage, or dimensions.
