# Báo cáo Lab: Self evolving Agentic

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Nguyễn Quốc Đạt | 2A202602369 | Thực hiện lab với hỗ trợ Codex: harness, thí nghiệm và báo cáo theo GUIDE. |

- Mô hình chính: `LAB_MODEL=openai:gpt-6-luna`; `LAB_TEMPERATURE=0`, `reasoning_effort="none"`, `recursion_limit=60`. Cấu hình reasoning được áp dụng nhất quán trong TODO build_agent và curate_skills; không sửa model.py có sẵn. Dùng cùng model cho main, workers và curator.
- Deep Agents 0.7.21; Windows PowerShell chuẩn bị môi trường, Docker Linux Python 3.11 chạy harness vì cần `/bin/sh`. Native `.venv` là Python 3.11.9. Backend shell timeout 120 giây, inherit_env=False.
- Số lượt cuối: 18 chính thức Luna + 3 development Luna; 12 lượt lịch sử/chẩn đoán lưu riêng (9 mini learning, 2 mini code CRLF, 1 Luna API lỗi ban đầu), tổng 33 run.json. Không đặt ngân sách số token cứng; không chạy mở rộng hoặc lặp chọn điểm. Trước freeze có 6 lượt baseline/subagents learn hợp lệ + 3 lượt skills-auto development. Curator Luna thử 2 lần: lần đầu API 400 do reasoning mặc định với temperature 0; lần thứ hai cùng reasoning none như harness thành công, sinh 3 skills. Xóa/sửa tay 0 skills Luna.
- Commit của tag `freeze`: `1ca4dfe1931c4e12c53a3e6341bb5e5605c959b6`; commit giả thuyết `5009116` đứng trước tag. Không đọc/chạy evaluation trước khi commit H1–H3.
- Kết quả gpt-4.1-mini và skills của nó được lưu riêng `results/diagnostics/gpt-4.1-mini-learning/` theo yêu cầu đổi model; không dùng trong bảng chính hoặc đầu vào curator Luna. Hai tool smoke tests gpt-5.6-luna và gpt-6-luna đều thành công (131 và 50 token), không tính vào token benchmark.

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

- H1 (subagents so với baseline): Dự đoán subagents cải thiện điểm evaluation trung bình vừa phải nhưng tăng token. Learn code giữ 7/10, data giảm 5/8 xuống 4/8, logs tăng 2/9 lên 6/9; cần reviewer kiểm chứng sau handoff, giao việc không bảo đảm đúng schema/định nghĩa. Căn cứ GUIDE 2.3 và guides/pseudocode/02_subagents.md về vai trò, context truyền và kiểm chứng kết quả.
- H2 (skills-auto so với baseline): Dự đoán skills-auto có điểm evaluation trung bình cao nhất và hơn baseline, chủ yếu nhờ code; ở development code tăng 7/10 lên 10/10 sau đọc skill. Data/logs skills chỉ nói units/schema khi được yêu cầu, chưa ghi đầy đủ quy ước Acme nên khó cải thiện rule checks ẩn của hai miền này. Căn cứ guides/pseudocode/05_skill_quality.md mục 1, 3, 5 về progressive disclosure, tính đúng và việc đọc/làm theo skill; phân loại lỗi mục 4.
- H3 (tác vụ học so với tác vụ đánh giá): Dự đoán mức cải thiện trên evaluation nhỏ hơn learning vì quy ước mới không có trong feedback; skills code có thể chuyển giao quy trình kiểm chứng nhưng không tự biết luật mới. Giữ cả development và frozen learn để đo nhiễu, không quy mọi khác biệt thành học. Căn cứ README mục thiết kế thí nghiệm, GUIDE 4.2 về freeze và sao lưu lượt development.

## 3. Làm quen Deep Agents (Phần 0.3)

1. **Công cụ mặc định:** `python scripts/tour.py` liệt kê 9 công cụ: `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`, `execute`, `task`. Công cụ `execute` chạy lệnh shell trong sandbox, trả về stdout/stderr và mã thoát.
2. **Subagent `general-purpose`:** Theo mô tả của `task`, subagent này nghiên cứu câu hỏi phức tạp, tìm tệp/nội dung và thực hiện tác vụ nhiều bước; có các công cụ như tác tử chính. Mỗi lần gọi mặc định không có trạng thái: subagent chỉ nhận prompt được gửi và trả về một báo cáo cuối, không tự nhận toàn bộ hội thoại của tác tử chính. Vì vậy, lời giao việc cần chứa đủ yêu cầu, quy tắc, đường dẫn và định dạng kết quả. Tác tử chính tổng hợp báo cáo cho người dùng.
3. **Chỉ dẫn hành vi từ mô tả công cụ:** Tour in system prompt mặc định là `''` (rỗng). Câu từ `task`: “Put full detail in the prompt and state exactly what it should return — unless an agent type below says it inherits your conversation instead.” Câu từ `execute`: “Use read_file rather than cat/head/tail.” Đây là chỉ dẫn từ mô tả công cụ, không phải system prompt do sinh viên viết.

**Kiến trúc đã cài đặt:** agent chính điều phối bằng `task`; ba worker `explorer` (đọc đặc tả), `implementer` (sửa/chạy kiểm tra), `reviewer` (kiểm chứng độc lập). Chúng dùng cùng backend tệp/shell trong sandbox; không có message queue riêng. Curator là bước học ngoại tuyến, không phải worker trong mỗi lượt tác vụ. Runner ghi trace, token và kết quả check; `recursion_limit=60` và timeout shell 120 giây giới hạn thực thi. Không đồng nhất giới hạn recursion với số lần giao việc.

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

Chỉ dùng baseline Luna learning hợp lệ; lỗi API và CRLF của lượt chẩn đoán không thuộc taxonomy reasoning.

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| code-learn | `rule_type_hints` | E | RULE: every public function (name not starting with '_') in the package has type annotations on all parameters and on the return value. |
| code-learn | `rule_regression_tests` | E | RULE: add tests/test_regressions.py with one test function per bug you fixed (at least 3); the file must pass. |
| code-learn | `rule_changelog` | E | RULE: record each fix in CHANGELOG.md under the heading '## Unreleased' as a bullet '- fix(<function name>): <short description>' (at least 3 bullets). |
| data-learn | `rule_money_in_cents` | E | RULE: money values in answer.json are integer cents (1606.67 USD is written 160667). |
| data-learn | `rule_meta_block` | E | RULE: answer.json has an object `meta` = {"source": <input file name>, "rows_in": <number of data rows in the input file, duplicates included>, "rows_used": <number of distinct orders with a known amount>}. |
| data-learn | `rule_clean_csv` | E | RULE: write workspace/clean.csv with the header order_id,timestamp_utc,region,amount_cents; one row per distinct order with a known amount; timestamp_utc as YYYY-MM-DDTHH:MM:SSZ (UTC); region in canonical spelling (North, South, East, West); amount in integer cents. |
| logs-learn | `timestamps_utc` | D/B | 23/25 timestamps match |
| logs-learn | `exception_fields` | D/B | 2 wrong `exception` values |
| logs-learn | `repeat_counts` | D/B | 2 wrong `repeat_count` values |
| logs-learn | `counts_by_service` | D/B | counts_by_service: wrong values |
| logs-learn | `rule_service_names` | E | RULE: service names in the output are lower-case with '-' replaced by '_' (payment-service -> payment_service). |
| logs-learn | `rule_sorted_errors` | E | RULE: `errors` is sorted by service, then by timestamp_utc, ascending. |
| logs-learn | `rule_schema_header` | E | RULE: the top-level object has "schema_version": 2 and "generated_by": "log-triage". |

Nhóm E chiếm 9/13 check thất bại (69.2%): quy ước ẩn chưa có trong prompt/README được đọc. Có 4 lỗi kỹ thuật logs; JSON viết thủ công thay vì parser kiểm chứng, chỉ 23/25 timestamps khớp và 2 exception/repeat_count sai. Baseline đạt kỹ thuật 14/18, quy ước 0/9. Code đạt 7/7 technical checks và data 5/5 nên chưa có bằng chứng lỗi A–D trong hai miền này; không khẳng định toàn bộ baseline yếu về kỹ thuật. Trace data dùng csv/datetime, kiểm đếm 101 rows, 94 unique và 7 duplicates; đây là bằng chứng kiểm chứng có thực. Chưa có bằng chứng vá triệu chứng C hoặc báo tạo tệp không tồn tại F ở baseline hợp lệ. Skill có thể chuyển quy ước E thành checklist; skill logs cần xử lý toàn bộ entry, timezone và repetition để giảm D/B.

## 5. Điều kiện `subagents` (Phần 2.3)

- Định nghĩa 3 worker: explorer đọc đặc tả không sửa; implementer sửa nguyên nhân và chạy kiểm tra; reviewer kiểm chứng độc lập không sửa. Main sử dụng task, không có coordinator/message queue riêng.
- Code gọi explorer 1 + implementer 1; data gọi explorer 1 + general-purpose 2; logs gọi explorer 1 + reviewer 1. Không phải mọi worker tùy chỉnh đều được gọi, built-in general-purpose vẫn tồn tại.
- Code truyền docstrings, đường dẫn và không sửa tests; main tự chạy shell kiểm tra sau worker. Data truyền timezone và missing sentinel nhưng lời giao việc không nhấn mạnh north_q1_orders chỉ đếm orders tham gia revenue: worker và main đếm 13 thay vì 10 dù revenue đúng. Main tự tính lại row counts/metrics nhưng lặp cùng lỗi diễn giải, cho thấy thêm kiểm tra không đủ nếu tiêu chí sai.
- Logs giao explorer nhiệm vụ tạo errors.json dù role explorer chỉ đọc: phạm vi giao việc lệch vai trò; reviewer kiểm tra độc lập, kết quả technical đạt 6/6 nhưng quy ước vẫn 0/3. Những quy ước Acme không hiện trong dữ liệu nên nhắc chung tên Acme không truyền được nội dung luật.
- Trace chỉ luồng main và báo cáo worker; token callback gồm cả worker. Không khẳng định mọi hành động bên trong worker được quan sát.

| Tác vụ | baseline → subagents (điểm) | Token baseline → subagents | Giây baseline → subagents |
|---|---|---|---|
| code-learn | 7/10 → 7/10 | 75383 → 102878 | 46.2 → 89.4 |
| data-learn | 5/8 → 4/8 | 29861 → 123507 | 15.3 → 92.3 |
| logs-learn | 2/9 → 6/9 | 21114 → 98926 | 19.2 → 71.0 |

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Curator Luna 2 lần thử, 1 lần trả đầu ra: lỗi API lần đầu chưa sinh skill, sửa reasoning none rồi gọi lại. 3 skills giữ nguyên đầu ra, xóa 0 và sửa tay 0; không sử dụng skills mini đã lưu riêng. Mỗi skill validate cấu trúc và eval_markers trước ghi. Tính hợp lệ không đồng nghĩa đầy đủ quy tắc.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `code-fix-completion` | Quy trình bugfix tổng quát; tên regression/changelog là quy ước được phép, không có tên hàm/đáp án cụ thể. | Đúng với learning feedback và development đạt 3/3 rule. Bước annotate ưu tiên hàm được sửa, phải kiểm tra cả package để tránh thiếu public function khác. | Body 5 dòng; description 96 ký tự: Use when fixing bugs in a typed package that requires regression coverage and changelog entries. |
| `data-output-integrity` | Quy trình tabular data tổng quát, không hardcode dữ liệu/metrics. | Không thấy hướng dẫn tính sai, nhưng cents chỉ khi required và metadata không có schema meta cụ thể; chưa mã hóa đầy đủ 3 Acme rules nên development vẫn 0/3 rule. | Body 6 dòng; description 84 ký tự: Use when transforming tabular data into structured answer files or cleaned datasets. |
| `log-triage-aggregation` | Quy trình multiline/repetition tổng quát. | Parser/count từ cùng entries đúng; chỉ nói normalize/sort/metadata theo schema mà không ghi service underscore/schema_version 2/generated_by, nên chưa giải quyết rule ẩn. Có dòng thừa === END do delimiter thiếu === ở đầu ra; giữ nguyên, không ảnh hưởng validator nhưng giảm độ sạch. | Body 8 dòng; description 97 ký tự: Use when converting logs with multiline entries and repetition markers into structured summaries. |

Development: code-learn: 10/10, skills_read=1, token=79163; data-learn: 4/8, skills_read=2, token=42500; logs-learn: 6/9, skills_read=1, token=60663. Code đọc code-fix-completion rồi tạo regression tests/type hints/changelog; data đọc 2 skills nhưng vẫn thiếu quy ước; logs đọc 1 skill và technical đạt 6/6, rules 0/3. Sao lưu development ở results/skills-auto-dev trước rerun chính thức.

## 7. Kết quả so sánh (Phần 4.3, 4.4)

| Task | baseline | subagents | skills-auto |
|---|---|---|---|
| code-learn | 7/10 | 7/10 | 10/10 |
| data-learn | 5/8 | 4/8 | 5/8 |
| logs-learn | 2/9 | 6/9 | 6/9 |
| code-eval | 7/11 | 7/11 | 10/11 |
| data-eval | 5/9 | 4/9 | 5/9 |
| logs-eval | 1/10 | 6/10 | 6/10 |
| **Mean score - learning tasks** | 0.52 | 0.62 | 0.76 |
| **Mean score - evaluation tasks** | 0.43 | 0.56 | 0.69 |
| **Mean tokens per run** | 36,509 | 134,659 | 61,414 |
| **Runs that read a skill** | 0/6 | 0/6 | 6/6 |

Kết quả `python scripts/check_breakdown.py` (bản lưu: `report/check_breakdown.txt`):

```text
condition     role    technical  house rules  mean tokens  read a skill
baseline      eval     13/18         0/12          30,900      0/3     
baseline      learn    14/18         0/9           42,119      0/3     
subagents     eval     17/18         0/12         160,882      0/3     
subagents     learn    17/18         0/9          108,437      0/3     
skills-auto   eval     18/18         3/12          50,329      3/3     
skills-auto   learn    18/18         3/9           72,500      3/3     
```

- Toàn bộ 18 lượt chính thức có error=null, skills_modified=false và token > 0. Sáu lượt skills-auto đều đọc skill; không có lượt chính thức bị ghi đè để chọn điểm.
- `python scripts/verify_freeze.py`: checked 6 runs of skill conditions: OK. Bộ skills không đổi sau tag, hashes và timestamps khớp freeze. Linux verifier dùng core.autocrlf=true giống Git Windows để tránh báo khác bytes CRLF của README kỹ năng có sẵn; không thay đổi skills.
- Full suite: 29 passed in 9.20s (Docker Linux). Các hằng số/helper có sẵn, tests/tasks/scripts và file template vẫn giữ nguyên; kiểm tra SHA-256 và AST trước freeze đạt.
- Lỗi/chuyển model trước thí nghiệm chính được ghi ở mục 1 và phụ lục, lưu riêng diagnostics. Chúng không thuộc mẫu 18 lượt hoặc taxonomy reasoning.

## 8. Phân tích

1. **Điểm học và đánh giá.** Mean normalized score learning: baseline 0.5157, subagents 0.6222, skills-auto 0.7639. Evaluation tương ứng 0.4306, 0.5603, 0.6882. Subagents tăng learning 10.65 điểm phần trăm, evaluation 12.96; skills tăng 24.81 và 25.76. Không có điều kiện chỉ tăng mean learn mà giảm mean eval trong mẫu này; riêng data subagents giảm ở cả hai vai trò. H1 được số liệu mean hỗ trợ với chi phí lớn; H2 được hỗ trợ. H3 dự đoán mức tăng eval nhỏ hơn learn không được xác nhận: mức tăng skills eval hơi lớn hơn learn. Điểm tuyệt đối eval thấp hơn learn không đồng nghĩa mức cải thiện thấp hơn. Các kết luận chỉ mô tả một lượt trên ba tác vụ.

2. **Technical và rules.** Baseline learn 14/18 technical, 0/9 rules; subagents 17/18, 0/9; skills 18/18, 3/9. Eval tương ứng baseline 13/18, 0/12; subagents 17/18, 0/12; skills 18/18, 3/12. Skills giúp 3 quy ước code cũ cùng quy trình test; parser logs cải thiện technical từ 2/6 learn và 1/6 eval lên 6/6 mỗi vai trò. Data/logs rule checks vẫn fail vì skills chỉ nhắc tuân thủ units/schema/sort được chỉ định, chưa chuyển đủ tên/key/units Acme thành luật cụ thể. Ba rules eval mới `rule_version_bump`, `rule_sorted_keys_format`, `rule_source_line` đều fail trong cả ba điều kiện; chúng không nằm trong learning feedback hay bộ skills. Đây là giới hạn chuyển giao luật mới.

3. **Cơ chế đọc và thực hiện.** Code eval skills_read=1, trace đọc `skills/code-fix-completion/SKILL.md`, tạo `workspace/tests/test_regressions.py`, type hints và CHANGELOG rồi chạy `PYTHONPATH=workspace python -m pytest workspace/tests -q` đạt 6 tests; `rule_regression_tests` chuyển false → true. Trace cũng cho thấy lệnh sai timeout 120000s bị tool từ chối, đường dẫn tests sai rồi import error; agent tự sửa lệnh và kiểm tra lại, nên final score không che dấu những bước thừa. Ngược lại `rule_version_bump` vẫn fail dù đã đọc skill: skill không có quy ước bump version. Data development đọc 2 skills và tự validate JSON nhưng assert north_q1_orders=13 theo cùng diễn giải sai, nên không phát hiện việc đếm cả missing orders; frozen learn lên 5/8 vẫn thiếu cả 3 rules. Skills_read là số tên skill riêng biệt của main, không chứng minh mọi bước được thực hiện.

4. **Token và hiệu quả.** Mean token 6 lượt (giá trị chính xác, bảng compare lấy phần nguyên): baseline 36509.67, subagents 134659.67, skills 61414.67. Subagents dùng 3.69 lần baseline; skills 1.68 lần baseline và 45.6% token subagents. Định nghĩa hiệu quả = mean normalized score toàn 6 tasks × 1000 / mean tokens: baseline=0.01296; subagents=0.00439; skills-auto=0.01182; baseline cao nhất theo tỷ số này, skills có chất lượng cao nhất. Subagents tốn nhiều token hơn skills nhưng điểm thấp hơn trong mẫu, chưa đáng chi phí nếu mục tiêu là điểm/token. Trường hợp subagents data-eval riêng tốn 310692 token nhưng chỉ đạt 4/9 cho thấy delegation lặp có thể tăng chi phí mà không sửa lỗi diễn giải. Không quy đổi USD, không coi token output/input đồng giá, không so latency nhân quả vì có container chạy đồng thời.

5. **Rò rỉ/quá khớp.** Curator chỉ nhận source_condition=baseline, role=learn, failed names/details và trace tail; không nhận run.json hoặc check.py evaluation trước freeze. Mỗi đầu ra được validate eval_markers và safe name; không chứa tên hàm/dữ liệu/đáp án evaluation. Tên tests/test_regressions.py và CHANGELOG.md là quy ước learning được phép. Giả thuyết commit trước freeze và skills giữ nguyên; các luật eval mới đều chưa đạt, phù hợp với giới hạn thông tin. Không phát hiện rò rỉ theo những phép kiểm tra này, nhưng validator chỉ chặn định danh, không chứng minh tuyệt đối mọi dạng rò rỉ hay quá khớp. Data/log skills khá chung, code learning rules chuyển giao tốt; không suy ra tổng quát sang mọi miền.

6. **Nhiễu trên cùng bộ skills.**

| Tác vụ learn | Development | Sau freeze | Thay đổi normalized score |
|---|---|---|---|
| code-learn | 10/10 | 10/10 | +0.00 điểm phần trăm |
| data-learn | 4/8 | 5/8 | +12.50 điểm phần trăm |
| logs-learn | 6/9 | 6/9 | +0.00 điểm phần trăm |

Mean learning development 0.7222 → frozen 0.7639, tăng 4.17 điểm phần trăm, chỉ data thêm 1 check technical. Bộ skills và hash không đổi; chênh lệch không phải kết quả curator học thêm. Hai lượt là bằng chứng nhiễu/khác đường hành động, không đủ ước lượng variance hoặc confidence interval; không coi mọi chênh lệch nhỏ trong bảng là hiệu ứng chắc chắn.

## 9. Hạn chế và tính hợp lệ

1. Ba tác vụ mỗi vai trò, một lượt mỗi cấu hình: không có khoảng tin cậy hoặc bằng chứng thống kê rộng.
2. Chỉ một model và reasoning none; temperature 0 vẫn có nhiễu, không suy rộng sang model lớn/reasoning khác.
3. Trace chỉ main, snippet cắt 1500 ký tự; không quan sát đầy đủ hoạt động worker hoặc toàn bộ artifact.
4. Quy ước do giảng viên thiết kế và feedback learning được cung cấp curator: lợi ích cùng miền không chứng minh học kỹ năng tổng quát.
5. Token run gồm main+workers nhưng không gồm curator, smoke tests hoặc diagnostics; không quy đổi USD khi chưa có billing/pricing kiểm chứng.

6. Một số điều kiện độc lập chạy trong container đồng thời để tiết kiệm thời gian; số giây có thể bị ảnh hưởng tranh chấp CPU/API nên không dùng latency làm kết luận nhân quả.
7. Skills có dòng thừa delimiter và quy tắc có điều kiện chưa đủ cụ thể; validator không phát hiện những thiếu sót ngữ nghĩa này. Hash path/Git newline khác giữa Windows và Linux yêu cầu môi trường kiểm chứng nhất quán.

## 10. Kết luận

Với gpt-6-luna reasoning none trong mẫu sáu tác vụ, skills-auto có mean evaluation 0.69, cao hơn subagents 0.56 và baseline 0.43. Skills giúp đủ technical checks và ba quy ước code đã học, chưa giúp ba quy ước evaluation mới. Subagents tăng chất lượng so baseline nhưng dùng nhiều token nhất, trong khi baseline có tỷ số điểm/token cao nhất. Cùng bộ skills vẫn dao động một check data giữa development và frozen nên chưa có kết luận thống kê. Bước tiếp theo là cải thiện việc curator trích xuất schema/units cụ thể từ learning feedback rồi đo một thí nghiệm mới với lặp độc lập và freeze mới.

## Phụ lục

### Lệnh đã chạy và môi trường tái lập

1. Setup `.venv` Python 3.11, cài requirements và editable; `.env` nằm trong gitignore. Tour dùng model giả, không tiêu token. Windows Temp lỗi quyền được khắc phục bằng basetemp trong `.venv`.
2. Implement đúng 5 TODO trong 4 module, bảo toàn helpers/prompt. Offline test trước implementation có NotImplementedError; sau implementation suite Docker đạt 29/29. Review harness không thấy vi phạm contract; phạm vi quan sát và redaction nguyên secret vẫn có giới hạn.
3. Thử Luna tool reasoning trước đó lỗi 400; thử mini và lưu riêng. Theo lựa chọn cuối của sinh viên, smoke gpt-6-luna none gọi ping thành công (50 token); `LAB_MODEL=openai:gpt-6-luna`, LAB_TEMPERATURE=0, reasoning none áp dụng cả agent và curator. Curator lần đầu dùng reasoning mặc định bị 400 temperature, chỉnh tương thích trong TODO rồi thử lại thành công; không sửa model.py.
4. Learning và curator Luna:

   ```bash
   python -m lab.runner --condition baseline --tasks learn
   python -m lab.runner --condition subagents --tasks learn
   python -m lab.curator
   python -m lab.runner --condition skills-auto --tasks learn
   mv results/skills-auto results/skills-auto-dev
   ```

5. Điền H1–H3 và sections 1–6, kiểm tra hash/protected AST/secret scan trước commit. Chỉ stage source TODOs, skills, results và report, không stage .env.

   ```bash
   git commit -m hypotheses
   git commit --allow-empty -m "freeze skills"
   git tag freeze
   python -m lab.runner --condition baseline --tasks eval
   python -m lab.runner --condition subagents --tasks eval
   python -m lab.runner --condition skills-auto --tasks all
   python scripts/verify_freeze.py
   python -m lab.compare > report/table.md
   python scripts/check_breakdown.py
   pytest tests -q
   ```

6. Windows thực chạy các lệnh Python harness bên trong Docker qua helper tạm `.venv/lab-work/run.ps1`, image `day20-lab:local`. Source/tests/scripts và fixtures tasks mount read-only; skills mount read-only cho runner, writable chỉ curator. Results/report mount writable; main process nhận key qua env-file ignored, shell agent inherit_env=False. Helper chỉ dùng local, không nằm trong submission. Tái lập trên Linux clone dùng lệnh README ở trên và Dockerfile gốc; model API có thể không deterministic.
7. Khác biệt CRLF: test learning trong checkout Windows có CRLF trong khi checker hardcoded Git blob LF; lưu hai lượt code mini chẩn đoán rồi mount 35 task files xuất nguyên HEAD blob từ fixture tạm. Không sửa tasks/tests/checker và không đọc eval content trước freeze. verify_freeze chạy Linux cùng OS hash của runner; Git trong verifier đặt core.autocrlf=true để so sánh README kỹ năng giống cấu hình Git host, không sửa nội dung skills. Khi clone repo trên Linux, Git có thể có newline policy khác; phải giữ nguyên bytes SKILL.md đã dùng hoặc xác minh lại hashes trước tái lập.
8. Kết quả kiểm tra cuối: 29 passed in 9.20s; checked 6 runs of skill conditions: OK; 18 official run.json/trace.md + 3 development; mọi official error=null, skills_modified=false; ba skills không sửa tay; template/tests/tasks/scripts/protected helpers không đổi. Phần 6 mở rộng tùy chọn chưa làm. Các commit local không được push remote trong phiên này.

### Tài liệu tham khảo đã sử dụng

- README.md: thiết kế ba điều kiện, learn/eval và giới hạn xem evaluation.
- GUIDE.md: thứ tự checkpoint, taxonomy A–G, curator, hypotheses và freeze.
- RUBRIC.md: phạm vi bảo vệ, yêu cầu đủ artifacts và phân tích sáu câu hỏi.
- guides/pseudocode/01_agent.md, 02_subagents.md, 03_runner.md, 04_curator.md: contract triển khai.
- guides/pseudocode/05_skill_quality.md: cấu trúc, progressive disclosure và đánh giá nội dung skill.

Không trích dẫn kết quả paper hoặc giá model chưa được kiểm chứng. H1–H3 ở commit trước tag giữ nguyên trong báo cáo cuối; phần 8 nêu rõ giả thuyết nào phù hợp hoặc không phù hợp dữ liệu.
