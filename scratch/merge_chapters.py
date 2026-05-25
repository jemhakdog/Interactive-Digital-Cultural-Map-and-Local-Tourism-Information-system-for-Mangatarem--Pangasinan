import os

def merge_chapters():
    chapters_dir = r"d:\porjects\capstone_system\docs\capstone\chapters"
    c1_path = os.path.join(chapters_dir, "Chapter-1-Introduction.md")
    c2_path = os.path.join(chapters_dir, "Chapter-2-Methodology-and-Design.md")
    c3_path = os.path.join(chapters_dir, "Chapter-3-Results-and-Discussion.md")
    output_path = os.path.join(chapters_dir, "full chapters.md")

    print(f"Reading chapters from {chapters_dir}...")
    
    with open(c1_path, "r", encoding="utf-8") as f:
        c1_content = f.read().strip()
        
    with open(c2_path, "r", encoding="utf-8") as f:
        c2_content = f.read().strip()
        
    with open(c3_path, "r", encoding="utf-8") as f:
        c3_content = f.read().strip()

    combined = f"{c1_content}\n\n\n{c2_content}\n\n\n{c3_content}\n"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(combined)
        
    print(f"Consolidated chapters successfully written to: {output_path}")

if __name__ == "__main__":
    merge_chapters()
