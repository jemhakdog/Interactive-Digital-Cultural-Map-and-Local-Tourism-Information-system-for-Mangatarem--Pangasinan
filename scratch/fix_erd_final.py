import xml.etree.ElementTree as ET

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v2.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

# 1. Fix ATTRACTION_REVIEW table size
ar_table = None
for cell in mx_root.findall('mxCell'):
    if cell.attrib.get('id') == 'erd_table_6009':
        ar_table = cell
        break

if ar_table is not None:
    geom = ar_table.find('mxGeometry')
    if geom is not None:
        geom.attrib['width'] = '560'
        geom.attrib['height'] = '229'
        print("Updated ATTRACTION_REVIEW table width=560, height=229.")

# 2. Fix ATTRACTION_REVIEW rows and columns
rows = []
for cell in mx_root.findall('mxCell'):
    if cell.attrib.get('parent') == 'erd_table_6009':
        rows.append(cell)

# Sort rows by y geometry coordinate
rows.sort(key=lambda r: int(r.find('mxGeometry').attrib.get('y', '0')))
print(f"Sorting and fixing {len(rows)} rows...")

def get_col_idx(col_id):
    parts = col_id.split('_')
    for i, p in enumerate(parts):
        if p == 'col' and i + 1 < len(parts):
            if parts[i+1].isdigit():
                return int(parts[i+1])
    return col_id

for idx, r in enumerate(rows):
    row_id = r.attrib.get('id')
    r_geom = r.find('mxGeometry')
    if r_geom is not None:
        r_geom.attrib['width'] = '560'
        r_geom.attrib['height'] = '34'
        r_geom.attrib['y'] = str(25 + idx * 34)
    
    # Columns of this row
    cols = []
    for cell in mx_root.findall('mxCell'):
        if cell.attrib.get('parent') == row_id:
            cols.append(cell)
            
    # Sort columns by their column index from ID
    cols.sort(key=lambda c: get_col_idx(c.attrib.get('id', '')))
    print(f"Row {idx} ({row_id}) has {len(cols)} columns. Setting geometry...")
    
    # Correct each column's geometry and style
    # Col 0: width=50, height=34
    # Col 1: width=200, height=34, x=50
    # Col 2: width=100, height=34, x=250
    # Col 3: width=210, height=34, x=350
    col_configs = [
        {'width': '50', 'height': '34', 'x': None},
        {'width': '200', 'height': '34', 'x': '50'},
        {'width': '100', 'height': '34', 'x': '250'},
        {'width': '210', 'height': '34', 'x': '350'}
    ]
    
    for c_idx, c in enumerate(cols):
        c_geom = c.find('mxGeometry')
        if c_geom is not None:
            config = col_configs[c_idx] if c_idx < len(col_configs) else col_configs[-1]
            c_geom.attrib['width'] = config['width']
            c_geom.attrib['height'] = config['height']
            if config['x'] is not None:
                c_geom.attrib['x'] = config['x']
            else:
                if 'x' in c_geom.attrib:
                    del c_geom.attrib['x']
                    
        # Remove bold/underline styling for non-key rows (Row 3, 4, 5)
        style = c.attrib.get('style', '')
        if idx in [3, 4, 5]:
            style = style.replace('fontStyle=5;', '')
            # Ensure it is fontStyle=0 or no fontStyle
            if 'fontStyle=' not in style:
                style += 'fontStyle=0;'
        c.attrib['style'] = style

# 3. Correct the Edges
edge_configs = {
    'erd_edge_ar_fixed_8010': {
        'name': 'review_id (REVIEW_PHOTO -> ATTRACTION_REVIEW)',
        'source': 'erd_table_2009_row_1',
        'target': 'erd_table_6009',
        'style': 'edgeStyle=orthogonalEdgeStyle;rounded=1;startArrow=ERzeroToMany;startSize=10;endArrow=ERmandOne;endSize=10;fontSize=14;fillColor=#0050ef;strokeColor=#001DBC;jumpStyle=none;jumpSize=50;strokeWidth=3;exitX=0.5;exitY=1;entryX=0.5;entryY=0;exitDx=0;exitDy=0;entryDx=0;entryDy=0;'
    },
    'erd_edge_ar_fix2_11013': {
        'name': 'user_id (ATTRACTION_REVIEW -> USER)',
        'source': 'erd_table_2009_row_1_ar_6009',
        'target': 'erd_1001',
        'style': 'edgeStyle=orthogonalEdgeStyle;rounded=1;startArrow=ERzeroToMany;startSize=10;endArrow=ERmandOne;endSize=10;fontSize=14;fillColor=#0050ef;strokeColor=#001DBC;jumpStyle=none;jumpSize=50;strokeWidth=3;exitX=0;exitY=0.5;entryX=1;entryY=0.5;exitDx=0;exitDy=0;entryDx=0;entryDy=0;'
    },
    'erd_edge_ar_fix2_11014': {
        'name': 'attraction_id (ATTRACTION_REVIEW -> ATTRACTION)',
        'source': 'erd_table_2009_row_2_ar_6009',
        'target': 'erd_1037',
        'style': 'edgeStyle=orthogonalEdgeStyle;rounded=1;startArrow=ERzeroToMany;startSize=10;endArrow=ERmandOne;endSize=10;fontSize=14;fillColor=#0050ef;strokeColor=#001DBC;jumpStyle=none;jumpSize=50;strokeWidth=3;exitX=0;exitY=0.5;entryX=1;entryY=0.5;exitDx=0;exitDy=0;entryDx=0;entryDy=0;'
    }
}

for eid, config in edge_configs.items():
    found = False
    for cell in mx_root.findall('mxCell'):
        if cell.attrib.get('id') == eid:
            found = True
            cell.attrib['source'] = config['source']
            cell.attrib['target'] = config['target']
            cell.attrib['style'] = config['style']
            
            # Clear old control points in mxGeometry
            geom = cell.find('mxGeometry')
            if geom is not None:
                for pt in list(geom.findall('mxPoint')):
                    geom.remove(pt)
            print(f"Fixed edge: {config['name']}")
            break
            
    if not found:
        print(f"WARNING: Edge {eid} not found!")

# 4. Save file
tree.write(file_path, encoding='utf-8', xml_declaration=False)
print("\nerd_v2.drawio has been fully corrected successfully!")
