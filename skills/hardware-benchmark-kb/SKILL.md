---
name: "hardware-benchmark-kb"
description: "Look up curated, dated laptop and desktop CPU/GPU benchmark snapshots for grounded component comparisons; do not use for live prices or FPS estimates."
---

# Hardware benchmark knowledge base

Use this skill when a user asks how a CPU or GPU compares with another, or asks for a quantitative relative-performance reference. Read `references/hardware-explainers.md` for stable terminology questions, `references/technical-qa.md` for routing and research limits, and `references/benchmark-snapshot.json` before making a numerical claim.

## Use rules

- Determine the requested device class before selecting evidence: `笔记本/laptop/notebook` means `laptop`; `台式机/desktop/PC/主机` means `desktop`. If a component-only request does not establish a class and the exact product name is ambiguous, ask one compact device-class clarification before comparing.
- Match exact component names and form factor. `RTX 4060 Laptop GPU` is not the desktop RTX 4060; a laptop CPU must not be replaced by a similar desktop SKU. Never calculate a direct percentage or ranking across laptop and desktop entries.
- State the selected class visibly: `按笔记本条目比较` or `按台式机条目比较`. If the user explicitly asks for a cross-class comparison, show the two classes separately and explain that power, cooling and platform make the aggregate scores non-equivalent.
- State that the result is a local benchmark snapshot and show its snapshot date and source URL.
- CPU Mark / Single Thread Rating and GPU G3D Mark are comparative indicators only. They do not prove in-game FPS, compile time, battery life, temperature, or a product's exact performance.
- With the seed snapshot, compare only entries explicitly present in the file and state the calculated difference. Do not call a component `同级上限`, `主流档`, `中上`, `同一档`, or give a market-wide rank unless a future snapshot declares a named cohort with enough comparable records and a documented ranking method.
- When a user requests a subset of stored models, say only that the answer compares those requested entries. Never claim that the snapshot contains only that subset; if relevant, report the complete CPU/GPU entry counts separately.
- For laptop GPUs, retain the seller's stated TGP separately. A benchmark entry with a different or unspecified TGP is comparative context, not proof for that laptop. For desktop GPUs, retain board-power/TDP separately and do not relabel it as laptop TGP.
- If the exact model is absent, say the local knowledge base has no matching snapshot. Do not infer a score from its name. Web research may be attempted only under the technical-QA retrieval limits.
- Never use this dataset for prices, stock, or product-variant affordability.

## Maintenance

The snapshot is curated, dated evidence rather than a live feed. Add an entry only with: exact name, class/form factor, metric, value, source URL, source-as-of date, snapshot date, and caveat. Replace or append data on a documented refresh; never silently overwrite a historical value.
