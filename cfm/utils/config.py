import json
import os

def load_cfmrc():
    config_path = ".cfmrc"
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return {}
