# Snapshot maintenance

Add only exact laptop component records from an attributable source. Capture the source URL and the source's own as-of date where present, then add the local snapshot date.

For PassMark CPU data, preserve both CPU Mark and Single Thread Rating. For PassMark GPU data, preserve G3D Mark, memory amount, and the source-listed maximum TDP. Do not merge desktop and laptop records.

Before a batch refresh, retain the prior JSON as a dated snapshot. A changed score is normal because PassMark aggregates submitted results; explain the snapshot date rather than treating the newest value as timeless.

UserBenchmark may be recorded only when its page is accessible without bypassing CAPTCHA and when accompanied by a stronger source. It cannot be the only basis for a numerical recommendation.
