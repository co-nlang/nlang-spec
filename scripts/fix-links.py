import os
import re

# --- Configuration ---
SPEC_DIR = "spec/zh_TW"

# Mapping of code to filename (we can discover this dynamically)
def get_spec_map(directory):
    spec_map = {}
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            # Extract docs
            match = re.match(r"^((?:SPEC|REAL|GUIDE|ORDER|APP)_\w+?)(?:_|\.md)", filename)
            if match:
                spec_map[match.group(1)] = filename
    return spec_map

def fix_bare_references(directory, spec_map):
    print(f"--- Standardizing Cross-References in {directory} ---")

    # Regex to find bare XXXX_YY not preceded by [ or (
    # We use a simple regex and check context manually to avoid complex lookbehinds
    ref_pattern = re.compile(r"(?<![\[\(/])((?:SPEC|REAL|GUIDE|ORDER|APP)_\d{2})\b")

    for filename in os.listdir(directory):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content

        # Find all potential matches
        matches = ref_pattern.finditer(content)
        # Process in reverse to maintain offsets
        for match in reversed(list(matches)):
            ref_code = match.group(1)
            if ref_code in spec_map:
                target_file = spec_map[ref_code]
                # Avoid linking to itself
                if target_file == filename:
                    continue
                
                start, end = match.span()
                link = f"**[{ref_code}](./{target_file})**"
                new_content = new_content[:start] + link + new_content[end:]
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[FIXED] Linked bare references in {filename}")

if __name__ == "__main__":
    if not os.path.exists(SPEC_DIR):
        print("[FATAL] spec directory not found.")
    else:
        s_map = get_spec_map(SPEC_DIR)
        fix_bare_references(SPEC_DIR, s_map)
