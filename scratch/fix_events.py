import os

file_path = r"d:\porjects\Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan\routes\barangay\events.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace permission checks
old_check = 'if event.user_id != current_user.id:'
new_check = 'if event.barangay_id != current_user.barangay_id:'

content = content.replace(old_check, new_check)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated events.py permission checks.")
