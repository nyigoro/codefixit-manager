#!/usr/bin/env python3
# cfm/cli.py

import argparse
import json
from cfm.engine.filewalker import collect_files
from cfm.engine.transformer import apply_rules
from cfm.utils.config import load_cfmrc
from cfm.utils.ruleloader import resolve_rule_path
from cfm.utils.htmlreport import generate_html_report
from cfm.utils.registry import list_available_rules
from cfm.utils.installer import install_rule_from_url
from cfm.utils.validator import validate_rule_file
from cfm.utils.generator import generate_rule_from_prompt
from cfm.utils.scaffold import init_rule_pack
from cfm.utils.testrunner import run_rule_tests
from cfm.utils.publish import publish_rule_pack
from cfm.utils.vscode import setup_vscode_workspace
from cfm.utils.watcher import watch_directory

def main():
    parser = argparse.ArgumentParser(description="CodeFixit Manager CLI")

    parser.add_argument("command", choices=[
        "fix", "dry-run", "list-rules", "install", "validate-rule", "rule-gen",
        "init", "test", "test-all", "vscode-hook", "publish", "watch", "prompt-test"
    ], help="Action to perform")

    parser.add_argument("--lang", help="Programming language (e.g. cpp, python)")
    parser.add_argument("--rule", nargs="+", help="One or more rule packs (e.g. qt5to6 modernizer)")
    parser.add_argument("--path", help="Directory to process")

    parser.add_argument("--dry-run", action="store_true", help="Alias for `dry-run` command")
    parser.add_argument("--backup", action="store_true", help="Create .bak backups before overwriting files")
    parser.add_argument("--diff", action="store_true", help="Show before/after diff in dry-run mode")
    parser.add_argument("--report", choices=["json", "html"], help="Output report format")

    parser.add_argument("--url", help="Rule pack URL to install (used with install)")
    parser.add_argument("--prompt", help="Natural language prompt (used with rule-gen)")
    parser.add_argument("--output", help="Output file path for rule-gen or validate-rule")

    parser.add_argument("--name", help="Used for `init` and `publish`")
    parser.add_argument("--test-dir", help="Test cases directory for `test`")

    args = parser.parse_args()

    # 🎯 COMMAND: list-rules
    if args.command == "list-rules":
        list_available_rules(args.lang or "cpp")
        return

    # 📦 COMMAND: install
    if args.command == "install":
        if not args.url:
            print("❌ --url is required with install")
            return
        install_rule_from_url(args.url)
        return

    # 🛠️ COMMAND: validate-rule
    if args.command == "validate-rule":
        if not args.output:
            print("❌ --output path required for validate-rule")
            return
        validate_rule_file(args.output)
        return

    # 🧠 COMMAND: rule-gen
    if args.command == "rule-gen":
        if not args.prompt or not args.output:
            print("❌ --prompt and --output are required for rule-gen")
            return
        generate_rule_from_prompt(args.prompt, args.output)
        return

    # 🧠 COMMAND: prompt-test
    if args.command == "prompt-test":
        interactive_rule_gen()
        return

    # 🧰 COMMAND: init
    if args.command == "init":
        if not args.name or not args.lang:
            print("❌ --name and --lang are required for init")
            return
        init_rule_pack(args.name, args.lang)
        return

    # 🧩 COMMAND: test
    if args.command == "test":
        if not args.rule or not args.test_dir:
            print("❌ --rule and --test-dir are required for test")
            return
        run_rule_tests(args.rule[0], args.test_dir)
        return

    # 🧪 COMMAND: test-all
    if args.command == "test-all":
        test_all_rules()
        return

    # 💻 COMMAND: vscode-hook
    if args.command == "vscode-hook":
        setup_vscode_workspace()
        return

    # 📦 COMMAND: publish
    if args.command == "publish":
        if not args.name or not args.lang:
            print("❌ --name and --lang are required for publish")
            return
        publish_rule_pack(args.name, args.lang)
        return

    # 🔁 COMMAND: watch
    if args.command == "watch":
        if not args.path or not args.lang or not args.rule:
            print("❌ Missing --path --lang --rule for watch")
            return
        watch_directory(args.path, args.lang, args.rule[0])
        return

    # 🧠 Load config from .cfmrc
    config = load_cfmrc()
    for key, value in config.items():
        current = getattr(args, key, None)
        if key == "rule" and isinstance(current, list) and current:
            continue
        if current in [None, False]:
            setattr(args, key, value)

    if not args.lang or not args.path or not args.rule:
        parser.error("Missing required arguments: --lang, --rule, or --path")

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

    if args.command == "dry-run" and combined_report["total_files_changed"] > 0:
        print("❌ CodeFixit found files that need formatting.")
        exit(1)
    elif args.command == "dry-run":
        print("✅ All files are up to date.")


if __name__ == "__main__":
    main()
