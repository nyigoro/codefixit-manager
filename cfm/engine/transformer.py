import json
import re
from pathlib import Path
from shutil import copyfile
from difflib import unified_diff

def load_rules(rule_path):
    with open(rule_path, "r", encoding="utf-8") as f:
        return json.load(f)

def apply_rules(file_paths, rule_path, dry_run=False, backup=False, show_diff=False):
    rules = load_rules(rule_path)
    report = {
        "total_files_changed": 0,
        "per_rule": {rule["description"]: 0 for rule in rules},
        "per_file": {}
    }

    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original = content
        file_change_count = 0

        for rule in rules:
            pattern = rule["match"]
            replacement = rule["replace"]
            desc = rule["description"]

            matches = len(re.findall(pattern, content))
            if matches:
                content = re.sub(pattern, replacement, content)
                report["per_rule"][desc] += matches
                file_change_count += matches

        if content != original:
            report["total_files_changed"] += 1
            report["per_file"][file_path] = file_change_count

            print(f"✔ Matched in: {file_path} ({file_change_count} change(s))")
            if dry_run:
                print("⚠ Dry run only. No changes saved.")
                if show_diff:
                    diff = unified_diff(
                        original.splitlines(keepends=True),
                        content.splitlines(keepends=True),
                        fromfile=file_path + " (original)",
                        tofile=file_path + " (updated)"
                    )
                    print("".join(diff))
            else:
                if backup:
                    backup_path = file_path + ".bak"
                    copyfile(file_path, backup_path)
                    print(f"🗂️  Backup created: {backup_path}")

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print("✅ File updated.")
        else:
            print(f"⏩ No change: {file_path}")

    return report
