import os

EXTENSIONS = {
    "cpp": [".cpp", ".h", ".hpp", ".cc"],
    "python": [".py"],
    "js": [".js", ".jsx", ".ts", ".tsx"]
}

def collect_files(base_path, lang):
    valid_exts = EXTENSIONS.get(lang, [])
    matched = []

    for root, _, files in os.walk(base_path):
        for file in files:
            if any(file.endswith(ext) for ext in valid_exts):
                matched.append(os.path.join(root, file))
    
    return matched
