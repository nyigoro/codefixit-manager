#!/usr/bin/env python3

import argparse
from cfm.engine.filewalker import collect_files
from cfm.engine.transformer import apply_rules
from cfm.utils.config import load_cfmrc
from cfm.utils.ruleloader import resolve_rule_path
from cfm.utils.htmlreport import generate_html_report
import json

def main():
    parser = argparse.ArgumentParser(description="CodeFixit Manager CLI")

    parser.add_argument("command", choices=["fix", "dry-run"], help="Action to perform")
    parser.add_argument("--lang", help="Programming language (e.g. cpp, python)")
    parser.add_argument("--rule", required=True, nargs="+", help="One or more rule packs (e.g. qt5to6 modernizer)")
    parser.add_argument("--path", help="Directory to process")

    parser.add_argument("--dry-run", action="store_true", help="Alias for `dry-run` command")
    parser.add_argument("--backup", action="store_true", help="Create .bak backups before overwriting files")
    parser.add_argument("--diff", action="store_true", help="Show before/after diff in dry-run mode")
    parser.add_argument("--report", choices=["json", "html"], help="Output report format")

    args = parser.parse_args()

    # 🧠 Load config from .cfmrc (if needed)
    config = load_cfmrc()
    for key, value in config.items():
        current = getattr(args, key, None)
        if key == "rule" and isinstance(current, list) and current:
            continue
        if current in [None, False]:
            setattr(args, key, value)

    if not args.lang or not args.path:
        parser.error("Missing required arguments: --lang and/or --path")

    files = collect_files(args.path, args.lang)

    # 🔁 Run each rule pack in order
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

        # 🧩 Merge results
        combined_report["total_files_changed"] += report["total_files_changed"]
        for rule, count in report["per_rule"].items():
            combined_report["per_rule"][rule] = combined_report["per_rule"].get(rule, 0) + count
        for file, count in report["per_file"].items():
            combined_report["per_file"][file] = combined_report["per_file"].get(file, 0) + count

    # 📤 Report output
    if args.report == "json":
        print(json.dumps(combined_report, indent=2))
    elif args.report == "html":
        generate_html_report(combined_report)

if __name__ == "__main__":
    main()
