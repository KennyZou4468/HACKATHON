# Variant Price and Availability Policy

## Price states

Classify every marketplace price before using it:

| Source state | User-facing treatment |
| --- | --- |
| A current price bound to the chosen model ID | `Verified selected-variant price` |
| Listing starting price, product-level price, or range | `Budget pending` |
| Missing, conflicting, or currency-mismatched price | `Budget pending` |

Only the first state may be compared with the active budget or used for remaining-budget arithmetic. A discount badge, original price, seller rating, title, or lower-priced sibling model does not bind a price to the chosen configuration.

## Availability

Use `Available` only when the selected model is explicitly reported available by the current verifier. Use `Unavailable` when that selected model is explicitly unavailable. Otherwise use `Stock unknown`.

## Variant binding

The displayed product name, selected option, model ID, current price, stock result, URL, and verified observations must all describe the same candidate. If a listing has several configurations and none is identifiable, it may be discussed only as a provisional listing; it cannot be called within budget.

## Checkout boundary

Listing prices exclude any unverified shipping, vouchers, taxes, and checkout changes. State this once per final response when a price is shown; do not imply the final payable total is verified.
