# Consumer Language Policy

Write for a shopper, not for an engineer reviewing an evidence pipeline. Before finalising any sentence, translate internal status into: **what was found, what it means for this shopper, and what still needs checking**.

## General rules

- Lead with the shopper-facing meaning; put evidence detail second only when it changes the decision.
- Use short familiar words. Define a necessary technical term once in parentheses.
- State uncertainty precisely, but never use a bare internal status as the explanation.
- Do not expose tool names, JSON fields, validation steps, search-page limits, ranking internals, or model reasoning unless the shopper asks.
- Do not repeat the same caveat for every row. Put a shared limitation once above or below a comparison when it applies to all options.

## Translation guide

| Internal idea | Say to the shopper | Avoid saying alone |
| --- | --- | --- |
| selected variant price verified | `The price for the selected [colour/size/configuration] is SGD X.` | `verified selected-variant price` |
| starting price or price range | `This is the listing's starting price. The price for the option you need is not confirmed yet.` | `Budget pending` |
| stock unavailable | `The [selected option] is currently shown as unavailable.` | `variant status: unavailable` |
| stock unknown | `The listing does not clearly show whether this option is in stock.` | `stock unknown` |
| seller/product-page specification | `The product page lists [fact].` | `seller claim` |
| buyer rating and reviews | `Shopee buyers gave this listing X/5 from Y reviews.` | `seller-listed rating` |
| independently tested fact missing | `The listing says [fact], but I could not find an independent test for it.` | `not independently measured` |
| hard requirement passed | `It matches your must-have requirement: [requirement].` | `hard constraint pass` |
| evidence missing | `I could not confirm [specific fact] from the product page or an appropriate source.` | `unknown` / `unverified` |
| provisional candidate | `This could suit you, but please confirm [specific missing fact] before buying.` | `provisional only` |
| no verified match | `I could not confirm a match among the listings checked because [reason].` | `no verified match` without context |
| source conflict | `The listing gives conflicting information about [field], so I would not rely on it yet.` | `source conflict` |
| search/tool failure | `I could not retrieve live listing details right now, so I cannot safely recommend a current product.` | tool name or error message |
| benchmark gap | `I could not find a test for this exact setup, so I cannot promise that result.` | `benchmark unverified` |

## Examples across categories

- Water: `The title says “24s”, but it does not clearly say 24 bottles, so I cannot confirm the pack count.`
- Shoes: `The available option is labelled US 9. I have kept that sizing system rather than guessing an EU equivalent.`
- Furniture: `The product page lists 120 × 60 × 75 cm, which matches the size you asked for.`
- Electronics: `The page lists 65 W charging. That is the seller's stated specification, not a speed I have tested myself.`
- Computers: `This laptop has 16 GB of memory, which is enough for ordinary coding and several open apps; the listing does not confirm whether it can be upgraded.`

## Final check

Replace every vague phrase such as `good`, `high performance`, `verified`, `unknown`, `pending`, `claimed`, or `not independently measured` with either a concrete shopper-facing explanation or omit it. Preserve the underlying safety boundary; plain language must not make missing evidence sound confirmed.
