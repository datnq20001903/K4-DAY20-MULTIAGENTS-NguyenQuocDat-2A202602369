### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Assistant
[{'arguments': '{"path":"workspace"}', 'call_id': 'call_NiXxIO4wul20UpcqbC6LD9To', 'name': 'ls', 'type': 'function_call', 'id': 'fc_04d2ae7a289e390c006ac47cd5ec4087d0984e93b83ba2a1b1', 'status': 'completed'}]

### Tool call: ls
{"path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Assistant
[{'arguments': '{"path":"workspace/bookings"}', 'call_id': 'call_xgnJZuNrFAiLaMHSYpLrVcpj', 'name': 'ls', 'type': 'function_call', 'id': 'fc_04d2ae7a289e390c006ac47cd7a09087d087e9c9ada4424668', 'status': 'completed'}]

### Tool call: ls
{"path": "workspace/bookings"}

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py']

### Assistant
[{'arguments': '{"file_path":"workspace/bookings/billing.py","offset":0,"limit":300}', 'call_id': 'call_8UdRqNH9R8i2Uqd4razdLoz3', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_04d2ae7a289e390c006ac47cda65fc87d09818335336d3f4ad', 'status': 'completed'}, {'arguments': '{"file_path":"workspace/bookings/calendar_export.py","offset":0,"limit":300}', 'call_id': 'call_Lw4cJZl2K5GP2XjQ2BnTw9uJ', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_04d2ae7a289e390c006ac47cda660c87d097ebdc9f4d79e207', 'status': 'completed'}, {'arguments': '{"file_path":"workspace/bookings/schedule.py","offset":0,"limit":300}', 'call_id': 'call_iA19idR8h6Ka4nyB86tGAiEm', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_04d2ae7a289e390c006ac47cda661487d0906903b9eb14e844', 'status': 'completed'}, {'arguments': '{"file_path":"workspace/bookings/timeutil.py","offset":0,"limit":300}', 'call_id': 'call_ISkYl1LwQMMJsAYUYs8VTqFQ', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_04d2ae7a289e390c006ac47cda661c87d08f3c0219f4ab41d3', 'status': 'completed'}, {'arguments': '{"file_path":"workspace/bookings/__init__.py","offset":0,"limit":200}', 'call_id': 'call_pUBFkbWdaMpoberjaoeADPJP', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_04d2ae7a289e390c006ac47cda662487d097cbc09d3bbb1892', 'status': 'completed'}, {'arguments': '{"path":"workspace/tests"}', 'call_id': 'call_tEn3PtqwPUL3tcmgLp6CZ6Zw', 'name': 'ls', 'type': 'function_call', 'id': 'fc_04d2ae7a289e390c006ac47cda662887d097

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py", "offset": 0, "limit": 300}

### Tool call: read_file
{"file_path": "workspace/bookings/calendar_export.py", "offset": 0, "limit": 300}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py", "offset": 0, "limit": 300}

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py", "offset": 0, "limit": 300}

### Tool call: read_file
{"file_path": "workspace/bookings/__init__.py", "offset": 0, "limit": 200}

### Tool call: ls
{"path": "workspace/tests"}

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
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

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
@@ lines 1-1 of 1 @@
__version__ = "1.4.2"

### Tool result
['/workspace/tests/test_bookings.py']

### Assistant
[{'arguments': '{"file_path":"workspace/tests/test_bookings.py","offset":0,"limit":300}', 'call_id': 'call_YuxYx6q6wARUj7K18Vsxpbxb', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_04d2ae7a289e390c006ac47cdcf48087d0a54b31f1231febb4', 'status': 'completed'}]

### Tool call: read_file
{"file_path": "workspace/tests/test_bookings.py", "offset": 0, "limit": 300}

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
[{'arguments': '{"command":"python -m pytest -q workspace/tests","timeout":120}', 'call_id': 'call_gJqr8cF7WfVBBpaWIfw7uJNU', 'name': 'execute', 'type': 'function_call', 'id': 'fc_04d2ae7a289e390c006ac47cdea04887d09182c73a3ce25765', 'status': 'completed'}]

### Tool call: execute
{"command": "python -m pytest -q workspace/tests", "timeout": 120}

### Tool result

==================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py _______________
ImportError while importing test module '/tmp/day20-lab-vyede8ni/workspace/tests/test_bookings.py'.
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
1 error in 0.08s

Exit code: 2
[Command failed with exit code 2]

### Assistant
[{'arguments': '{"command":"PYTHONPATH=workspace python -m pytest -q workspace/tests","timeout":120}', 'call_id': 'call_FlZD3oTeNR4jQTrVJtad1n9x', 'name': 'execute', 'type': 'function_call', 'id': 'fc_04d2ae7a289e390c006ac47ce1c5b887d0b461e363bc111845', 'status': 'completed'}]

### Tool call: execute
{"command": "PYTHONPATH=workspace python -m pytest -q workspace/tests", "timeout": 120}

### Tool result
FF.                                                                      [100%]
=================================== FAILURES ===================================
_______________________ test_total_minutes_mixed_formats _______________________

    def test_total_minutes_mixed_formats():
>       assert total_minutes(["1h30m", "2h"]) == 210
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

workspace/tests/test_bookings.py:6: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
workspace/bookings/schedule.py:7: in total_minutes
    return sum(parse_duration(d) for d in durations)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
workspace/bookings/schedule.py:7: in <genexpr>
    return sum(parse_duration(d) for d in durations)
               ^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

text = '2h'

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
>           raise ValueError(f"bad duration: {text!r}")
E           ValueError: bad duration: '2h'

workspace/bookings/timeutil.py:18: ValueError
________________________ test_billable_blocks_rounds_up __

### Assistant
[{'arguments': '{"file_path":"workspace/bookings/billing.py","old_string":"    return round(minutes / block)\\n","new_string":"    if minutes < 0:\\n        raise ValueError(\\"minutes must be non-negative\\")\\n    if block <= 0:\\n        raise ValueError(\\"block must be positive\\")\\n    return (minutes + block - 1) // block\\n","replace_all":false}', 'call_id': 'call_Tp6pJ8CSFNV3TKYZTC6iSzc9', 'name': 'edit_file', 'type': 'function_call', 'id': 'fc_04d2ae7a289e390c006ac47ce6985087d0861243a96fefc515', 'status': 'completed'}]

### Tool call: edit_file
{"file_path": "workspace/bookings/billing.py", "old_string": "    return round(minutes / block)\n", "new_string": "    if minutes < 0:\n        raise ValueError(\"minutes must be non-negative\")\n    if block <= 0:\n        raise ValueError(\"block must be positive\")\n    return (minutes + block - 1) // block\n", "replace_all": false}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/billing.py'

### Assistant
[{'arguments': '{"file_path":"workspace/bookings/schedule.py","old_string":"def add_slot(slot, slots=[]):\\n    \\"\\"\\"Return a NEW list containing the given slots plus `slot`.\\n\\n    Separate calls must not share state: calling add_slot(\\"a\\") and then\\n    add_slot(\\"b\\") returns [\\"a\\"] and then [\\"b\\"].\\n    \\"\\"\\"\\n    slots.append(slot)\\n    return slots\\n","new_string":"def add_slot(slot, slots=None):\\n    \\"\\"\\"Return a NEW list containing the given slots plus `slot`.\\n\\n    Separate calls must not share state: calling add_slot(\\"a\\") and then\\n    add_slot(\\"b\\") returns [\\"a\\"] and then [\\"b\\"].\\n    \\"\\"\\"\\n    return [*(slots or []), slot]\\n","replace_all":false}', 'call_id': 'call_fvzqnBTBqf2OsX8NgQf7LGrR', 'name': 'edit_file', 'type': 'function_call', 'id': 'fc_04d2ae7a289e390c006ac47ce922a487d086e1b9a26ef69493', 'status': 'completed'}]

### Tool call: edit_file
{"file_path": "workspace/bookings/schedule.py", "old_string": "def add_slot(slot, slots=[]):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    slots.append(slot)\n    return slots\n", "new_string": "def add_slot(slot, slots=None):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    return [*(slots or []), slot]\n", "replace_all": false}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/schedule.py'

### Assistant
[{'arguments': '{"file_path":"workspace/bookings/timeutil.py","old_string":"    m = re.fullmatch(r\\"(\\\\d+)h(\\\\d+)m\\", text.strip())\\n    if not m:\\n        raise ValueError(f\\"bad duration: {text!r}\\")\\n    return int(m.group(1)) * 60 + int(m.group(2))\\n","new_string":"    if not isinstance(text, str):\\n        raise ValueError(f\\"bad duration: {text!r}\\")\\n\\n    value = text.strip()\\n    patterns = (\\n        (r\\"(\\\\d+)h(\\\\d+)m\\", lambda match: int(match.group(1)) * 60 + int(match.group(2))),\\n        (r\\"(\\\\d+)h\\", lambda match: int(match.group(1)) * 60),\\n        (r\\"(\\\\d+)m\\", lambda match: int(match.group(1))),\\n        (r\\"(\\\\d+):(\\\\d+)\\", lambda match: int(match.group(1)) * 60 + int(match.group(2))),\\n        (r\\"(\\\\d+)\\", lambda match: int(match.group(1))),\\n    )\\n    for pattern, convert in patterns:\\n        match = re.fullmatch(pattern, value)\\n        if match:\\n            return convert(match)\\n    raise ValueError(f\\"bad duration: {text!r}\\")\\n","replace_all":false}', 'call_id': 'call_d0JqrbRQuh5NBqGiCLamsy1S', 'name': 'edit_file', 'type': 'function_call', 'id': 'fc_04d2ae7a289e390c006ac47cec1aa887d0b52a699301ae7400', 'status': 'completed'}]

### Tool call: edit_file
{"file_path": "workspace/bookings/timeutil.py", "old_string": "    m = re.fullmatch(r\"(\\d+)h(\\d+)m\", text.strip())\n    if not m:\n        raise ValueError(f\"bad duration: {text!r}\")\n    return int(m.group(1)) * 60 + int(m.group(2))\n", "new_string": "    if not isinstance(text, str):\n        raise ValueError(f\"bad duration: {text!r}\")\n\n    value = text.strip()\n    patterns = (\n        (r\"(\\d+)h(\\d+)m\", lambda match: int(match.group(1)) * 60 + int(match.group(2))),\n        (r\"(\\d+)h\", lambda match: int(match.group(1)) * 60),\n        (r\"(\\d+)m\", lambda match: int(match.group(1))),\n        (r\"(\\d+):(\\d+)\", lambda match: int(match.group(1)) * 60 + int(match.group(2))),\n        (r\"(\\d+)\", lambda match: int(match.group(1))),\n    )\n    for pattern, convert in patterns:\n        match = re.fullmatch(pattern, value)\n        if match:\n            return convert(match)\n    raise ValueError(f\"bad duration: {text!r}\")\n", "replace_all": false}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/timeutil.py'

### Assistant
[{'arguments': '{"command":"PYTHONPATH=workspace python -m pytest -q workspace/tests","timeout":120}', 'call_id': 'call_NZwCOGNeP1SjNa3G3oXf20Vo', 'name': 'execute', 'type': 'function_call', 'id': 'fc_04d2ae7a289e390c006ac47cf00d0887d0a7cfd7165636c6a3', 'status': 'completed'}]

### Tool call: execute
{"command": "PYTHONPATH=workspace python -m pytest -q workspace/tests", "timeout": 120}

### Tool result
...                                                                      [100%]
3 passed in 0.01s

[Command succeeded with exit code 0]

### Assistant
[{'arguments': '{"file_path":"workspace/bookings/schedule.py","old_string":"    return [*(slots or []), slot]\\n","new_string":"    return [*([] if slots is None else slots), slot]\\n","replace_all":false}', 'call_id': 'call_3Wx2Xq8EjH7YcIMxiBqZ8l7z', 'name': 'edit_file', 'type': 'function_call', 'id': 'fc_04d2ae7a289e390c006ac47cf33bbc87d0babbb0a3b2c43a3f', 'status': 'completed'}]

### Tool call: edit_file
{"file_path": "workspace/bookings/schedule.py", "old_string": "    return [*(slots or []), slot]\n", "new_string": "    return [*([] if slots is None else slots), slot]\n", "replace_all": false}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/schedule.py'

### Assistant
[{'arguments': '{"command":"PYTHONPATH=workspace python -m pytest -q workspace/tests","timeout":120}', 'call_id': 'call_Q8EC5GiSUjjG9W0tNBrXyeI3', 'name': 'execute', 'type': 'function_call', 'id': 'fc_04d2ae7a289e390c006ac47cf51d4487d09d531b61357e39ef', 'status': 'completed'}]

### Tool call: execute
{"command": "PYTHONPATH=workspace python -m pytest -q workspace/tests", "timeout": 120}

### Tool result
...                                                                      [100%]
3 passed in 0.01s

[Command succeeded with exit code 0]

### Assistant
[{'type': 'text', 'text': 'Fixed duration parsing to support every documented format, changed billing to round partial blocks up and reject negative minutes, and made `add_slot` return a new list without shared state. The test suite passes.', 'annotations': [], 'id': 'msg_04d2ae7a289e390c006ac47cf7c9e887d0903255e48cea7ee3', 'phase': 'final_answer'}]