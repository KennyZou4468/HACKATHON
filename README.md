# AI Product Selection Agent

Team Bay2Bay — Team Code `RZ9B4TXE`

An OpenClaw-based product-selection agent that turns natural-language shopping needs into evidence-grounded recommendations from Shopee Singapore. It is designed to separate language understanding and explanation from deterministic checks for price, stock, product variants, and hard constraints.

## Included

- `skills/product-selection-agent/` — decision flow, response rules, safe attribute normalization, and edge-case contracts.
- `skills/product-selection-discovery/` — structured query planning, query-plan audits, and search-coverage checks.
- `evals/` — acceptance scenarios and session-route assertions.
- `docs/` — technical document source and business proposal.

## Safety model

- A listing starting price is never treated as the price of a selected product variant.
- Measurable hard conditions require literal source evidence and selected-variant verification.
- Safe format normalization may reconcile forms such as `500ml` and `500 ml`, but never converts shoe-size systems or invents pack counts from ambiguous shorthand such as `24s`.
- Technical questions route to explanation first; marketplace search runs only for products, pricing, stock, or listing requests.

## Tests

Run the regression suite from the repository root:

```bash
python3 -m unittest discover -s evals/tests -v
python3 -m unittest discover -s skills/product-selection-discovery/tests -v
python3 -m unittest discover -s skills/product-selection-agent/tests -v
```

## Deployment note

This repository intentionally excludes API keys, OpenClaw runtime configuration, conversation sessions, logs, and personal data. Configure those only in the deployment environment.
