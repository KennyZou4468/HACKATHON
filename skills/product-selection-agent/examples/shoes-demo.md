# Example: Multilingual Shoe Search

## Customer input

`我想买一双 US 9 的跑鞋，预算 120 新币，主要日常跑步。`

## Expected behaviour

1. Extract the category as running shoes, the named size system as `US 9`, the maximum budget as SGD 120, and everyday running as the use case.
2. Reply in English under the workspace language policy.
3. Search safe notation variants such as `US 9` and `US9`, but do not automatically convert this to EU 42 or any other system.
4. Recommend only a selected variant explicitly marked `US 9` and currently available. A seller's conversion chart may be shown as its own claim, not as a conversion invented by the agent.

## Avoid

- Do not recommend an EU-only variant merely because a title contains a US-to-EU chart.
- Do not say the product-level starting price is the US 9 price until the selected variant is bound and verified.
