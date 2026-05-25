import xml.etree.ElementTree as ET
import copy
import sys

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v2.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

def find_table(name):
    for cell in mx_root.findall('mxCell'):
        val = cell.attrib.get('value', '')
        if name in val and 'shape=table' in cell.attrib.get('style', ''):
            return cell.attrib.get('id')
    return None

def get_max_id():
    max_id = 0
    for cell in mx_root.findall('mxCell'):
        cid = cell.attrib.get('id', '')
        parts = cid.split('_')
        for p in parts:
            if p.isdigit():
                max_id = max(max_id, int(p))
    return max_id

user_id = find_table('USER')
attraction_id = find_table('ATTRACTION')
attraction_review_id = find_table('ATTRACTION_REVIEW')

if not attraction_review_id:
    print("ATTRACTION_REVIEW not found")
    sys.exit(1)

# We need to change the rows of ATTRACTION_REVIEW.
# Currently it has rows from REVIEW_PHOTO.
# Let's find its rows and replace their contents.
ar_rows = []
for cell in mx_root.findall('mxCell'):
    if cell.attrib.get('parent') == attraction_review_id:
        ar_rows.append(cell)

# The structure we want:
# Row 0: PK | id | int | not null
# Row 1: (FK1) | user_id | int | -> USER.id
# Row 2: (FK2) | attraction_id | int | -> ATTRACTION.id
# Row 3: | rating | int | not null
# Row 4: | comment | text | nullable
# Row 5: | created_at | datetime | default=now

new_rows_data = [
    ("PK", "id", "int", "not null"),
    ("(FK1)", "user_id", "int", "→ USER.id"),
    ("(FK2)", "attraction_id", "int", "→ ATTRACTION.id"),
    ("", "rating", "int", "not null"),
    ("", "comment", "text", "nullable"),
    ("", "created_at", "datetime", "default=now")
]

# Create missing rows if we have less than 6 rows
max_num = get_max_id() + 3000

while len(ar_rows) < 6:
    max_num += 1
    new_row = copy.deepcopy(ar_rows[0])
    new_row.attrib['id'] = f"erd_table_{max_num}_row"
    mx_root.append(new_row)
    ar_rows.append(new_row)
    
    # create columns for this new row
    for i in range(4):
        new_col = copy.deepcopy(mx_root.find(f".//mxCell[@parent='{ar_rows[0].attrib['id']}']"))
        new_col.attrib['id'] = f"erd_table_{max_num}_col_{i}"
        new_col.attrib['parent'] = new_row.attrib['id']
        mx_root.append(new_col)

# Now update the text of the rows
for idx, data in enumerate(new_rows_data):
    row_cell = ar_rows[idx]
    # find columns
    cols = mx_root.findall(f".//mxCell[@parent='{row_cell.attrib['id']}']")
    # ensure it has 4 columns (it should, based on template)
    if len(cols) >= 4:
        cols[0].attrib['value'] = data[0]
        cols[1].attrib['value'] = data[1]
        cols[2].attrib['value'] = data[2]
        cols[3].attrib['value'] = data[3]

# Now we need to add edges from user_id to USER, and attraction_id to ATTRACTION
row_user_id = ar_rows[1].attrib['id']
row_attr_id = ar_rows[2].attrib['id']

edges_to_add = [
    (row_user_id, user_id, 'user_id'),
    (row_attr_id, attraction_id, 'attraction_id')
]

for src, tgt, val in edges_to_add:
    max_num += 1
    new_edge = ET.Element('mxCell')
    new_edge.attrib['id'] = f"erd_edge_ar_fix2_{max_num}"
    new_edge.attrib['value'] = val
    new_edge.attrib['style'] = "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#000000;strokeWidth=2;endArrow=classic;html=1;fontSize=14;"
    new_edge.attrib['parent'] = "1"
    new_edge.attrib['source'] = src
    new_edge.attrib['target'] = tgt
    new_edge.attrib['edge'] = "1"
    
    geom = ET.SubElement(new_edge, 'mxGeometry')
    geom.attrib['relative'] = "1"
    geom.attrib['as'] = "geometry"
    mx_root.append(new_edge)

tree.write(file_path, encoding='utf-8', xml_declaration=False)
print("Fixed ATTRACTION_REVIEW table and connected it successfully!")
