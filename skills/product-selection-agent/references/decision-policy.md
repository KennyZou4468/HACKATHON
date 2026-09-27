# Decision policy

## Detail-page priority

Select pages to inspect using preference relevance rather than randomness. Until a deterministic selector is implemented, use this auditable preliminary weighting:

- requirement/search-keyword match: 40%
- plausibility against target and maximum budget: 25%
- official or verified seller signals: 15%
- rating quality: 10%
- sales/review evidence: 10%

This score only chooses which listings receive detail checks. It is not the final product score. Exclude obvious accessories, parts, deposits, rentals, duplicates, irrelevant categories, and suspicious impossible prices before applying it.

## Constraint outcomes

For every candidate and hard constraint, record one outcome:

- `pass`: verified fact satisfies it;
- `fail`: verified fact violates it;
- `unknown`: source data is insufficient.

Any `fail` removes the candidate from the eligible ranking set. Any `unknown` prevents the candidate from being called a verified match unless the user explicitly accepts the uncertainty.

For quantitative performance constraints, product specifications alone do not produce `pass` or `fail`. Require a retrieved benchmark matching the relevant product or laptop GPU power class, workload/game, resolution, preset, and technologies such as DLSS/frame generation. Otherwise record `unknown`, even if the GPU is generally considered powerful.

## Deterministic budget check

Use the most recent explicit budget in the active Conversation State. A later user budget replaces an earlier one; never blend them or retain the earlier value for affordability labels.

For each candidate whose exact current variant price is verified, calculate:

```text
budget_delta = verified_current_price - current_budget
remaining_budget = current_budget - verified_current_price
```

- If `budget_delta <= 0`: the product is within budget. Display `预算内（余量 SGD remaining_budget）`.
- If `budget_delta > 0`: the product exceeds budget. Display `超预算 SGD budget_delta`; an optional percentage is `budget_delta / current_budget × 100`, rounded sensibly.
- Never calculate affordability from the original/list price, discount percentage, another candidate's price, an inferred budget, or a superseded budget.
- If currency differs, convert only with an explicit sourced exchange rate and timestamp; otherwise mark budget status unknown.
- If exact variant price is unverified or shown only as a product-wide range, use `预算状态待确认`; do not claim it passes the hard budget and do not emit a percentage.
- For a price range, display `预算状态待确认（展示范围 SGD X–Y）`. Never compute budget remaining from the minimum or maximum endpoint.

Before presenting results, run a consistency check across the understood-needs sentence, every displayed price, every budget label, and the recommendation text. A candidate priced below SGD 3000, for example SGD 2504, must never be described as exceeding a SGD 3000 budget.

## Catalogue-versus-derived claims

Treat the following separately:

- Catalogue facts: title, stated configuration, displayed price, condition, rating, sold count, description, IDs, and URL.
- Availability: verified only when the source explicitly reports current stock; sold count and successful retrieval do not prove it.
- Derived arithmetic: budget remaining, budget overage, and price difference; calculate directly from normalized values.
- External performance: FPS, benchmark scores, runtime, thermal behavior, acoustics, and ML throughput; requires matching benchmark evidence.
- Hardware capability: upgrade slots, maximum RAM, GPU power limit, ports, battery capacity, weight, and color gamut; requires explicit specification evidence.

Do not let one evidence class stand in for another. A seller description can support what the listing claims, but it is not independent benchmark evidence.

If a quantitative hard constraint remains `unknown`, the product may appear only as a provisional candidate. Ranking may compare verified catalogue fit, but the response must not declare a verified winner or suggest the unknown target is probably close.

Derived explanations must remain no stronger than their evidence. More RAM is a verified capacity difference; its effect on a particular model, compiler, game, or concurrency level remains conditional without workload evidence. CPU core count, GPU name, OLED technology, and brand tier do not independently prove speed, latency, cooling, glare, or longevity.

Product numbering is not a deterministic performance map. Unless an approved mapping table or retrieved comparison exists, do not rank GPU or CPU model names by speed and do not use them to decide which candidate is closer to an FPS target.

User-derived resource suggestions remain soft inferences until confirmed. Do not turn `local small-model inference` into a 32 GB requirement, required upgrade, or exclusion criterion.

When catalogue fields conflict, record the exact conflict and set the affected facts to unknown. The candidate cannot be variant-verified or recommended until the conflict is resolved. Its displayed price is not considered bound to a trustworthy configuration, so affordability remains pending.

Hard constraints apply to detail-page selection as well as final filtering. Do not inspect a clearly over-budget card while plausible within-budget cards remain; over-budget inspection is a no-match recovery action, not a default performance shortcut.

## Display consistency

Refresh rate and rendered FPS are different. A 165 Hz panel refreshes at most 165 times per second. Higher rendered FPS may reduce latency, but the recommendation must not say the panel displays or fully utilizes 200 distinct frames each second.

## Search-scope wording

Search results are a sample, not an exhaustive catalogue. Negative findings must state both the actual query count and returned-card count, for example `not found in the 10 cards returned from the first page of 1 query`. Do not call returned cards “query groups” and do not infer platform-wide absence, lack of stock, or replacement by a newer generation.

## Personalized ranking

Use a 0–100 normalized score per relevant dimension. Candidate dimensions may include:

- use-case performance;
- portability;
- battery;
- display;
- memory/storage suitability;
- value;
- seller/listing confidence;
- data completeness.

Derive weights from the Preference Profile. Document weights and the facts/mappings used. Do not score irrelevant dimensions merely because data exists.

```text
base_fit = Σ(normalized_dimension_score × user_weight)
confidence_adjusted_score = base_fit × evidence_confidence
```

Rules:

- User weights apply to fit dimensions; listing confidence and data completeness adjust confidence rather than pretending to improve product quality.
- Missing facts do not receive an average or perfect score. Mark the dimension unknown and reduce evidence confidence.
- Do not use LLM intuition as a benchmark database.
- Use only verified catalogue facts and approved deterministic mappings for CPU/GPU/use-case capability.
- Do not claim score precision that the inputs cannot support.
- Higher specifications or price do not automatically mean better fit.

## Shortlist diversity

Prefer `best_match`, `best_value`, and one user-relevant `specialist`. If role differences are not supported by evidence, present a smaller shortlist rather than manufacture distinctions.

## Recommendation confidence

- `high`: exact variant, price, availability, hard constraints, and key scoring facts verified.
- `medium`: core fit is supported, but one non-hard field or secondary comparison is missing.
- `low`: variant/price or a major decision field remains ambiguous. Do not give a definitive winner.
