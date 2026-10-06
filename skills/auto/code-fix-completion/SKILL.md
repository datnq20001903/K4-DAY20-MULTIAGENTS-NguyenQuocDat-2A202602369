---
name: code-fix-completion
description: Use when fixing bugs in a typed package that requires regression coverage and changelog entries.
---
1. Inspect the package conventions and identify each distinct bug before editing.
2. Add or preserve type annotations for every parameter and return value of each public function you touch; check other public functions if the task requires package-wide compliance.
3. Add `tests/test_regressions.py` with a separate test for each fixed bug, and ensure there are at least three tests when required by the project rules.
4. Under `## Unreleased` in `CHANGELOG.md`, add one bullet per fix using `- fix(<function name>): <short description>`.
5. Run the full relevant test suite and verify the regression tests are included and pass.
