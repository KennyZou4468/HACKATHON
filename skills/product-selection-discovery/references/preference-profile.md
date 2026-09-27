# Preference Profile Contract

Maintain this structure in the current conversation only. Keep unknowns as `null` or empty arrays and never promote an inference to a hard condition.

```json
{
  "category": null,
  "locale": "SG",
  "marketplace_domain": "shopee.sg",
  "currency": "SGD",
  "budget": {"maximum": null, "hard": false, "evidence": null},
  "use_cases": [],
  "hard_constraints": [],
  "soft_preferences": [],
  "explicit_requirements": [],
  "assumptions": [],
  "unknowns": [],
  "clarification": {"used": false, "question": null, "reason": null},
  "conflict_clarifications": {"count": 0, "unresolved": []}
}
```

- The latest explicit value replaces the prior active value for the same field.
- The normal pre-search clarification limit is one. Conflict clarification is separate and capped at two consecutive rounds.
- Assumptions must be visible in the final response and are never hard constraints.
