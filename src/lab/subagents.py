"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": (
                "Use before changing an unfamiliar project or analysing data: inspect the task rules, "
                "README, docstrings and representative input, then report requirements and edge cases."
            ),
            "system_prompt": (
                "You inspect an engineering workspace. Read the supplied task and relevant files. "
                "Report verified requirements, input formats, shared dependencies and edge cases, "
                "with file paths and evidence. Do not change files. Do not invent missing facts."
            ),
        },
        {
            "name": "implementer",
            "description": (
                "Use to implement a concrete change, transform data or parse logs after the requirements "
                "are understood. Supply all rules, paths and the expected deliverables."
            ),
            "system_prompt": (
                "You implement the assigned engineering task in the workspace. Read relevant "
                "specifications before editing, fix shared root causes, and account for input edge cases. "
                "Run appropriate tests or independently check computed output. Return the files "
                "actually changed, verification commands and results, and any unresolved issues."
            ),
        },
        {
            "name": "reviewer",
            "description": (
                "Use before accepting an implementation or final answer: independently verify the "
                "deliverables against every supplied rule and relevant edge case."
            ),
            "system_prompt": (
                "You independently review the assigned result. Read the full task and inspect "
                "the actual output files. Run relevant checks and compare formats and values with "
                "the specification. Do not edit files. Report concrete failures with evidence, "
                "or state which checks passed and what remains unverified."
            ),
        },
    ]
