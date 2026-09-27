# Safe attribute normalisation audit

Run this audit only after the Shopee variant verifier returns and only for a hard condition whose result is `unknown`. It is a deterministic formatting and unit parser, not an alternative product verifier.

## Allowed workflow

1. Preserve the original user requirement and the original Shopee verifier result.
2. If an exact source quote may contain a safe formatting difference, write one JSON payload to `/workspace/product-selection-normalization-audit.json` with `mode="audit"`, the unresolved requirements, and their original observations.
3. Run `python3 /workspace/.openclaw/sandbox-skills/skills/product-selection-agent/scripts/normalize_attributes.py < /workspace/product-selection-normalization-audit.json` exactly once.
4. Use `normalized_verified` only when the script returns it with an exact source quote. Display it as “verified after format normalisation”, not as a Shopee MCP verified result.
5. If the result is `unknown` or `not_met`, keep the original verifier outcome. Do not retry, edit a quote, change a requirement, or ask the normaliser to infer missing evidence.

## Safe registry

The normaliser accepts only unambiguous formatting and physical-unit rules: whitespace and case in units, litre/millilitre, kilogram/gram/milligram, kilowatt/watt, dimensions with `x` or `×`, explicit pack-count labels, `N x measurement` pack notation, SGD price spelling, and the same named shoe system with spacing differences. Explicit count targets such as `bottles` or `pieces` can use those two count forms; they are never inferred from a bare suffix.

Bare suffixes such as `24s` are not a count. Shoe systems are never converted. Storage TB is deliberately not equated with GB because seller conventions differ. Product claims, seller descriptions, and nearby text do not fill missing evidence.

## Post-verification LLM audit

After the deterministic normalisation audit, the response model may perform one restricted semantic review: it may remove unsupported claims, retain uncertainty, or explain why a normalised match passed. It may not add facts, change `not_met` to a pass, or request another tool call.
