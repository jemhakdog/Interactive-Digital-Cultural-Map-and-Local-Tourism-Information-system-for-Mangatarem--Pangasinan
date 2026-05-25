import xml.etree.ElementTree as ET
import sys
import copy

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v2.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

# 1. find tables
def find_table(name):
    for cell in mx_root.findall('mxCell'):
        val = cell.attrib.get('value', '')
        if name in val and 'shape=table' in cell.attrib.get('style', ''):
            return cell.attrib.get('id')
    return None

def find_row(table_id, fk_name):
    for cell in mx_root.findall('mxCell'):
        if cell.attrib.get('parent') == table_id:
            row_id = cell.attrib.get('id')
            for col in mx_root.findall(f"mxCell[@parent='{row_id}']"):
                if fk_name in col.attrib.get('value', ''):
                    return row_id
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
visitor_log_id = find_table('VISITOR_LOG')
review_photo_id = find_table('REVIEW_PHOTO')
pwd_id = find_table('PASSWORD_RESET_TOKEN')
audit_id = find_table('DATABASE_AUDIT_LOG')
attraction_id = find_table('ATTRACTION')

rp_table = None
for cell in mx_root.findall('mxCell'):
    if cell.attrib.get('id') == review_photo_id:
        rp_table = cell
        break

attraction_review_id = None

def get_descendants(parent_id):
    desc = []
    for cell in mx_root.findall('mxCell'):
        if cell.attrib.get('parent') == parent_id:
            desc.append(cell)
            desc.extend(get_descendants(cell.attrib.get('id')))
    return desc

if rp_table is not None:
    ar_existing = find_table('ATTRACTION_REVIEW')
    if ar_existing:
        attraction_review_id = ar_existing
        print(f"Found existing ATTRACTION_REVIEW: {attraction_review_id}")
    else:
        print("ATTRACTION_REVIEW not found, duplicating from REVIEW_PHOTO...")
        max_num = get_max_id() + 1000
        old_to_new = {}
        
        ar_table = copy.deepcopy(rp_table)
        ar_table.attrib['id'] = f"erd_table_{max_num}"
        ar_table.attrib['value'] = "ATTRACTION_REVIEW"
        old_to_new[rp_table.attrib['id']] = ar_table.attrib['id']
        
        geom = ar_table.find('mxGeometry')
        if geom is not None:
            try:
                y = int(geom.attrib.get('y', '0'))
                x = int(geom.attrib.get('x', '0'))
                geom.attrib['y'] = str(y - 200)
                geom.attrib['x'] = str(x + 250)
            except:
                pass
            
        mx_root.append(ar_table)
        attraction_review_id = ar_table.attrib['id']
        
        desc = get_descendants(rp_table.attrib['id'])
        for d in desc:
            new_d = copy.deepcopy(d)
            new_id = f"{d.attrib['id']}_ar_{max_num}"
            old_to_new[d.attrib['id']] = new_id
            new_d.attrib['id'] = new_id
            new_d.attrib['parent'] = old_to_new[d.attrib['parent']]
            mx_root.append(new_d)

# We also need to fix the edge we previously added that went to the column
to_remove = []
for cell in mx_root.findall('mxCell'):
    if cell.attrib.get('id', '').startswith('erd_edge_ar_'):
        if cell.attrib.get('target') == 'erd_table_2009_row_1_col_3':
            to_remove.append(cell)

for cell in to_remove:
    mx_root.remove(cell)

# add the corrected edge
edges_to_add = []
if review_photo_id and attraction_review_id:
    row = find_row(review_photo_id, 'review_id')
    if row:
        edges_to_add.append((row, attraction_review_id, 'review_id'))

max_num = get_max_id() + 2000
print(f"Adding {len(edges_to_add)} edges...")
for src, tgt, val in edges_to_add:
    max_num += 1
    new_edge = ET.Element('mxCell')
    new_edge.attrib['id'] = f"erd_edge_ar_fixed_{max_num}"
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
print("Updated erd_v2.drawio successfully!")
