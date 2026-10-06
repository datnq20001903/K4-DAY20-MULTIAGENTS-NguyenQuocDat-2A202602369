---
name: maintain-accurate-changelog-for-fixes
description: Use when completing bug fixes to record each fix clearly in the project changelog.
---
1. Open the CHANGELOG.md file in the project root.
2. Locate the section headed "## Unreleased".
3. For each bug fix, add a bullet point under "## Unreleased" in the format:
   - fix(<function name>): <short description>
4. Use the exact function name where the fix was applied.
5. Write concise, clear descriptions summarizing the fix.
6. Add at least one bullet per bug fixed; if multiple bugs fixed, add multiple bullets.
7. Keep the changelog entries in chronological order of fixes.
8. Review the changelog for spelling and formatting consistency.
9. Commit the changelog update along with the code changes for the fixes.
10. Before release, move the "## Unreleased" section to a versioned heading as appropriate.
