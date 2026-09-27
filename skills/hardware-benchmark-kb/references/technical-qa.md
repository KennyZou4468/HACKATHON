# Technical specification and performance questions

Use this route when the user asks what a component means, compares two component models, or asks how a specification affects their workload. Do not run the Shopee catalogue workflow unless the user also asks for products, listings, live prices, or availability.

For a general terminology question — for example cores, threads, cache, VRAM, RAM channels, NVMe, TGP, or DLSS — first read `hardware-explainers.md`. Explain the stable concept directly in short plain language; do not search merely to define it. Use web research only when the user also needs a current or model-specific fact, benchmark, driver, price, compatibility, or product detail.

## Answer-first research workflow

1. Reuse requirements already stated in the current conversation or canonical purchase state. Do not ask again for a game, resolution, preset, frame-rate target, workload, or budget that is already known. For every laptop-purchase or laptop-comparison conversation, when both display resolution and external-display status are omitted, use the visible default assumption `1080p, laptop's built-in display, no external monitor`. For any game/FPS target that omits graphics settings or rendering features, also use `medium preset, native rendering, DLSS/FSR/XeSS and frame generation off`. State every applicable assumption in the answer. They are assumptions, not hard requirements, and any user-provided resolution, external-display, graphics-setting, upscaling, or frame-generation detail overrides them immediately.
2. Determine device class before reading local scores: `笔记本/laptop/notebook` means `laptop`; `台式机/desktop/PC/主机` means `desktop`. If a component-only request leaves class ambiguous, ask one compact clarification. Then read `skills/hardware-benchmark-kb/references/benchmark-snapshot.json` for an exact local CPU/GPU match in that class. State the selected class, snapshot date, and source URL with every local numerical reference. For current hardware, facts missing from the snapshot, prices, drivers, or game-specific benchmarks, run `web_search` before answering.
3. Use at most 3 research tool calls total (`web_search` or `web_fetch` combined), and make them sequential. Prefer a manufacturer specification for factual configuration and one reputable benchmark/review source for measured performance. A seller listing, forum post, SEO comparison page, or unsourced aggregate is not benchmark evidence.
4. Cite the source URL next to each factual or numerical claim. State the tested laptop/configuration, resolution, preset, power setting, and frame-generation/upscaling state when the source provides them.
5. A local CPU Mark, Single Thread Rating, or G3D Mark is a relative-performance reference only; it is never an exact-setting game benchmark. With a small local snapshot, describe only the direct recorded difference between explicitly listed entries, not a market-wide performance tier or rank. If no exact-setting benchmark exists, still answer the question: explain the verified architectural/specification differences and any retrieved nearby evidence, then state narrowly that the exact requested FPS remains unverified. Do not turn that missing datum into a general refusal.
6. If two research calls fail, or if the search provider returns bot detection, stop researching immediately. Give only stable conceptual guidance that can be stated without current facts, disclose the specific retrieval failure, and avoid numerical performance, price, or product claims. Do not reply only “I don't know.”

## Forbidden shortcuts

- Research evidence must come only from `web_search` and `web_fetch`. Never use `exec`, `process`, curl, wget, Python, Node, browser automation, or a downloaded page to search, scrape, bypass bot detection, or extract performance data. A web tool failure is evidence of an unavailable source, not authorization to bypass it.
- Do not issue concurrent research calls. Do not call search-engine URLs through `web_fetch`. Do not use Wikipedia, a retailer blog, an SEO comparison page, forum content, or a source without a stated methodology as the sole support for a numerical performance claim.
- Do not infer that a larger model number is faster, sufficient, safer, or better value without retrieved comparative evidence.
- Do not say a GPU “may be enough” for 60/144/200 FPS, that another is “more future-proof/safer,” or that a price difference is “usually a few hundred” without supporting sources.
- Do not generalize from a desktop GPU benchmark to a laptop GPU, or vice versa. Laptop GPU power limits, desktop board power, CPU/platform differences, and cooling matter. Do not calculate a direct cross-class percentage from the local snapshot.
- Do not claim coding, compilation, AI inference, training, cooling, battery life, or responsiveness differences from the GPU name alone.
- Do not ask the user to choose an experience target when the target is already present in state. Ask one compact clarification only when the missing definition materially prevents a useful search.

## CPU and GPU comparison sources

For a CPU comparison, use PassMark CPU Benchmark (`cpubenchmark.net`) as the first comparative source. Search with the exact processor names and the `site:cpubenchmark.net` domain restriction. For laptop CPUs, preserve the exact mobile SKU; do not substitute a desktop CPU with a similar name. Use its CPU Mark and Single Thread Rating only as comparative indicators, not as a direct FPS or compile-time prediction.

For a GPU comparison, use PassMark Video Card Benchmark (`videocardbenchmark.net`) as one comparative source, with the exact desktop or Laptop GPU name. It does not replace an in-game benchmark: never turn its aggregate score into a CS2 FPS estimate.

`cpu.userbenchmark.com` is an optional secondary cross-check for CPU comparisons, never the sole source for a numerical claim or recommendation. It commonly presents a CAPTCHA to automated access. If it requires CAPTCHA, returns 403, or returns bot detection, record it as unavailable and continue only if the remaining research budget and a stronger source are available. Never bypass its CAPTCHA, scrape it using `exec`, or tell the user it was checked when it was not.

When the user asks for a CPU or GPU comparison, use this bounded sequence when evidence is needed: (1) one domain-targeted PassMark search or fetch; (2) one official manufacturer specification or reputable methodology-based review; (3) UserBenchmark only as an optional cross-check. Stop sooner if bot detection occurs, as specified above.

## Response shape

Lead with the practical conclusion. Then give the evidence-backed differences, what they mean for the user's stated scenario, and the exact remaining uncertainty. Include concise source links. Avoid an encyclopedia-style definition.
