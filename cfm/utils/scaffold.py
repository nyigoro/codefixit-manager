import os
import json
from pathlib import Path

def init_rule_pack(name, lang):
    base_dir = Path(f"rules/{lang}/{name}")
    rules_file = base_dir / f"{name}.json"
    readme_file = base_dir / "README.md"
    tests_dir = base_dir / "tests"

    if base_dir.exists():
        print(f"⚠ Rule pack already exists: {base_dir}")
        return

    print(f"📁 Creating rule pack: {name} ({lang})")
    base_dir.mkdir(parents=True)
    tests_dir.mkdir()

    # Empty rule list
    rule_content = [
        {
            "match": "QRegExp",
            "replace": "QRegularExpression",
            "description": "Upgrade QRegExp to QRegularExpression"
        }
    ]
    with open(rules_file, "w", encoding="utf-8") as f:
        json.dump(rule_content, f, indent=2)

    # README
    readme_file.write_text(f"# Rule Pack: {name}\n\nLanguage: `{lang}`\n\nDescribe the goal of this rule pack here.\n")

    # Sample test
    (tests_dir / "example.cpp").write_text("QRegExp regex(\"pattern\");\n")
    (tests_dir / "expected.cpp").write_text("QRegularExpression regex(\"pattern\");\n")

    print(f"✅ Rule pack created at: {base_dir}")
