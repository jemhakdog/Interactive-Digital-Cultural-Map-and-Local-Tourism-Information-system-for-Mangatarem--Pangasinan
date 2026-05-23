import sys
import os
import glob
import traceback

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from routes.v1.documents import _parse_docx_file

def main():
    gathered_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "interview_data", "gathered_froms"))
    docx_files = glob.glob(os.path.join(gathered_dir, "*.docx"))
    
    if not docx_files:
        print(f"No .docx files found in {gathered_dir}")
        return
        
    print(f"Found {len(docx_files)} .docx files to analyze:\n")
    
    for filepath in docx_files:
        filename = os.path.basename(filepath)
        print("=" * 80)
        print(f"FILE: {filename}")
        print("=" * 80)
        
        try:
            with open(filepath, "rb") as f:
                slug, extracted = _parse_docx_file(f)
                
            print(f"DETECTED SLUG: {slug}")
            print(f"RAW EXTRACTED DATA: {repr(extracted)}")
            print("EXTRACTED PROPERTIES:")
            if extracted is not None:
                for k in sorted(extracted.keys()):
                    v = extracted[k]
                    # truncate extremely long lists or strings for cleaner console output
                    if isinstance(v, list) and len(v) > 3:
                        display_val = f"{v[:3]} ... (+{len(v) - 3} more)"
                    elif isinstance(v, str) and len(v) > 120:
                        display_val = v[:117] + "..."
                    else:
                        display_val = v
                    print(f"  {k}: {repr(display_val)}")
            else:
                print("  Failed to extract data (extracted is None).")
        except Exception as e:
            print(f"  Error processing file: {e}")
            traceback.print_exc()
        print()

if __name__ == "__main__":
    main()
