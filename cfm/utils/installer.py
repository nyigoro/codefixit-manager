import urllib.request
from pathlib import Path
import shutil

def install_rule_from_url(url: str):
    cache_dir = Path(".cfm_cache")
    cache_dir.mkdir(exist_ok=True)

    filename = Path(url).name
    dest_path = cache_dir / filename

    try:
        print(f"🌐 Downloading rule from: {url}")
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                print(f"❌ Failed to download rule (HTTP {response.status})")
                return
            with open(dest_path, "wb") as f:
                shutil.copyfileobj(response, f)

        print(f"✅ Installed rule to: {dest_path}")
    except Exception as e:
        print(f"❌ Failed to install rule: {e}")
