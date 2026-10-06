---
name: enforce-type-annotations-on-public-functions
description: Use when writing or reviewing package code to ensure all public functions have complete type hints on parameters and return values.
---
1. Identify all public functions in the package: functions whose names do not start with an underscore.
2. For each public function, check that every parameter has an explicit type annotation.
3. Verify that the function’s return type is annotated.
4. If any parameter or the return type lacks annotation, add the appropriate type hint based on the function’s logic and expected inputs/outputs.
5. Use standard Python typing conventions and imports (e.g., from typing import Optional, List) as needed.
6. Run static type checkers (e.g., mypy) to confirm no missing or incompatible type hints remain.
7. Review the code to ensure type hints are consistent and clear.
8. Commit changes only after all public functions have complete and correct type annotations.
9. Document any complex type hints in docstrings if necessary for clarity.
10. Before finalizing, re-run tests to ensure no runtime issues were introduced by type hint changes.
