import os
from pathlib import Path

def list_available_rules(lang="cpp"):
    local_dir = Path(f"rules/{lang}")
    external_dir = Path(".cfm_cache")

    print(f"\n📦 Available Rule Packs ({lang}):\n")

    if local_dir.exists():
        for f in sorted(local_dir.glob("*.json")):
            name = f.stem
            print(f"  • {name.ljust(15)} ({f})")
    else:
        print("  ⚠ No local rules found.")

    print("\n📦 Installed External Packs:\n")
    if external_dir.exists():
        for f in sorted(external_dir.glob("*.json")):
            name = f.stem
            print(f"  • {name.ljust(15)} ({f})")
    else:
        print("  (empty)")

    print("\n🛰️ Remote Registry Support: ⏳ coming soon\n")
