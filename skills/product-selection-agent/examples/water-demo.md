# Example: Multipack Water Search

## Customer input

`I need at least 20 bottles of plain 500 ml drinking water for no more than SGD 10.`

## Expected behaviour

1. Preserve `500 ml`, `at least 20 bottles`, and `SGD 10` as literal hard requirements.
2. Let discovery search plausible packaging routes such as multipacks and cartons; do not require the exact text `20 bottles` in a listing title.
3. Accept a safely explicit expression such as `24 x 500ml` as evidence for both 24 bottles and 500 ml per bottle after the documented normalisation audit.
4. Treat bare `24s` as unknown quantity. It must not become proof of 24 bottles without contextual seller evidence.
5. Exclude empty bottles, coconut water, flavoured drinks, refills, and unrelated beverages before ranking.

## Correct no-match wording

`No verified match in this search: the in-budget listings did not provide enough evidence for both plain drinking water and the required bottle count. Would you accept a 24-bottle carton once its count is verified?`
