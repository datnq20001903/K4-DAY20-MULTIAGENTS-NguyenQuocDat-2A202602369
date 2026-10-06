"""GUIDE Phần 3 - Người tuyển chọn skill (skill curator): tự viết skill từ các lần chạy thất bại.   >>> SINH VIÊN CÀI ĐẶT curate_skills <<<

Pseudo-code: guides/pseudocode/04_curator.md
Kiểm tra:    pytest tests/test_04_curator.py
Chạy thật:   python -m lab.curator
"""
import re
from pathlib import Path

from .tasks import eval_markers   # có sẵn: định danh của tác vụ đánh giá, tính lúc chạy

# ---- CÓ SẴN, KHÔNG SỬA: kiểm tra và tách khối skill (phần dễ sai và liên quan bảo mật) ----------------
SAFE_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_skill(text: str, expected_name: str | None = None) -> list[str]:
    """Kiểm tra nội dung một SKILL.md. Trả về danh sách vấn đề (rỗng = hợp lệ).

    Quy tắc: có khối YAML frontmatter; `name` chữ thường/số/gạch ngang (tối đa 64 ký tự) và bằng `expected_name`
    nếu được truyền; có `description` (tối đa 1024 ký tự); phần thân tối đa 80 dòng; không chứa chuỗi nào của
    `eval_markers()`. Quy tắc về `name` cũng là biện pháp bảo mật: tên khối do LLM sinh ra được dùng để tạo
    đường dẫn, nên `../evil` không được lọt qua.
    """
    problems = []
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text.strip() + "\n", re.S)
    if not m:
        return ["missing YAML frontmatter"]
    front, body = m.groups()
    name = re.search(r"^name:\s*(.+)$", front, re.M)
    desc = re.search(r"^description:\s*(.+)$", front, re.M)
    n = name.group(1).strip() if name else ""
    if not SAFE_NAME.fullmatch(n) or len(n) > 64:
        problems.append("invalid name")
    elif expected_name is not None and n != expected_name:
        problems.append("name differs from the block name")
    if not desc or len(desc.group(1).strip()) > 1024:
        problems.append("missing or too long description")
    if len(body.strip().splitlines()) > 80:
        problems.append("body longer than 80 lines")
    low = text.lower()
    for marker in eval_markers():
        if marker in low:
            problems.append(f"mentions evaluation material: {marker}")
    return problems


def parse_skill_blocks(reply: str) -> list[tuple[str, str]]:
    """Tách câu trả lời của LLM thành danh sách (name, nội dung SKILL.md).

    Khuôn dạng: `=== SKILL: <name> ===` ... `=== END ===`. Một khối kết thúc ở điểm nào đến trước trong ba điểm:
    `=== END ===`, tiêu đề `=== SKILL:` kế tiếp, hoặc cuối văn bản (LLM đôi khi quên dòng END).
    """
    pattern = re.compile(r"^=== SKILL: (\S+) ===[ \t]*\n(.*?)(?=^=== END ===|^=== SKILL: |\Z)", re.S | re.M)
    return [(name, text.strip()) for name, text in pattern.findall(str(reply))]
# --------------------------------------------------------------------------------------------------


def curate_skills(results_dir="results", source_condition="baseline", out_dir=None, model=None, max_skills: int = 3) -> list[Path]:
    """Đọc các lần chạy của TÁC VỤ HỌC (role == "learn") trong `source_condition`, nhờ LLM viết skill, ghi file.

    Các bước: nạp run.json + trace.md -> (nếu không có check nào thất bại: in cảnh báo và trả về [] mà KHÔNG gọi LLM)
    -> dựng prompt -> model.invoke(prompt) -> parse_skill_blocks -> validate_skill(text, expected_name=name)
    -> ghi `<out_dir>/<name>/SKILL.md`. Mặc định `out_dir` = <gốc lab>/skills/auto (dùng `ROOT` từ lab.tasks).
    Giữ tối đa `max_skills` skill hợp lệ; skill không hợp lệ bị bỏ qua.
    Prompt chứa, với mỗi check thất bại, TÊN và trường `detail` (lời nhận xét của bot đánh giá: phát biểu quy tắc bị vi phạm)
    cùng phần cuối của vết (trace). Với tác vụ học, `detail` chỉ phát biểu quy tắc, không chứa đáp án.
    Tuyệt đối KHÔNG đưa dữ liệu của tác vụ đánh giá (role == "eval") vào prompt.
    model mặc định: make_model() (lab.model).
    Trả về: danh sách đường dẫn SKILL.md đã ghi.
    """
    import json

    from .model import make_model
    from .tasks import ROOT
    from langchain_openai import ChatOpenAI

    if max_skills < 0:
        raise ValueError("max_skills must not be negative")
    if max_skills == 0:
        return []
    runs = []
    for file in sorted((Path(results_dir) / source_condition).glob("*/run.json")):
        run = json.loads(file.read_text(encoding="utf-8"))
        if run.get("role") != "learn":
            continue
        failed = [
            {"name": check["name"], "detail": check.get("detail", "")}
            for check in run.get("checks", []) if check.get("passed") is False
        ]
        trace_file = file.with_name("trace.md")
        trace = trace_file.read_text(encoding="utf-8")[-6000:] if trace_file.exists() else ""
        runs.append({"task": run["task"], "failed_checks": failed, "trace": trace})
    if not any(run["failed_checks"] for run in runs):
        print("Warning: no failed checks in learning tasks; no model call made.")
        return []
    prompt = (
        "Write procedural SKILLs for an engineering agent from the learning-run feedback below. "
        f"Produce at most {max_skills} short, generalizable skills that prevent common process failures "
        "on NEW tasks of the same kind. The feedback states violated rules, not an answer key. "
        "Do not include task IDs, task-specific input filenames, functions, columns, answers or numbers. "
        "Names explicitly required by reusable organizational conventions in the feedback are allowed. "
        "Do not use evaluation material. Each skill must have YAML frontmatter with a lowercase "
        "hyphenated name and a description stating when to use it, then at most 40 lines of actionable "
        "instructions and verification steps. Do not propose incorrect shortcuts or memorized answers. "
        "Use exactly this output format for every skill:\n"
        "=== SKILL: <name> ===\n---\nname: <name>\ndescription: Use when ...\n---\n"
        "<instructions>\n=== END ===\n\nLearning evidence:\n"
        + json.dumps(runs, ensure_ascii=False, indent=2)
    )
    chat_model = make_model() if model is None else model
    if isinstance(chat_model, ChatOpenAI) and chat_model.model_name in {"gpt-5.6-luna", "gpt-6-luna"}:
        chat_model = chat_model.model_copy(update={"reasoning_effort": "none"})
    response = chat_model.invoke(prompt)
    reply = response.content
    if not isinstance(reply, str):
        reply = "\n".join(block.get("text", "") for block in reply if isinstance(block, dict))
    destination = Path(out_dir) if out_dir is not None else ROOT / "skills" / "auto"
    written = []
    seen = set()
    for name, text in parse_skill_blocks(reply):
        if len(written) >= max_skills:
            break
        if name in seen or validate_skill(text, expected_name=name):
            continue
        file = destination / name / "SKILL.md"
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text + "\n", encoding="utf-8")
        written.append(file)
        seen.add(name)
    return written


if __name__ == "__main__":
    for p in curate_skills():
        print("wrote", p)
