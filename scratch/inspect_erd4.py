import re

with open('d:/porjects/capstone_system/docs/diagrams/erd/erd_v2.drawio', 'r', encoding='utf-8') as f:
    content = f.read()

rows = re.finditer(r'<mxCell id="([^"]+)" style="shape=tableRow;.*?parent="([^"]+)"', content)
table_matches = re.finditer(r'<mxCell id="([^"]+)" value="([A-Z_]+)" style="shape=table;', content)
tables = {}
for m in table_matches:
    tables[m.group(1)] = m.group(2)

row_to_table = {}
for m in rows:
    row_id = m.group(1)
    parent_id = m.group(2)
    if parent_id in tables:
        row_to_table[row_id] = tables[parent_id]

cells = re.finditer(r'<mxCell id="([^"]+)" value="([^"]*)" style="shape=partialRectangle;.*?parent="([^"]+)"', content)
row_contents = {}
for m in cells:
    cell_id = m.group(1)
    val = m.group(2)
    parent_id = m.group(3)
    if parent_id in row_to_table:
        if parent_id not in row_contents:
            row_contents[parent_id] = []
        row_contents[parent_id].append(val)

print("ALL FIELDS:")
for r_id, vals in row_contents.items():
    if len(vals) >= 2:
        key_type = vals[0]
        name = vals[1]
        print(f"{row_to_table[r_id]}: {key_type} | {name}")
