#!/usr/bin/env python3

import argparse
from cfm.engine.filewalker import collect_files
from cfm.engine.transformer import apply_rules
from cfm.utils.config import load_cfmrc


def main():
    parser = argparse.ArgumentParser(description="CodeFixit Manager CLI")
    parser.add_argument("command", choices=["fix", "dry-run"], help="Action to perform")
parser.add_argument("--backup", action="store_true",
                        help="Create .bak backups before overwriting files")

parser.add_argument("--report", choices=["json"], help="Output report format")
report = apply_rules(
        files,
        rules_path,
        dry_run=(args.command == "dry-run"),
        backup=args.backup,
        show_diff=args.diff
    )

    parser.add_argument("--lang", required=True, help="Programming language (e.g. cpp, python)")
   parser.add_argument("--rule", required=True, nargs="+",
                    help="One or more rule packs (e.g. qt5to6 stylefix)")

    parser.add_argument("--path", required=True, help="Directory to process")

    parser.add_argument("--check", action="store_true",
                        help="Exit with non-zero if changes would be made (CI mode)")

    args = parser.parse_args()

    config = load_cfmrc()

    # Merge config fallback for missing CLI args
    for key, value in config.items():
        if getattr(args, key, None) in [None, False]:
            setattr(args, key, value)

   from cfm.utils.ruleloader import resolve_rule_path

files = collect_files(args.path, args.lang)

combined_report = {
    "total_files_changed": 0,
    "per_rule": {},
    "per_file": {}
}

for rule_name in args.rule:
    rules_path = resolve_rule_path(rule_name, args.lang)
    print(f"\n🔧 Applying rule set: {rule_name}")
    report = apply_rules(
        files,
        rules_path,
        dry_run=(args.command == "dry-run"),
        backup=args.backup,
        show_diff=args.diff
    )

    # Merge report
    combined_report["total_files_changed"] += report["total_files_changed"]
    for rule, count in report["per_rule"].items():
        combined_report["per_rule"][rule] = (
            combined_report["per_rule"].get(rule, 0) + count
        )
    for file, count in report["per_file"].items():
        combined_report["per_file"][file] = (
            combined_report["per_file"].get(file, 0) + count
        )

    # --- Summary output ---
    print("\n📊 Summary Report")
    print(f"🧾 Total files changed: {report['total_files_changed']}\n")

    print("📌 Changes by rule:")
    for rule, count in report["per_rule"].items():
        if count > 0:
            print(f"  • {rule}: {count} occurrence(s)")

    print("\n📂 Changes by file:")
    for file, count in report["per_file"].items():
        print(f"  • {file}: {count} replacement(s)")

    # --- CI check mode ---
    if args.check and report["total_files_changed"] > 0:
        print("\n❌ CodeFixIt check failed: changes are needed.")
        exit(1)
    elif args.check:
        print("\n✅ CodeFixIt check passed: no changes needed.")
        exit(0)

# --- Optional: Export report ---
    if args.report == "json":
        import json
        print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
