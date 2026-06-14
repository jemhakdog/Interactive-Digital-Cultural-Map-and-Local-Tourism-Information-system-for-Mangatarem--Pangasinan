import pypdf
import os

def extract_txt(pdf_path, txt_path):
    print(f"Extracting {pdf_path}...")
    if not os.path.exists(pdf_path):
        print(f"File {pdf_path} does not exist!")
        return
    reader = pypdf.PdfReader(pdf_path)
    text = ""
    for i, page in enumerate(reader.pages):
        text += f"\n--- Page {i+1} ---\n"
        text += page.extract_text()
    
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Done. Extracted {len(reader.pages)} pages.")

# PDF 1
extract_txt(
    "docs/interview_data/Project Needs Assessment_ Cultural & Tourism System - Google Forms.pdf",
    "scratch/needs_assessment.txt"
)

# PDF 2
extract_txt(
    "docs/rrl/Bridging Gaps in Public Service_ Insights from Local and Global Academic Studies for a Tourism Management System in Mangatarem.pdf",
    "scratch/bridging_gaps.txt"
)
