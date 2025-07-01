import os
import openai

def generate_rule_from_prompt(prompt, output_path):
    api_key = os.getenv("OPENAI_API_KEY") or load_cfmrc().get("openai_api_key")
    if not api_key:
        print("❌ No OpenAI API key found in environment or config")
        return

    openai.api_key = api_key

    print("🤖 Contacting LLM to generate rule...")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a code refactoring rule assistant."},
            {"role": "user", "content": f"Create a regex-based code transformation rule for: {prompt}"}
        ]
    )

    text = response.choices[0].message.content
    try:
        rule = json.loads(text)
    except:
        print("⚠️ Model did not return valid JSON. Showing raw:")
        print(text)
        return

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rule, f, indent=2)

    print(f"✅ AI-generated rule saved to: {output_path}")

