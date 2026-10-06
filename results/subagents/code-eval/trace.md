### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Assistant
[{'arguments': '{"description":"Inspect the bookings package and tests in workspace/, determine documented requirements and failing behavior. Do not modify files. Report relevant source paths, test commands, and a concise implementation plan including edge cases.","subagent_type":"explorer"}', 'call_id': 'call_lqj4zCE8XFsYZZJc5ohpawda', 'name': 'task', 'type': 'function_call', 'id': 'fc_062afba2da59c364006ac47cd5ecd087d0b8798b42feac6fa7', 'status': 'completed'}]

### Tool call: task
{"description": "Inspect the bookings package and tests in workspace/, determine documented requirements and failing behavior. Do not modify files. Report relevant source paths, test commands, and a concise implementation plan including edge cases.", "subagent_type": "explorer"}

### Tool result
## Findings

The documented test command is:

```sh
cd workspace && python -m pytest tests -q
```

I ran it from the sandbox root. **Result: 2 failed, 1 passed.**

### Verified requirements and failures

- **Duration parsing** — `workspace/bookings/timeutil.py` documents support for `1h30m`, `2h`, `45m`, `1:30`, and bare minutes such as `45`, with surrounding whitespace ignored. It currently accepts only the `NhNm` form, so `2h` fails with `ValueError`. This breaks `total_minutes(["1h30m", "2h"])` in `workspace/bookings/schedule.py` and the corresponding test.
- **Billing blocks** — `workspace/bookings/billing.py` documents rounding partial blocks **up** and says negative minutes raise `ValueError`. The implementation uses `round(minutes / block)`, which rounds `20 / 15` to 1 rather than 2. The billing test fails on that assertion. The negative-input requirement is documented but not covered by the current tests.
- **Slot list isolation** — `workspace/bookings/schedule.py` documents that separate calls to `add_slot` must not share state. Its default argument is a shared list and the function mutates it. The existing test checks only one call, so it passes; repeated calls can expose the defect.
- **Calendar export dependency** — `workspace/bookings/calendar_export.py` uses the shared `parse_duration` helper in `slot_end`. Fixing duration parsing there also affects calendar slot-end calculations. No calendar-export test is present in the inspected test file.

### Relevant paths

### Assistant
[{'arguments': '{"path":"workspace"}', 'call_id': 'call_3g5vJOVSAsmUoRicJuludA5C', 'name': 'ls', 'type': 'function_call', 'id': 'fc_062afba2da59c364006ac47cecdac887d0a033f44cc0c9e2eb', 'status': 'completed'}, {'arguments': '{"pattern":"**/*.py","path":"workspace"}', 'call_id': 'call_ulWXx5uYfzvsnJmGqQZlzwjU', 'name': 'glob', 'type': 'function_call', 'id': 'fc_062afba2da59c364006ac47cecdadc87d0bf648d3d89ed4fd8', 'status': 'completed'}]

### Tool call: ls
{"path": "workspace"}

### Tool call: glob
{"pattern": "**/*.py", "path": "workspace"}

### Tool result
['/workspace/.pytest_cache/', '/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/test_bookings.py']

### Assistant
[{'arguments': '{"file_path":"workspace/bookings/timeutil.py","offset":0,"limit":200}', 'call_id': 'call_XxoustotNkPcBzLcqJpDSfYl', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_062afba2da59c364006ac47cef8b5487d0a2be35ab9abf12a7', 'status': 'completed'}, {'arguments': '{"file_path":"workspace/bookings/billing.py","offset":0,"limit":200}', 'call_id': 'call_3XktENNTM3104px6WjqysJo2', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_062afba2da59c364006ac47cef8b6887d08d15f13b304896ac', 'status': 'completed'}, {'arguments': '{"file_path":"workspace/bookings/schedule.py","offset":0,"limit":200}', 'call_id': 'call_OJAc8nQXDkaDGK21a3lFK0LY', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_062afba2da59c364006ac47cef8b7487d09cfbd6e274a4bf3e', 'status': 'completed'}, {'arguments': '{"file_path":"workspace/bookings/calendar_export.py","offset":0,"limit":200}', 'call_id': 'call_aBdumJXM72pDCX6nqFVjlySq', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_062afba2da59c364006ac47cef8b7c87d0b5f02abecefaac54', 'status': 'completed'}, {'arguments': '{"file_path":"workspace/README.md","offset":0,"limit":200}', 'call_id': 'call_frZTRTEn510lUBcXW9K1VsHe', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_062afba2da59c364006ac47cef8b8887d0bfa90104830a7c98', 'status': 'completed'}, {'arguments': '{"file_path":"workspace/tests/test_bookings.py","offset":0,"limit":200}', 'call_id': 'call_Luj2Iv3BbU3NKCY2Dmx0GlPI', 'name': 'read_file', 'type': 'function_call', 'id':

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py", "offset": 0, "limit": 200}

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py", "offset": 0, "limit": 200}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py", "offset": 0, "limit": 200}

### Tool call: read_file
{"file_path": "workspace/bookings/calendar_export.py", "offset": 0, "limit": 200}

### Tool call: read_file
{"file_path": "workspace/README.md", "offset": 0, "limit": 200}

### Tool call: read_file
{"file_path": "workspace/tests/test_bookings.py", "offset": 0, "limit": 200}

### Tool result
@@ lines 1-19 of 19 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
    if not m:
        raise ValueError(f"bad duration: {text!r}")
    return int(m.group(1)) * 60 + int(m.group(2))

### Tool result
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)

### Tool result
@@ lines 1-17 of 17 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    slots.append(slot)
    return slots

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

### Tool result
@@ lines 1-5 of 5 @@
# bookings

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Assistant
[{'arguments': '{"description":"Implement the documented fixes in workspace/bookings only (do not modify tests): parse_duration must support all documented formats with whitespace and reject malformed values; billable_blocks must round partial blocks up and reject negative minutes; add_slot must avoid shared default state and return a new list. Follow conventional Python style, handle sensible invalid block sizes. Run tests from workspace and report changed files/results.","subagent_type":"implementer"}', 'call_id': 'call_tTcoWlfkpCLqO5B99oJLxkkr', 'name': 'task', 'type': 'function_call', 'id': 'fc_062afba2da59c364006ac47cf12ecc87d0913de2956b40ef8e', 'status': 'completed'}]

### Tool call: task
{"description": "Implement the documented fixes in workspace/bookings only (do not modify tests): parse_duration must support all documented formats with whitespace and reject malformed values; billable_blocks must round partial blocks up and reject negative minutes; add_slot must avoid shared default state and return a new list. Follow conventional Python style, handle sensible invalid block sizes. Run tests from workspace and report changed files/results.", "subagent_type": "implementer"}

### Tool result
Implemented the fixes in `workspace/bookings`:

- `timeutil.py`: supports all documented duration formats, including whitespace, and rejects malformed or non-string inputs with `ValueError`.
- `billing.py`: rounds partial blocks up and rejects negative minutes and non-positive block sizes.
- `schedule.py`: removes the shared mutable default and returns a new list on every call.

**Verification:** `cd workspace && python -m pytest tests -q` — 3 passed. Additional checks for duration formats and malformed inputs, billing edge cases, and list independence also passed. No tests were modified.

### Assistant
[{'arguments': '{"file_path":"workspace/bookings/timeutil.py","offset":0,"limit":200}', 'call_id': 'call_TZpfxK0nEap0rWMjx4JMur3y', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_062afba2da59c364006ac47d1d2d0487d0a0dbde6cd43d3cdc', 'status': 'completed'}, {'arguments': '{"file_path":"workspace/bookings/billing.py","offset":0,"limit":200}', 'call_id': 'call_QBMVxsDmSzha3L8GWaWBDfEG', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_062afba2da59c364006ac47d1d2d1c87d085814f8d186fe534', 'status': 'completed'}, {'arguments': '{"file_path":"workspace/bookings/schedule.py","offset":0,"limit":200}', 'call_id': 'call_zRBliokQbC875IkivSzxmwZS', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_062afba2da59c364006ac47d1d2d2887d0b42235e69e386a47', 'status': 'completed'}, {'arguments': '{"command":"python -m pytest workspace/tests -q","timeout":120}', 'call_id': 'call_UQjV1KwDQUSg7Au2vDmResYs', 'name': 'execute', 'type': 'function_call', 'id': 'fc_062afba2da59c364006ac47d1d2d3087d0920d20996a8f34ca', 'status': 'completed'}]

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py", "offset": 0, "limit": 200}

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py", "offset": 0, "limit": 200}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py", "offset": 0, "limit": 200}

### Tool call: execute
{"command": "python -m pytest workspace/tests -q", "timeout": 120}

### Tool result
@@ lines 1-31 of 31 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    if not isinstance(text, str):
        raise ValueError(f"bad duration: {text!r}")

    value = text.strip()
    patterns = (
        (r"(\d+)\s*h\s*(\d+)\s*m", lambda m: int(m.group(1)) * 60 + int(m.group(2))),
        (r"(\d+)\s*h", lambda m: int(m.group(1)) * 60),
        (r"(\d+)\s*m", lambda m: int(m.group(1))),
        (r"(\d+)\s*:\s*(\d+)", lambda m: int(m.group(1)) * 60 + int(m.group(2))),
        (r"\d+", lambda m: int(m.group(0))),
    )
    for pattern, convert in patterns:
        match = re.fullmatch(pattern, value)
        if match:
            return convert(match)
    raise ValueError(f"bad duration: {text!r}")

### Tool result
@@ lines 1-15 of 15 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    if minutes < 0:
        raise ValueError("minutes must be non-negative")
    if block <= 0:
        raise ValueError("block must be positive")
    return (minutes + block - 1) // block

### Tool result
@@ lines 1-16 of 16 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=None):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    return [*(slots if slots is not None else []), slot]

### Tool result

==================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py _______________
ImportError while importing test module '/tmp/day20-lab-ewaq85x0/workspace/tests/test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/local/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
workspace/tests/test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ============================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.09s

Exit code: 2
[Command failed with exit code 2]

### Assistant
[{'arguments': '{"command":"cd workspace && python -m pytest tests -q","timeout":120}', 'call_id': 'call_IUTHs3TzwrEnoqg0dJJ6AQ3I', 'name': 'execute', 'type': 'function_call', 'id': 'fc_062afba2da59c364006ac47d20eabc87d08a57244627ec7e71', 'status': 'completed'}]

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q", "timeout": 120}

### Tool result
...                                                                      [100%]
3 passed in 0.01s

[Command succeeded with exit code 0]

### Assistant
[{'type': 'text', 'text': 'Updated `workspace/bookings/timeutil.py` to parse all documented duration formats, `billing.py` to round partial blocks up and reject invalid inputs, and `schedule.py` to avoid shared list state. The test suite passes: **3 passed**.', 'annotations': [], 'id': 'msg_062afba2da59c364006ac47d24996487d0b70215e38353a2f5', 'phase': 'final_answer'}]