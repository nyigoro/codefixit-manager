import difflib
from pathlib import Path
from cfm.engine.transformer import apply_rules

def run_rule_tests(rule_path, test_dir):
    test_dir = Path(test_dir)
    test_files = list(test_dir.glob("*.cpp"))  # simple assumption

    if not test_files:
        print(f"❌ No test files found in: {test_dir}")
        return

    passed = 0
    failed = 0

    for test_file in test_files:
        name = test_file.stem
        expected_path = test_dir / f"expected.{test_file.suffix.lstrip('.')}"
        if not expected_path.exists():
            print(f"⚠ Skipping test: {test_file.name} (no expected output)")
            continue

        input_code = test_file.read_text()
        expected_code = expected_path.read_text()

        # Apply rules directly to string
        result = apply_rules_to_string(input_code, rule_path)

        if result.strip() == expected_code.strip():
            print(f"✅ Passed: {test_file.name}")
            passed += 1
        else:
            print(f"❌ Failed: {test_file.name}")
            print_diff(expected_code, result)
            failed += 1

    print(f"\n📊 Test summary: {passed} passed, {failed} failed")


def apply_rules_to_string(code: str, rule_path: str) -> str:
    import json, re

    with open(rule_path, "r", encoding="utf-8") as f:
        rules = json.load(f)

    for rule in rules:
        code = re.sub(rule["match"], rule["replace"], code)

    return code


def print_diff(expected, actual):
    diff = difflib.unified_diff(
        expected.splitlines(),
        actual.splitlines(),
        fromfile='expected',
        tofile='actual',
        lineterm=''
    )
    for line in diff:
        print(line)
