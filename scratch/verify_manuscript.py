import os
import re

def verify_files():
    chapters_dir = r"d:\porjects\capstone_system\docs\capstone\chapters"
    files = [
        "Chapter-1-Introduction.md",
        "Chapter-2-Methodology-and-Design.md",
        "Chapter-3-Results-and-Discussion.md"
    ]
    
    # 1. Check for first-person pronouns as independent words (case-insensitive)
    # Match "we", "our", "us", "i", but ignore common prefixes/suffixes or markdown syntax.
    # We use boundary checks \b
    pronouns_pattern = re.compile(r'\b(we|our|us|i)\b', re.IGNORECASE)
    
    # 2. Check for the specific typos listed in todo.md
    typos = [
        "comm it",
        "vi a",
        "me dia",
        "Da ta Store D1",
        "attem pts",
        "anot her",
        "HT TP",
        "crit ical",
        "searchin g",
        "confus ion"
    ]
    
    errors_found = 0
    
    for filename in files:
        filepath = os.path.join(chapters_dir, filename)
        if not os.path.exists(filepath):
            print(f"File not found: {filename}")
            continue
            
        print(f"\nAuditing {filename}...")
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Check typos
        for typo in typos:
            if typo in content:
                print(f"  [ERROR] Found unresolved typo: '{typo}'")
                errors_found += 1
                
        # Check pronouns
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            # Strip markdown links to avoid matching URL tokens if any
            clean_line = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line)
            
            matches = pronouns_pattern.findall(clean_line)
            if matches:
                # Filter out valid singular occurrences (like NCCA standard, SQL, etc., but check for manual pronouns)
                filtered_matches = []
                for m in matches:
                    if m.lower() == 'i' and any(term in clean_line for term in ["Form 01", "ISO", "Standard", "1.", "2.", "3.", "4.", "5.", "I1", "V1"]):
                        continue # Ignore structural markers like Form 01-07 Roman numerals
                    # Standard check
                    filtered_matches.append(m)
                    
                if filtered_matches:
                    print(f"  [WARNING] Possible first-person pronoun(s) {filtered_matches} on Line {line_num}:")
                    print(f"    '{line.strip()}'")
                    errors_found += 1
                    
    if errors_found == 0:
        print("\n[SUCCESS] Quality audit completed successfully! 0 errors/warnings found.")
    else:
        print(f"\n[AUDIT FAILED] Completed with {errors_found} errors/warnings to review.")

if __name__ == "__main__":
    verify_files()
