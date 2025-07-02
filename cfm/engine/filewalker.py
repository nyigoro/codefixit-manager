import os

# Supported file extensions by language
EXTENSIONS = {
    "cpp": [".cpp", ".h", ".hpp", ".cc"],
    "python": [".py"],
    "js": [".js", ".jsx", ".ts", ".tsx"]
}

def collect_files(base_path, lang):
    """
    Recursively collect all source files matching language-specific extensions.

    Args:
        base_path (str): Root directory to scan.
        lang (str): Language key (e.g. "cpp", "python").

    Returns:
        List[str]: List of full file paths.
    """
    valid_exts = EXTENSIONS.get(lang)
    if not valid_exts:
        raise ValueError(f"❌ Unsupported language: '{lang}'")

    matched = []

    for root, _, files in os.walk(base_path):
        for file in files:
            if any(file.endswith(ext) for ext in valid_exts):
                full_path = os.path.join(root, file)
                matched.append(full_path)

    print(f"📂 Collected {len(matched)} {lang} file(s) from {base_path}")
    return matched
