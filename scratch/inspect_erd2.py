import re

with open('d:/porjects/capstone_system/docs/diagrams/erd/erd_v2.drawio', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all table shapes and their IDs
table_matches = re.finditer(r'<mxCell id="([^"]+)" value="([A-Z_]+)" style="shape=table;', content)
tables = {}
for m in table_matches:
    tables[m.group(1)] = m.group(2)

# Row extraction is tricky because they are children of tables.
# But we can just use regex to find all rows.
# Actually, the cells within a row have the row as their parent. 
# And rows have the table as parent.

rows = re.finditer(r'<mxCell id="([^"]+)" style="shape=tableRow;.*?parent="([^"]+)"', content)
row_to_table = {}
for m in rows:
    row_id = m.group(1)
    parent_id = m.group(2)
    if parent_id in tables:
        row_to_table[row_id] = tables[parent_id]

# Now let's look at cells inside rows
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

# Now print out what we found
for r_id, vals in row_contents.items():
    if len(vals) >= 4:
        key_type = vals[0]
        name = vals[1]
        dtype = vals[2]
        extra = vals[3]
        
        # Look for inconsistencies
        # PK should be 'id'
        if key_type == 'PK' and name != 'id':
            print(f"Table {row_to_table[r_id]}: PK is named '{name}' instead of 'id'")
        
        # FK should usually be x_id
        if 'FK' in key_type:
            # extra looks like '&#8594; user.id' or '→ user.id'
            # decode HTML entities if needed, but we can just regex for '(\w+)\.id'
            target_match = re.search(r'([a-z_]+)\.id', extra)
            if target_match:
                target_table = target_match.group(1)
                expected_name = f"{target_table}_id"
                if name != expected_name:
                    print(f"Table {row_to_table[r_id]}: FK is named '{name}' but points to '{target_table}.id' (expected '{expected_name}')")
            else:
                print(f"Table {row_to_table[r_id]}: FK '{name}' has extra '{extra.encode('unicode_escape')}'")

