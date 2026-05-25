import xml.etree.ElementTree as ET

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v2.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

# Find ATTRACTION_REVIEW table
ar_table_id = None
for cell in mx_root.findall('mxCell'):
    val = cell.attrib.get('value', '')
    style = cell.attrib.get('style', '')
    if 'ATTRACTION_REVIEW' in val and 'shape=table' in style:
        ar_table_id = cell.attrib.get('id')
        print(f"Table ATTRACTION_REVIEW id: {ar_table_id}")
        print(f"Attributes: {cell.attrib}")
        geom = cell.find('mxGeometry')
        if geom is not None:
            print(f"Geometry: {geom.attrib}")

if not ar_table_id:
    print("Table ATTRACTION_REVIEW not found")
    exit(1)

# Dump rows of ATTRACTION_REVIEW
rows = []
for cell in mx_root.findall('mxCell'):
    if cell.attrib.get('parent') == ar_table_id:
        rows.append(cell)

print(f"\nFound {len(rows)} rows for ATTRACTION_REVIEW:")
for idx, r in enumerate(rows):
    r_id = r.attrib.get('id')
    r_val = r.attrib.get('value', '')
    r_style = r.attrib.get('style', '')
    r_geom = r.find('mxGeometry')
    geom_str = r_geom.attrib if r_geom is not None else "None"
    print(f"\nRow {idx}: ID={r_id}, Value={r_val}, Style={r_style}, Geometry={geom_str}")
    
    # Columns of this row
    cols = []
    for col in mx_root.findall('mxCell'):
        if col.attrib.get('parent') == r_id:
            cols.append(col)
    
    print(f"  Columns ({len(cols)}):")
    for c in cols:
        c_id = c.attrib.get('id')
        c_val = c.attrib.get('value', '')
        c_style = c.attrib.get('style', '')
        c_geom = c.find('mxGeometry')
        c_geom_str = c_geom.attrib if c_geom is not None else "None"
        print(f"    Col ID={c_id}, Value={repr(c_val)}, Style={c_style}, Geometry={c_geom_str}")

print("\n" + "="*80 + "\n")

# Find REVIEW_PHOTO table
rp_table_id = None
for cell in mx_root.findall('mxCell'):
    val = cell.attrib.get('value', '')
    style = cell.attrib.get('style', '')
    if 'REVIEW_PHOTO' in val and 'shape=table' in style:
        rp_table_id = cell.attrib.get('id')
        print(f"Table REVIEW_PHOTO id: {rp_table_id}")
        print(f"Attributes: {cell.attrib}")
        geom = cell.find('mxGeometry')
        if geom is not None:
            print(f"Geometry: {geom.attrib}")

if not rp_table_id:
    print("Table REVIEW_PHOTO not found")
    exit(1)

# Dump rows of REVIEW_PHOTO
rp_rows = []
for cell in mx_root.findall('mxCell'):
    if cell.attrib.get('parent') == rp_table_id:
        rp_rows.append(cell)

print(f"\nFound {len(rp_rows)} rows for REVIEW_PHOTO:")
for idx, r in enumerate(rp_rows):
    r_id = r.attrib.get('id')
    r_val = r.attrib.get('value', '')
    r_style = r.attrib.get('style', '')
    r_geom = r.find('mxGeometry')
    geom_str = r_geom.attrib if r_geom is not None else "None"
    print(f"\nRow {idx}: ID={r_id}, Value={r_val}, Style={r_style}, Geometry={geom_str}")
    
    # Columns of this row
    cols = []
    for col in mx_root.findall('mxCell'):
        if col.attrib.get('parent') == r_id:
            cols.append(col)
    
    print(f"  Columns ({len(cols)}):")
    for c in cols:
        c_id = c.attrib.get('id')
        c_val = c.attrib.get('value', '')
        c_style = c.attrib.get('style', '')
        c_geom = c.find('mxGeometry')
        c_geom_str = c_geom.attrib if c_geom is not None else "None"
        print(f"    Col ID={c_id}, Value={repr(c_val)}, Style={c_style}, Geometry={c_geom_str}")
