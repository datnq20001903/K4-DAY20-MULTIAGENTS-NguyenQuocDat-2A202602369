---
name: add-regression-tests-for-fixed-bugs
description: Use after fixing bugs to create regression tests that prevent reintroduction of those bugs.
---
1. For each bug fixed, write at least one dedicated test function that reproduces the bug scenario.
2. Place all regression test functions in the file tests/test_regressions.py.
3. Ensure each test function is clearly named to reflect the bug it covers.
4. Write tests to assert the correct behavior or output that fixes the bug.
5. Avoid duplicating existing tests; focus on the specific bug conditions.
6. Run the full test suite to verify all tests pass, including the new regression tests.
7. Confirm that tests fail if the bug is reintroduced by temporarily reverting the fix.
8. Maintain the regression tests as part of the test suite for ongoing validation.
9. Use consistent test framework conventions and fixtures as used in the project.
10. Commit the regression tests together with the bug fix code changes.
