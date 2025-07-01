from pathlib import Path
import json

def setup_vscode_workspace():
    vscode_dir = Path(".vscode")
    vscode_dir.mkdir(exist_ok=True)

    tasks_path = vscode_dir / "tasks.json"
    launch_path = vscode_dir / "launch.json"
    workspace_path = Path(".code-workspace")

    # 🔧 tasks.json
    tasks = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Run cfm dry-run",
                "type": "shell",
                "command": "python3 cfm.py dry-run --lang cpp --rule qt5to6 --path src",
                "group": "build",
                "problemMatcher": []
            },
            {
                "label": "Run cfm test",
                "type": "shell",
                "command": "python3 cfm.py test --rule rules/cpp/qt5to6/qt5to6.json --test-dir rules/cpp/qt5to6/tests",
                "group": "test",
                "problemMatcher": []
            }
        ]
    }
    with open(tasks_path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)
    print(f"✅ Created: {tasks_path}")

    # 🐞 launch.json (optional)
    launch = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: cfm dry-run",
                "type": "python",
                "request": "launch",
                "program": "cfm.py",
                "args": ["dry-run", "--lang", "cpp", "--rule", "qt5to6", "--path", "src"],
                "console": "integratedTerminal"
            }
        ]
    }
    with open(launch_path, "w", encoding="utf-8") as f:
        json.dump(launch, f, indent=2)
    print(f"✅ Created: {launch_path}")

    # 🧠 .code-workspace
    workspace = {
        "folders": [{"path": "."}],
        "settings": {},
        "tasks": { "version": "2.0.0" },
        "launch": {}
    }
    with open(workspace_path, "w", encoding="utf-8") as f:
        json.dump(workspace, f, indent=2)
    print(f"✅ Created: {workspace_path}")
