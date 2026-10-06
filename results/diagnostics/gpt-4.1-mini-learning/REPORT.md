# Báo cáo Lab: Self evolving Agentic

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Nguyễn Quốc Đạt | 2A202602369 | Thực hiện lab với hỗ trợ Codex: harness, thí nghiệm và báo cáo theo GUIDE. |

- Mô hình: `LAB_MODEL=openai:gpt-4.1-mini`, `LAB_TEMPERATURE=0`, `recursion_limit=60`; dùng nhất quán cho các lượt hợp lệ và curator.
- Deep Agents 0.7.21; Windows/PowerShell chuẩn bị môi trường; harness chạy Docker Linux Python 3.11 để có `/bin/sh`. Native `.venv` Python 3.11.9. Backend shell không kế thừa biến môi trường chứa API key.
- Giai đoạn trước freeze: 6 lượt baseline/subagents learn hợp lệ, 3 lượt skills-auto development và 1 lần curator. Ba lượt chẩn đoán hạ tầng lưu riêng trong `results/diagnostics/`, không tính vào bảng chính.
- Commit của tag `freeze`: sẽ ghi sau khi tạo tag; chưa chạy bất kỳ evaluation nào tại thời điểm commit giả thuyết.

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

- H1 (subagents so với baseline): Dự đoán điểm evaluation trung bình của subagents cao hơn baseline, nhưng token cao hơn. Trên learning, implementer giúp data từ 0/8 lên 5/8; code giữ 7/10, logs giảm 1/9 xuống 0/9. Vì giao việc có thể mất schema, cải thiện không chắc chắn. Căn cứ: GUIDE 2.3 và `guides/pseudocode/02_subagents.md` về vai trò, truyền đủ yêu cầu và kiểm chứng báo cáo.
- H2 (skills-auto so với baseline): Dự đoán skills-auto cao nhất trên code evaluation nếu đọc ba skills Python, nhưng điểm evaluation trung bình không nhất thiết vượt subagents: curator không sinh skill cho data/logs. Learning development code vẫn 7/10 vì không đọc skill. Căn cứ: `guides/pseudocode/05_skill_quality.md` mục 1 và 5 về nạp dần, description, đọc và thực hiện; ba lỗi rule của code baseline trong mục 4.
- H3 (tác vụ học so với tác vụ đánh giá): Dự đoán lợi ích rule checks trên evaluation nhỏ hơn learning, vì chỉ học quy ước từ learning và evaluation có thể có quy ước mới. Chênh lệch development/frozen learning cùng skills sẽ được dùng nhận diện nhiễu. Căn cứ: README mục thiết kế thí nghiệm; GUIDE 4.2 yêu cầu giữ bộ skills và sao lưu development, phân biệt cải thiện trên learn với khả năng khái quát.

## 3. Làm quen Deep Agents (Phần 0.3)

1. **Công cụ mặc định:** `python scripts/tour.py` liệt kê 9 công cụ: `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`, `execute`, `task`. Công cụ `execute` chạy lệnh shell trong sandbox, trả về stdout/stderr và mã thoát.
2. **Subagent `general-purpose`:** Theo mô tả của `task`, subagent này nghiên cứu câu hỏi phức tạp, tìm tệp/nội dung và thực hiện tác vụ nhiều bước; có các công cụ như tác tử chính. Mỗi lần gọi mặc định không có trạng thái: subagent chỉ nhận prompt được gửi và trả về một báo cáo cuối, không tự nhận toàn bộ hội thoại của tác tử chính. Vì vậy, lời giao việc cần chứa đủ yêu cầu, quy tắc, đường dẫn và định dạng kết quả. Tác tử chính tổng hợp báo cáo cho người dùng.
3. **Chỉ dẫn hành vi từ mô tả công cụ:** Tour in system prompt mặc định là `''` (rỗng). Câu từ `task`: “Put full detail in the prompt and state exactly what it should return — unless an agent type below says it inherits your conversation instead.” Câu từ `execute`: “Use read_file rather than cat/head/tail.” Đây là chỉ dẫn từ mô tả công cụ, không phải system prompt do sinh viên viết.

**Kiến trúc đã cài đặt:** agent chính điều phối bằng `task`; ba worker `explorer` (đọc đặc tả), `implementer` (sửa/chạy kiểm tra), `reviewer` (kiểm chứng độc lập). Chúng dùng cùng backend tệp/shell trong sandbox; không có message queue riêng. Curator là bước học ngoại tuyến, không phải worker trong mỗi lượt tác vụ. Runner ghi trace, token và kết quả check; `recursion_limit=60` và timeout shell 120 giây giới hạn thực thi. Không đồng nhất giới hạn recursion với số lần giao việc.

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

Chỉ sử dụng các lượt learning hợp lệ; không đưa lỗi API và CRLF vào taxonomy của tác tử.

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| code-learn | `rule_type_hints` | E | RULE: every public function (name not starting with '_') in the package has type annotations on all parameters and on the return value. |
| code-learn | `rule_regression_tests` | E | RULE: add tests/test_regressions.py with one test function per bug you fixed (at least 3); the file must pass. |
| code-learn | `rule_changelog` | E | RULE: record each fix in CHANGELOG.md under the heading '## Unreleased' as a bullet '- fix(<function name>): <short description>' (at least 3 bullets). |
| data-learn | `north_q1_revenue` | B/G | north_q1_revenue: wrong value (got None) |
| data-learn | `north_q1_orders` | B/G | north_q1_orders: wrong value (got None) |
| data-learn | `top_region` | B/G | top_region: wrong value (got None) |
| data-learn | `missing_amount_orders` | B/G | missing_amount_orders: wrong value (got None) |
| data-learn | `duplicate_rows_removed` | B/G | duplicate_rows_removed: wrong value (got None) |
| data-learn | `rule_money_in_cents` | E | RULE: money values in answer.json are integer cents (1606.67 USD is written 160667). |
| data-learn | `rule_meta_block` | E | RULE: answer.json has an object `meta` = {"source": <input file name>, "rows_in": <number of data rows in the input file, duplicates included>, "rows_used": <number of distinct orders with a known amount>}. |
| data-learn | `rule_clean_csv` | E | RULE: write workspace/clean.csv with the header order_id,timestamp_utc,region,amount_cents; one row per distinct order with a known amount; timestamp_utc as YYYY-MM-DDTHH:MM:SSZ (UTC); region in canonical spelling (North, South, East, West); amount in integer cents. |
| logs-learn | `entry_count` | D/B | wrong number of entries (got 22) |
| logs-learn | `timestamps_utc` | D/B | 8/25 timestamps match |
| logs-learn | `exception_fields` | D/B | 17 wrong `exception` values |
| logs-learn | `repeat_counts` | D/B | 17 wrong `repeat_count` values |
| logs-learn | `counts_by_service` | D/B | counts_by_service: wrong values |
| logs-learn | `rule_service_names` | E | RULE: service names in the output are lower-case with '-' replaced by '_' (payment-service -> payment_service). |
| logs-learn | `rule_sorted_errors` | E | RULE: `errors` is sorted by service, then by timestamp_utc, ascending. |
| logs-learn | `rule_schema_header` | E | RULE: the top-level object has "schema_version": 2 and "generated_by": "log-triage". |

Baseline learn đạt kỹ thuật 8/18 và quy ước 0/9. Nhóm E có 9/19 check thất bại, cùng với 10/19 lỗi kỹ thuật B/G hoặc D/B; nếu tính nhãn chính, E là nhóm riêng lớn nhất nhưng không quá nửa tổng số lỗi. Data trace ghi `ModuleNotFoundError: No module named 'pandas'`, nhiều SyntaxError ở lệnh Python một dòng và `answer.json` rỗng: chưa thực thi được pipeline nhưng vẫn kết thúc. Logs được viết JSON thủ công, không chạy parser/validation: chỉ 8/25 timestamps khớp, 17 exception và repeat_count sai. Code kiểm tra được 6 visible tests và 7/7 technical checks nên không có bằng chứng lỗi A–D ở tác vụ này; quy ước chưa biết là nguồn thiếu điểm. Baseline code final_message nói đã sửa import trong test nhưng `tests_not_modified=true`: lời mô tả thay đổi không được hash xác nhận; không dùng lời nói này làm bằng chứng test thực sự bị sửa.

Skill có thể nhắc quy trình kiểm chứng và quy ước còn thiếu, nhưng bộ ba curator hiện chỉ bao phủ code; không tự giải quyết parsing data/logs.

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent: `explorer` đọc yêu cầu và tìm bằng chứng; `implementer` xử lý nguyên nhân, sửa và kiểm tra; `reviewer` kiểm chứng độc lập không sửa. Description chỉ rõ lúc gọi và system prompt giới hạn phạm vi, không nhúng quy ước ẩn của Acme.
- Mỗi tác vụ learn gọi `implementer` đúng 1 lần; không gọi explorer/reviewer. Không suy diễn hoạt động nội bộ từ trace chỉ chứa luồng chính.
- Code giao rõ docstrings và không sửa tests; worker trả code và báo tests pass, main ghi lại source rồi tự chạy pytest (6 passed). Prompt giao việc không nhắc rõ Acme review conventions dù user có nói; ba rule checks vẫn fail.
- Data giao đủ timezone/missing amount nhưng nói dedup theo tổ hợp bốn cột thay vì định danh order_id như README. Trên bộ learning vẫn đạt 5/5 technical, main đọc answer.json để xác nhận có file nhưng không tính lại. Logs giao đầy đủ `timestamp_utc`, exception và repeat_count; worker trả `timestamp` sai tên, main đọc file rồi vẫn chấp nhận: schema và mọi check đều fail. Đây là khoảng trống kiểm chứng sau handoff.

| Tác vụ | baseline → subagents (điểm) | Token baseline → subagents | Giây baseline → subagents |
|---|---|---|---|
| code-learn | 7/10 → 7/10 | 60100 → 82649 | 29.6 → 57.3 |
| data-learn | 0/8 → 5/8 | 53639 → 53556 | 31.2 → 21.3 |
| logs-learn | 1/9 → 0/9 | 21717 → 52603 | 15.1 → 21.2 |

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Chạy curator 1 lần từ baseline role=learn, sinh 3 skills; xóa 0, chạy lại 0, sửa tay 0. Validator kiểm tra cấu trúc và định danh evaluation; không bảo đảm đúng nội dung. Giữ nguyên bộ skills để đo cả kết quả âm.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `add-regression-tests-for-fixed-bugs` | Quy trình code tổng quát, không có tên hàm/dữ liệu/đáp án cụ thể; có phạm vi hẹp code. | Test theo bug và chạy lại đúng; tests/test_regressions.py là tên quy ước được phép. Tạm revert cần khôi phục chắc chắn, nếu không có thể làm mất fix; commit cũng không khả thi trong sandbox. | Body 10 dòng; description 91 ký tự: Use after fixing bugs to create regression tests that prevent reintroduction of those bugs. |
| `enforce-type-annotations-on-public-functions` | Quy trình code tổng quát, không có tên hàm/dữ liệu/đáp án cụ thể; có phạm vi hẹp code. | Quy tắc đầy đủ annotations đúng với learning feedback; mypy có thể chưa cài, nên static checking là phụ thuộc cần kiểm tra. Hướng dẫn commit không phù hợp sandbox không có Git metadata. | Body 10 dòng; description 131 ký tự: Use when writing or reviewing package code to ensure all public functions have complete type hints on parameters and return values. |
| `maintain-accurate-changelog-for-fixes` | Quy trình code tổng quát, không có tên hàm/dữ liệu/đáp án cụ thể; có phạm vi hẹp code. | CHANGELOG.md, Unreleased và fix(function) đúng feedback; bước chuyển sang heading version lúc release ngoài phạm vi sửa bug, có thể làm mất heading đang được checker yêu cầu nếu áp dụng sai thời điểm. | Body 11 dòng; description 82 ký tự: Use when completing bug fixes to record each fix clearly in the project changelog. |

Development: code-learn: 7/10, skills_read=0; data-learn: 0/8, skills_read=0; logs-learn: 1/9, skills_read=0. Trace code không có read_file SKILL.md nên chỉ có skills trong cấu hình không đủ chứng minh áp dụng. Kết quả development sẽ được giữ ở `results/skills-auto-dev/`.

## 7. Kết quả so sánh (Phần 4.3, 4.4)

Chưa chạy evaluation trước freeze. Bảng chính và breakdown sẽ bổ sung sau lượt chính thức.

## 8. Phân tích

Sẽ đối chiếu số liệu sau freeze theo sáu câu hỏi của mẫu.

## 9. Hạn chế và tính hợp lệ

1. Chỉ ba tác vụ mỗi vai trò, một lượt mỗi cấu hình: không ước lượng được độ tin cậy thống kê.
2. Chỉ một model gpt-4.1-mini, temperature 0 vẫn có thể nhiễu; không suy rộng sang model lớn hơn.
3. Trace chỉ luồng chính và mỗi snippet bị cắt 1500 ký tự; không quan sát trực tiếp mọi hành động worker hoặc toàn bộ output.
4. Quy ước do giảng viên thiết kế và feedback learning được đưa curator: cải thiện rule cùng miền không chứng minh học kỹ năng tổng quát.
5. Token trong run.json gồm main và workers, không gồm curator/connection tests/diagnostics; chưa quy đổi chi phí USD.

## 10. Kết luận

Chờ số liệu evaluation để kết luận; không khẳng định mức cải thiện trước khi đo.

## Phụ lục

- Thứ tự: setup → tour → implement TODOs → pytest → baseline/subagents learn → curator → skills-auto learn development → hypotheses → freeze → baseline/subagents eval → skills-auto all → verify_freeze → compare/breakdown → báo cáo.
- Windows pytest dùng basetemp trong `.venv` để tránh PermissionError. Docker dùng Python 3.11, `/bin/sh`, Git; backend PATH có Python và inherit_env=False.
- Luna kết nối đơn lẻ trả OK nhưng tool request lỗi 400 với reasoning_effort; đổi model theo yêu cầu sinh viên sang gpt-4.1-mini. Lượt lỗi có 0 token, nằm riêng diagnostics.
- Hai lượt code đầu bị tests_not_modified fail do checkout CRLF trong Windows trong khi hash chuẩn checker là blob Git LF. So sánh Git blob của test learning xác nhận nguyên nhân; xuất nguyên 35 file tasks từ HEAD sang fixture tạm ngoài submission rồi mount read-only. Không sửa tasks/tests/checker trong repo; không đọc nội dung evaluation trước freeze. Chỉ chạy lại hai code learn, các lượt data/logs giữ nguyên. Không xem đây là lỗi reasoning.
- Kiểm tra freeze thực hiện trong Linux cùng hệ điều hành chạy harness vì hash_skills dùng biểu diễn đường dẫn tương đối theo hệ điều hành; chạy native Windows có thể khác slash dù bytes bằng nhau.
- Không thực hiện phần mở rộng tùy chọn; không push remote trong phiên này.
