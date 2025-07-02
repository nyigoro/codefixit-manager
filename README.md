
# 🛠️ CodeFixit Manager (CFM)

> Modernize, refactor, and auto-fix legacy code using customizable transformation rules.

[![Test Rules](https://github.com/nyigoro/codefixit-manager/actions/workflows/test-rules.yml/badge.svg)](https://github.com/nyigoro/codefixit-manager/actions)

---

## 📦 Install

### Option 1: From Source (Dev Mode)

```bash
git clone https://github.com/build-africa-eng/codefixit-manager.git
cd codefixit-manager
python3 cfm.py --help
````

---

## ⚙ Supported Commands

| Command           | Purpose                                     |
| ----------------- | ------------------------------------------- |
| `fix` / `dry-run` | Apply rules or preview changes              |
| `list-rules`      | Show available local rules                  |
| `init`            | Scaffold new rule pack                      |
| `test`            | Run rule-based tests (input → expected)     |
| `rule-gen`        | Generate rules from natural language prompt |
| `validate-rule`   | Lint and check rule JSON syntax             |
| `publish`         | Package and prepare rule pack for release   |
| `vscode-hook`     | Auto-generate `.vscode` dev setup           |

---

## 🧠 Example

```bash
cfm init --name qt5to6 --lang cpp
cfm fix --lang cpp --rule qt5to6 --path ./src
cfm test --rule rules/cpp/qt5to6/qt5to6.json --test-dir rules/cpp/qt5to6/tests
```


