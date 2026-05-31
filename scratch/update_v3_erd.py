import xml.etree.ElementTree as ET
import copy

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

# 1. Update NEWSLETTER_SUBSCRIBER table height
ns_table = mx_root.find(".//*[@id='erd_table_2001']")
if ns_table is not None:
    geom = ns_table.find('mxGeometry')
    if geom is not None:
        geom.attrib['height'] = '195'  # 5 * 34 + 25 = 195
    print("Updated NEWSLETTER_SUBSCRIBER height.")

# 2. Add user_id FK row (row 4) to NEWSLETTER_SUBSCRIBER
# We'll duplicate row 2 as a base
row2 = mx_root.find(".//*[@id='erd_table_2001_row_2']")
if row2 is not None:
    row4 = copy.deepcopy(row2)
    row4.attrib['id'] = 'erd_table_2001_row_4'
    row4_geom = row4.find('mxGeometry')
    if row4_geom is not None:
        row4_geom.attrib['y'] = '161'  # 4 * 34 + 25 = 161
    
    # Update columns
    mx_root.append(row4)
    
    # Find columns belonging to row 4 (we will duplicate or modify)
    # Actually, let's find the original columns and add copies with correct parent and values
    col_idx = 0
    for col in mx_root.findall(".//*[@parent='erd_table_2001_row_2']"):
        new_col = copy.deepcopy(col)
        new_col.attrib['id'] = f"erd_table_2001_row_4_col_{col_idx}"
        new_col.attrib['parent'] = 'erd_table_2001_row_4'
        if col_idx == 0:
            new_col.attrib['value'] = 'FK'
            new_col.attrib['style'] += 'fontStyle=5;'
        elif col_idx == 1:
            new_col.attrib['value'] = 'user_id'
            new_col.attrib['style'] += 'fontStyle=5;'
        elif col_idx == 2:
            new_col.attrib['value'] = 'int'
        elif col_idx == 3:
            new_col.attrib['value'] = 'nullable'
        mx_root.append(new_col)
        col_idx += 1
    print("Added user_id FK row to NEWSLETTER_SUBSCRIBER.")

# 3. Create NEWSLETTER_HISTORY table (erd_table_2002)
# We can duplicate erd_table_2001 as a base
if ns_table is not None:
    nh_table = copy.deepcopy(ns_table)
    nh_table.attrib['id'] = 'erd_table_2002'
    nh_table.attrib['value'] = 'NEWSLETTER_HISTORY'
    nh_geom = nh_table.find('mxGeometry')
    if nh_geom is not None:
        nh_geom.attrib['x'] = '2100'
        nh_geom.attrib['y'] = '1823'
        nh_geom.attrib['height'] = '229'  # 6 * 34 + 25 = 229
    mx_root.append(nh_table)
    print("Created NEWSLETTER_HISTORY table.")

    # Create 6 rows for NEWSLETTER_HISTORY
    rows_data = [
        ('PK', 'id', 'int', 'not null'),
        ('', 'subject', 'string', 'not null'),
        ('', 'content', 'text', 'not null'),
        ('', 'recipient_count', 'int', 'default=0'),
        ('FK', 'sender_id', 'int', 'nullable'),
        ('', 'sent_at', 'datetime', 'default=now')
    ]
    
    for r_idx, (pk_fk, name, dtype, opt) in enumerate(rows_data):
        new_row = copy.deepcopy(row2)
        new_row.attrib['id'] = f"erd_table_2002_row_{r_idx}"
        new_row.attrib['parent'] = 'erd_table_2002'
        new_row_geom = new_row.find('mxGeometry')
        if new_row_geom is not None:
            new_row_geom.attrib['y'] = str(25 + r_idx * 34)
        mx_root.append(new_row)
        
        # Add columns
        col_idx = 0
        for col in mx_root.findall(".//*[@parent='erd_table_2001_row_2']"):
            new_col = copy.deepcopy(col)
            new_col.attrib['id'] = f"erd_table_2002_row_{r_idx}_col_{col_idx}"
            new_col.attrib['parent'] = f"erd_table_2002_row_{r_idx}"
            
            if col_idx == 0:
                new_col.attrib['value'] = pk_fk
                if pk_fk:
                    new_col.attrib['style'] += 'fontStyle=5;'
            elif col_idx == 1:
                new_col.attrib['value'] = name
                if pk_fk:
                    new_col.attrib['style'] += 'fontStyle=5;'
            elif col_idx == 2:
                new_col.attrib['value'] = dtype
            elif col_idx == 3:
                new_col.attrib['value'] = opt
                
            mx_root.append(new_col)
            col_idx += 1
    print("Added rows to NEWSLETTER_HISTORY.")

# 4. Add dynamic snapped edges referencing USER (erd_1001)
# Find max edge ID
max_edge_id = 0
for cell in mx_root.findall('mxCell'):
    cid = cell.attrib.get('id', '')
    if cid.startswith('erd_edge_'):
        try:
            num = int(cid.split('_')[-1])
            max_edge_id = max(max_edge_id, num)
        except:
            pass

edges_to_add = [
    ('erd_table_2001_row_4_col_1', 'erd_1001', 'user_id (FK)'),
    ('erd_table_2002_row_4_col_1', 'erd_1001', 'sender_id (FK)')
]

for src, tgt, val in edges_to_add:
    max_edge_id += 1
    edge = ET.Element('mxCell')
    edge.attrib['id'] = f"erd_edge_{max_edge_id}"
    edge.attrib['value'] = val
    edge.attrib['style'] = "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#000000;strokeWidth=2;endArrow=classic;html=1;fontSize=14;"
    edge.attrib['parent'] = '1'
    edge.attrib['source'] = src
    edge.attrib['target'] = tgt
    edge.attrib['edge'] = '1'
    
    geom = ET.SubElement(edge, 'mxGeometry')
    geom.attrib['relative'] = '1'
    geom.attrib['as'] = 'geometry'
    
    mx_root.append(edge)
    print(f"Added edge from {src} to {tgt}.")

tree.write(file_path, encoding='utf-8', xml_declaration=False)
print("Successfully updated erd_v3.drawio!")
