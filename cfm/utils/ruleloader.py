import os
from pathlib import Path
import urllib.request

def resolve_rule_path(rule_arg, lang):
    # Case 1: direct path (absolute or relative)
    if Path(rule_arg).exists():
        return rule_arg

    # Case 2: URL
    if rule_arg.startswith("http://") or rule_arg.startswith("https://"):
        temp_path = Path(".cfm_cache")
        temp_path.mkdir(exist_ok=True)
        dest = temp_path / f"{Path(rule_arg).name}"
        urllib.request.urlretrieve(rule_arg, dest)
        print(f"🌐 Downloaded external rule: {rule_arg}")
        return str(dest)

    # Case 3: built-in rule
    built_in_path = f"rules/{lang}/{rule_arg}.json"
    if Path(built_in_path).exists():
        return built_in_path

    raise FileNotFoundError(f"❌ Could not find rule: {rule_arg}")
