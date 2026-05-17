with open(r'd:\porjects\capstone_system\static\css\main.css', 'r', encoding='utf-8') as f:
    content = f.read()

classes = ['.gap-x-6', '.lg\\:gap-x-8']
for c in classes:
    if c in content:
        print(f"FOUND class: {c}")
    else:
        # Also try searching without escape for logging
        print(f"NOT FOUND class: {c}")
