import re

with open('d:/porjects/capstone_system/docs/diagrams/erd/erd_v2.drawio', 'r', encoding='utf-8') as f:
    content = f.read()

print('UK count:', content.count('value="UK"'))

tables = re.findall(r'value="([A-Z_]+)".*?shape=table;', content)
print('Tables:', tables)

# Find all field names
fields = re.findall(r'value="([^"]+)".*?shape=partialRectangle;', content)
# We want only those that might be IDs or FKs
fk_pk_fields = [f for f in fields if 'id' in f.lower() or f.islower()]
from collections import Counter
print('Fields counter:', Counter(fk_pk_fields).most_common(50))

# Let's find fields that might be named inconsistently
# Specifically look for foreign key patterns
fks = re.findall(r'value="\((FK\d*)\)".*?value="([^"]+)"', content, flags=re.DOTALL)
print('Foreign keys (approx):', len(fks))
