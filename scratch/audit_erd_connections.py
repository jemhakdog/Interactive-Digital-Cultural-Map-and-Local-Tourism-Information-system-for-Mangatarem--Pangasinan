import xml.etree.ElementTree as ET

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v2.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

# 1. Find all tables
tables = {}  # id -> name
for cell in mx_root.findall('mxCell'):
    style = cell.attrib.get('style', '')
    val = cell.attrib.get('value', '')
    if 'shape=table;' in style or style == 'shape=table':
        tables[cell.attrib.get('id')] = val
        print(f"Table Found: ID={cell.attrib.get('id')}, Name={val}")

# 2. Find all rows and map them to their parent tables
rows = {}  # row_id -> table_id
for cell in mx_root.findall('mxCell'):
    parent = cell.attrib.get('parent')
    if parent in tables:
        rows[cell.attrib.get('id')] = parent

# 3. Track connections for each table
connections = {tid: {'incoming': 0, 'outgoing': 0} for tid in tables}

for cell in mx_root.findall('mxCell'):
    if cell.attrib.get('edge') == '1':
        src = cell.attrib.get('source', '')
        tgt = cell.attrib.get('target', '')
        val = cell.attrib.get('value', '')
        eid = cell.attrib.get('id')
        
        src_table = None
        if src in tables:
            src_table = src
        elif src in rows:
            src_table = rows[src]
            
        tgt_table = None
        if tgt in tables:
            tgt_table = tgt
        elif tgt in rows:
            tgt_table = rows[tgt]
            
        # print(f"Edge ID={eid} (Value={val}): {src_table} -> {tgt_table}")
        
        if src_table:
            connections[src_table]['outgoing'] += 1
        if tgt_table:
            connections[tgt_table]['incoming'] += 1

print("\n" + "="*40 + " CONNECTION AUDIT REPORT " + "="*40)
for tid, counts in connections.items():
    name = tables[tid]
    total = counts['incoming'] + counts['outgoing']
    status = "CONNECTED" if total > 0 else "!!! FLOATING / UNCONNECTED !!!"
    print(f"Table: {name:<25} | Incoming: {counts['incoming']:<2} | Outgoing: {counts['outgoing']:<2} | Status: {status}")
