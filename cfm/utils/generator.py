import os
import sys
import json

def load_cfmrc():
    """Load ~/.cfmrc if available"""
    path = os.path.expanduser("~/.cfmrc")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Invalid JSON in ~/.cfmrc")
    return {}

def generate_rule_from_prompt(prompt, output_path):
    # 🚫 Skip LLM logic in CI or GitHub Actions
    if os.environ.get("CI") or not sys.stdin.isatty():
        print("⚠️ Skipping AI rule generation in CI or non-interactive environment.")
        return

    try:
        import openai
    except ImportError:
        print("❌ Missing `openai` package. Run: pip install .[ai]")
        return

    # Prefer environment variable (used in GitHub Actions secrets)
    api_key = os.getenv("OPENAI_API_KEY") or load_cfmrc().get("openai_api_key")
    if not api_key:
        print("❌ No OpenAI API key found in env or ~/.cfmrc")
        return

    openai.api_key = api_key

    print("🤖 Generating rule via OpenAI...")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a code refactoring rule assistant."},
                {"role": "user", "content": f"Create a regex-based code transformation rule for: {prompt}"}
            ]
        )
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return

    content = response.choices[0].message.content
    try:
        rule = json.loads(content)
    except json.JSONDecodeError:
        print("⚠️ Model output was not valid JSON. Showing raw text:\n")
        print(content)
        return

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rule, f, indent=2)

    print(f"✅ Rule saved to {output_path}")
