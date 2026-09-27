# Conversation State

Maintain one decision state for the current purchase. Update it incrementally from the current OpenClaw conversation rather than reconstructing it from memory.

This state is session-local and must not be stored in a workspace file. Do not create, read, or consult `/workspace/product-session-state.json`, `preference_profile.json`, `candidates.json`, `validate_input.json`, or any other cross-session purchase-state file. A new OpenClaw conversation starts with an empty decision state. The current conversation's earlier user messages are the only source for carried-forward budget and preferences.

```json
{
  "schema_version": "1.0",
  "decision_id": "session-local-id",
  "stage": "understanding|clarifying|searching|verifying|filtering|ranking|presenting|updating|no_match|handoff",
  "profile": {},
  "clarification": {
    "used": false,
    "question": null,
    "answer": null,
    "reason": null,
    "recovery_used": false
  },
  "conflict_clarifications": {
    "count": 0,
    "history": [],
    "unresolved": []
  },
  "search_handoff": null,
  "filter_result": null,
  "ranking_result": null,
  "shortlist": [],
  "assumptions": [],
  "warnings": [],
  "recommendation_version": 0,
  "last_changed_fields": [],
  "updated_at": "ISO-8601 timestamp"
}
```

## State rules

- Treat the JSON above as an in-conversation schema, not a file to write. Never transfer it between sessions.

- Set `clarification.used=true` as soon as the agent asks its first pre-shortlist question.
- Contradiction questions update `conflict_clarifications` and do not change `clarification.used`.
- A contradiction is a pair of mutually incompatible explicit requirements or a target that cannot be evaluated without resolving its definition. Ordinary preference trade-offs remain subject to the one-question normal limit.
- Ask contradictions in a combined question when possible. Do not repeat the same unresolved question after refusal; branch into labeled scenarios or mark the target unverifiable.
- Permit at most two consecutive contradiction-clarification rounds per purchase decision. Contradiction questions do not consume the normal-question allowance, but they are not unlimited.
- Never reset `clarification.used` during the same purchase decision.
- User-initiated changes update the profile and `last_changed_fields`; they do not reset clarification.
- A newer explicit value supersedes the older active value for the same field. Retain the previous value only in history; all filtering, arithmetic, and labels use the current value.
- Increment `recommendation_version` whenever the shortlist or primary recommendation changes.
- Preserve previous search timestamps so stale results can be identified.
- Reuse recent candidates within the same conversation when still fresh, but refresh price and any explicitly available stock field before making a changed final recommendation. If the tool does not expose stock, keep it unknown.
- Start a new decision state only when the user clearly switches to a different purchase decision or category.
- Never persist candidate-specific performance guesses, inferred GPU minimums, temporary search hypotheses, prices, or stock as user hard constraints. Persist them only as timestamped assumptions or evidence gaps, and invalidate them when a new search begins.
