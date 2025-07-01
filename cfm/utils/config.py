import os
import json
from pathlib import Path

def load_cfmrc():
    # Look for local first, then global
    local_path = Path(".cfmrc")
    global_path = Path.home() / ".cfmrc"

    for path in [local_path, global_path]:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠ Failed to parse config at {path}: {e}")
                return {}
    return {}
