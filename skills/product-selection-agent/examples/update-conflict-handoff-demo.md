# Example: Update, Conflict, and Handoff

## Conversation

Customer: `I need exactly 20 bottles and at least 30 bottles for SGD 10.`

Agent: `Those two quantity requirements conflict: should the purchase contain exactly 20 bottles, or at least 30 bottles?`

Customer: `At least 20. My budget is now SGD 12.`

## Expected behaviour

1. Resolve the contradiction without consuming the normal clarification allowance.
2. Replace SGD 10 with the current explicit budget of SGD 12. Do not blend the two budgets.
3. Refresh listing price and reported stock before presenting a changed recommendation.
4. If asked, create a handoff that lists the active quantity, current budget, candidates reviewed, verified versus provisional facts, links, and the outstanding question. Do not claim to have contacted a seller.
