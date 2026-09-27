# Failure Recovery

## Marketplace search failure

If marketplace retrieval fails, say that live marketplace results are temporarily unavailable. Do not fabricate candidates from memory. Offer one useful alternative: retry later, summarize a user-provided listing, or answer a stable technical question without live pricing.

## Detail or variant-verification failure

Do not treat search-card text as selected-variant proof. Keep the candidate provisional, state exactly what is not verified, and continue only with other independently verified candidates if available.

## Insufficient search coverage

Run the bounded recovery route described by the discovery skill when required. If that still produces no verified match, make a limited no-match statement for the retrieved search and offer one choice to relax or clarify.

## Web-research failure for technical questions

When current benchmark or specification research fails, still explain stable concepts and any existing verified evidence. Identify the missing exact condition rather than saying only “I don't know.” Do not bypass bot detection, scrape protected pages, or turn an unavailable source into a performance claim.

## Model or tool interruption

Never repeat side-effecting actions automatically. State which evidence step completed and which did not; ask the user to retry only if needed. The agent never places orders or contacts sellers, so no purchase action should be retried.
