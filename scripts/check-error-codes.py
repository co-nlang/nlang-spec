import os
import re
import sys

# --- Configuration ---
SPEC_DIR = "spec/zh_TW"
TAG_REGISTRY_FILE = os.path.join(SPEC_DIR, "TAG_REGISTRY.md")

def get_documented_tags(filepath):
    """Extract tags like #conflict from TAG_REGISTRY.md tables."""
    tags = set()
    if not os.path.exists(filepath):
        print(f"[FATAL] {filepath} not found.")
        return tags
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        # Match tags inside bold or backticks in tables: **#tag** or `#tag`
        found = re.findall(r"[`\*]+(#\w+)[`\*]+", content)
        tags.update(found)
    return tags

def get_mentioned_tags(directory):
    """Find all #tags used after %cause: in the spec files."""
    mentioned = {}
    # Pattern to find %cause: #tag or (%cause: #tag)
    cause_re = re.compile(r"%cause:\s*(#\w+)")
    
    for filename in os.listdir(directory):
        if not filename.endswith(".md") or filename == "TAG_REGISTRY.md":
            continue
            
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = cause_re.findall(content)
            for m in matches:
                if m not in mentioned:
                    mentioned[m] = []
                mentioned[m].append(filename)
    return mentioned

def main():
    print("--- n/ Error Code Coverage Check ---")
    
    documented = get_documented_tags(TAG_REGISTRY_FILE)
    mentioned = get_mentioned_tags(SPEC_DIR)
    
    errors = 0
    
    print(f"\n[1] Checking if mentioned tags are documented in TAG_REGISTRY.md...")
    for tag, files in mentioned.items():
        if tag not in documented:
            print(f"[ERR] Undocumented tag '{tag}' mentioned in: {', '.join(set(files))}")
            errors += 1
            
    print(f"\n[2] Checking for orphan tags (Documented but never mentioned in specs)...")
    for tag in documented:
        if tag not in mentioned and not tag.startswith("#ext:"): # Ignore extension template
            print(f"[INFO] Orphan tag '{tag}' is documented but not used as a %cause in any SPEC.")

    print("\n--- Summary ---")
    if errors == 0:
        print("Error code coverage is complete.")
    else:
        print(f"Found {errors} missing documentation entries.")
        sys.exit(1)

if __name__ == "__main__":
    if not os.path.exists("spec"):
        print("[FATAL] Please run this script from the nlang-spec root directory.")
        sys.exit(1)
    main()
