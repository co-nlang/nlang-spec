import os
import re
import sys

# --- Configuration ---
SPEC_DIR = "spec/zh_TW"
GLOSSARY_TERMS = {
    "資料": "數據 (Data)",
    "函數": "態射 (Morphism/Logic)",
    "類型": "型別 (Type)",
    "變數": "欄位 (Field)",
    "執行": "觀測 (Observation)",
}

def check_file_names(directory):
    print(f"--- Checking File Naming in {directory} ---")
    errors = 0
    # Support SPEC, REAL, ORDER, APP, GUIDE, and utility files
    pattern = re.compile(r"^(SPEC_\d{2}|REAL_\d{2}|ORDER_\d{2}|APP_\d{2}|GUIDE_\d{2}|PREFACE|GLOSSARY|QUICK_REFERENCE|ERROR_CODES|README|SPEC_STATUS)(_.*)?\.md$")
    
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            if not pattern.match(filename):
                print(f"[ERR] Invalid filename: {filename}")
                errors += 1
    return errors

def check_links_and_terms(directory):
    print(f"--- Checking Links and Terminology in {directory} ---")
    errors = 0
    all_files = set(os.listdir(directory))
    
    for filename in os.listdir(directory):
        if not filename.endswith(".md"):
            continue
            
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 1. Check Internal Links [text](SPEC_XX.md)
            links = re.findall(r"\]\((SPEC_\d{2}_.*?\.md)\)", content)
            for link in links:
                if link not in all_files:
                    print(f"[ERR] Broken link in {filename}: {link}")
                    errors += 1
            
            # 2. Check Prohibited Terms
            for bad_term, suggestion in GLOSSARY_TERMS.items():
                if bad_term in content:
                    # Avoid flagging the glossary itself if it's defining the term
                    if filename == "GLOSSARY.md": continue
                    
                    count = content.count(bad_term)
                    print(f"[WARN] {filename} uses '{bad_term}' {count} times. Suggestion: {suggestion}")
                    # We treat term misuse as a warning for now
    
    return errors

if __name__ == "__main__":
    # Ensure we are in the nlang-spec root
    if not os.path.exists("spec"):
        print("[FATAL] Please run this script from the nlang-spec root directory.")
        sys.exit(1)
        
    total_errors = 0
    total_errors += check_file_names(SPEC_DIR)
    total_errors += check_links_and_terms(SPEC_DIR)
    
    print("\n--- Summary ---")
    if total_errors == 0:
        print("Lattice is coherent. No errors found.")
    else:
        print(f"Found {total_errors} errors. Convergence failed.")
        sys.exit(1)
