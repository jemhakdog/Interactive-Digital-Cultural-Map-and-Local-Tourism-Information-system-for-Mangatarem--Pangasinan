import re

def clean_text(text):
    # Strip zero-width spaces, joins, and other non-standard characters
    clean = re.sub(r'[\u200b-\u200d\uFEFF\u200e\u200f\u202a-\u202e\U0001f000-\U0001ffff]', '', text)
    return clean

with open("scratch/chapter_1_3.txt", "r", encoding="utf-8") as f:
    text = f.read()

cleaned = clean_text(text)

with open("scratch/chapter_1_3_clean.txt", "w", encoding="utf-8") as f:
    f.write(cleaned)

print("Cleaned text written to scratch/chapter_1_3_clean.txt")
print("First 200 chars:")
print(cleaned[:200])
