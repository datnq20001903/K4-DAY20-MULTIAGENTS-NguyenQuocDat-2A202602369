---
name: data-output-integrity
description: Use when transforming tabular data into structured answer files or cleaned datasets.
---
1. Read the task specification and input format before transforming data; identify required output files, schemas, units, normalization rules, and deduplication criteria.
2. Parse values with suitable types and explicit missing-value handling; represent monetary values as integer cents when required, avoiding binary floating-point arithmetic for currency.
3. Normalize timestamps to the required UTC representation and categorical values to the specified canonical spelling.
4. Deduplicate according to the stated key and policy; keep input-row counts separate from distinct usable-record counts.
5. Write every required artifact, including metadata and cleaned data, with exact field names, header order, and row granularity.
6. Validate JSON and CSV by parsing them back; check schema, units, row counts, uniqueness, and representative normalized values against the source.
