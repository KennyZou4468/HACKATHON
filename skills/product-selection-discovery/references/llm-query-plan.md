# Structured LLM query plan

Use this before live search for every product category. The LLM may reason about user wording, category vocabulary, compatible form factors, and marketplace-language synonyms. It must not assert that a query proves a specification or that omitting a term relaxes a hard requirement.

Create one JSON payload at `/workspace/product-selection-query-plan.json`:

```json
{
  "mode": "query_plan",
  "category": "English marketplace category phrase",
  "hard_requirement_ids": ["..."],
  "plan": {
    "initial_queries": [
      {"query": "...", "purpose": "core", "included_requirement_ids": ["..."], "omitted_requirement_ids": ["..."]},
      {"query": "...", "purpose": "specification|alternative", "included_requirement_ids": ["..."], "omitted_requirement_ids": ["..."]}
    ],
    "recovery_query": {"query": "...", "purpose": "recovery", "included_requirement_ids": ["..."], "omitted_requirement_ids": ["..."]}
  }
}
```

From the workspace working directory, run `python3 .openclaw/sandbox-skills/skills/product-selection-discovery/scripts/audit_query_plan.py < product-selection-query-plan.json` once. Search its one or two initial queries. After examining titles and cards, list only plausible same-category candidate IDs in `/workspace/product-selection-search-coverage.json`, then run `python3 .openclaw/sandbox-skills/skills/product-selection-discovery/scripts/audit_search_coverage.py < product-selection-search-coverage.json` once. Run the audited recovery query only when it returns `recovery_required=true`. Merge and deduplicate results before the budget gate.

Query intents must differ: core category, a decisive specification or compatibility term, and a recovery route targeting the observed failure mode. A `gte` quantity is normally omitted from retrieval and retained as a verifier condition; use packaging/form-factor vocabulary for discovery instead. Query plans may use synonyms, but may not change the user profile or use query text as evidence.
