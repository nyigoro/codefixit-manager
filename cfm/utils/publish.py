import json
import shutil
from pathlib import Path
from cfm.utils.validator import validate_rule_file

def publish_rule_pack(name, lang):
    rule_dir = Path(f"rules/{lang}/{name}")
    rule_file = rule_dir / f"{name}.json"
    readme_file = rule_dir / "README.md"
    tests_dir = rule_dir / "tests"

    if not rule_file.exists():
        print(f"❌ Rule file not found: {rule_file}")
        return

    print(f"🔍 Validating rule file: {rule_file}")
    if not validate_rule_file(rule_file):
        print("❌ Validation failed. Fix issues before publishing.")
        return

    print(f"📦 Preparing rule pack for: {name} ({lang})")

    metadata = {
        "name": name,
        "language": lang,
        "description": readme_file.read_text().strip().split("\n")[0] if readme_file.exists() else "",
        "rule_file": f"{name}.json",
        "test_dir": "tests",
        "version": "1.0.0",
        "url": f"https://github.com/build-africa-eng/codefixit-manager/tree/main/rules/{lang}/{name}"
    }

    metadata_path = rule_dir / "metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"✅ metadata.json created at: {metadata_path}")

    # Optional zip
    archive_path = Path(f"dist/{lang}_{name}.zip")
    archive_path.parent.mkdir(exist_ok=True)

    shutil.make_archive(str(archive_path.with_suffix("")), 'zip', rule_dir)
    print(f"📦 Created archive: {archive_path}")

    print("\n🚀 Next steps:")
    print(f"1. Commit and push your rule pack to GitHub.")
    print(f"2. Optionally publish release with:")
    print(f"   gh release create v1.0.0 {archive_path} --title '{name} rule pack'")
