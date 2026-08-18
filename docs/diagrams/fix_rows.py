"""Remove value='0' from all tableRow cells in erd.drawio"""
import os

path = os.path.join(os.path.dirname(__file__), "erd.drawio")

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

count = content.count(' value="0"')
content = content.replace(' value="0"', "")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Removed {count} instances of value='0'. File saved.")
