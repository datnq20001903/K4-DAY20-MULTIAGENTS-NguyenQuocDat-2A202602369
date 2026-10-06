---
name: log-triage-aggregation
description: Use when converting logs with multiline entries and repetition markers into structured summaries.
---
1. Read the log-format documentation and output schema before parsing.
2. Treat each timestamped line as a new entry; attach following continuation lines, including tracebacks, to that entry until the next timestamped line.
3. Parse repetition markers as additional occurrences of the immediately preceding entry; apply the count consistently to aggregate totals.
4. Normalize timestamps to UTC, normalize service names exactly as specified, and normalize levels before filtering or counting.
5. Build the requested error records and service aggregates from the same parsed entries to avoid inconsistent totals.
6. Sort records by the required keys after normalization, not by source order.
7. Include all required top-level schema metadata and verify the serialized output by parsing it back and checking timestamps, exceptions, repeat counts, ordering, and aggregates.
=== END
