import json
from pathlib import Path

def validate_rule_file(rule_path):
    path = Path(rule_path)

    if not path.exists():
        print(f"❌ File does not exist: {rule_path}")
        return False

    try:
        with open(path, "r", encoding="utf-8") as f:
            rules = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False

    if not isinstance(rules, list):
        print("❌ Rule file must contain a list of rule objects.")
        return False

    errors = []
    for i, rule in enumerate(rules):
        if not isinstance(rule, dict):
            errors.append(f"Rule {i+1} is not an object.")
            continue
        for key in ["match", "replace", "description"]:
            if key not in rule:
                errors.append(f"Rule {i+1} missing '{key}'")

    if errors:
        print("❌ Validation failed:")
        for e in errors:
            print("   -", e)
        return False

    print(f"✅ Rule file is valid: {len(rules)} rule(s) found.")
    return True
