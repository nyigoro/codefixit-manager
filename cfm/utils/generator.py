import os
import sys
import json

def load_cfmrc():
    """Load ~/.cfmrc if it exists"""
    cfmrc_path = os.path.expanduser("~/.cfmrc")
    if os.path.exists(cfmrc_path):
        try:
            with open(cfmrc_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Failed to parse ~/.cfmrc. Please check the format.")
    return {}

def generate_rule_from_prompt(prompt, output_path):
    # Skip entirely if in GitHub Actions or CI
    if os.environ.get("CI") or not sys.stdin.isatty():
        print("⚠️ Skipping AI rule generation in CI or non-interactive environment.")
        return

    try:
        import openai
    except ImportError:
        print("❌ Missing `openai` package. Run: pip install .[ai]")
        return

    # Try to load API key from env or config
    api_key = os.getenv("OPENAI_API_KEY") or load_cfmrc().get("openai_api_key")
    if not api_key:
        print("❌ No OpenAI API key found in environment or ~/.cfmrc.")
        return

    openai.api_key = api_key

    print("🤖 Contacting LLM to generate rule...")
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

    text = response.choices[0].message.content
    try:
        rule = json.loads(text)
    except json.JSONDecodeError:
        print("⚠️ Model did not return valid JSON. Showing raw output:\n")
        print(text)
        return

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rule, f, indent=2)

    print(f"✅ AI-generated rule saved to: {output_path}")
