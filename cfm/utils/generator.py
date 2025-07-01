import json
from pathlib import Path

def generate_rule_from_prompt(prompt, output_path):
    print(f"🧠 Generating rule from prompt: \"{prompt}\"")

    # 💡 Basic example: 1-to-1 literal replace
    tokens = prompt.lower().split("replace ")
    if len(tokens) < 2 or " with " not in tokens[1]:
        print("❌ Invalid prompt format. Use: 'Replace X with Y'")
        return

    lhs_rhs = tokens[1].split(" with ")
    if len(lhs_rhs) != 2:
        print("❌ Could not parse replacement")
        return

    match_text = lhs_rhs[0].strip()
    replace_text = lhs_rhs[1].strip()

    rule = [{
        "match": match_text,
        "replace": replace_text,
        "description": prompt.strip().capitalize()
    }]

    dest = Path(output_path)
    dest.parent.mkdir(parents=True, exist_ok=True)

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(rule, f, indent=2)

    print(f"✅ Rule generated and saved to: {output_path}")
