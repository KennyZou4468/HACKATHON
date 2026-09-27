---
name: "product-selection-discovery"
description: "Plan bounded, category-neutral marketplace retrieval and audit query coverage before product-detail verification."
---

# Product-selection discovery

Use this skill only after the product-selection agent has extracted the current session's category, hard conditions, preferences, and unknowns. Query text is for retrieval only: it never proves a product fact or changes a user requirement.

## Query plan

Create a compact JSON query plan with one or two distinct initial semantic routes and one recovery route. Each query has a `purpose` (`core`, `specification`, `alternative`, or `recovery`) and the IDs of requirements it deliberately includes or omits. Include category terms and only evidence-safe requirements. For quantity requests, search realistic packaging routes rather than requiring an exact requested count in a title.

Run `scripts/audit_query_plan.py` on the plan before retrieval. It rejects duplicate routes, malformed requirement references, and unbounded plans. Search initial routes with the configured bounded result limit, deduplicate listings, and remove obvious accessories, refills, deposits, rentals, empty containers, unrelated categories, and incompatible products before details.

## Coverage and recovery

Run `scripts/audit_search_coverage.py` with the plausible candidate IDs. Use the single recovery query only when fewer than two plausible candidates remain, then merge and deduplicate. Do not claim the marketplace has no product: negative findings apply only to the retrieved sample.

## Detail and verification boundary

Inspect details only for plausible candidates. A product-level starting price is not a selected variant price. Pass selected model IDs, exact source observations, current budget, hard constraints, and preferences to the marketplace variant verifier. The verifier, not the query text, decides price, stock, and hard-condition eligibility.

## Input language

Extract requirements in the customer's language. Preserve named sizing systems and units in the plan; do not translate or convert them into a different measurement system.
