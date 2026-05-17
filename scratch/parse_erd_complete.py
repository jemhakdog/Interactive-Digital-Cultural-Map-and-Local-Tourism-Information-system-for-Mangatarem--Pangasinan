import xml.etree.ElementTree as ET
import os

def parse_detailed_erd():
    erd_path = r"d:\porjects\capstone_system\docs\diagrams\erd\erd_v1.drawio"
    if not os.path.exists(erd_path):
        print(f"Error: {erd_path} not found.")
        return
        
    tree = ET.parse(erd_path)
    root = tree.getroot()
    
    # Tables are cells with shape=table or similar
    cells = list(root.iter('mxCell'))
    
    tables = {}
    for cell in cells:
        style = cell.get('style', '')
        if 'shape=table;' in style:
            tid = cell.get('id')
            val = cell.get('value', '')
            clean_name = val.replace('<b>', '').replace('</b>', '').replace('<br>', '\n').strip()
            # Also get geometry if any
            geom = cell.find('mxGeometry')
            x = geom.get('x', '0') if geom is not None else '0'
            y = geom.get('y', '0') if geom is not None else '0'
            width = geom.get('width', '0') if geom is not None else '0'
            height = geom.get('height', '0') if geom is not None else '0'
            
            tables[tid] = {
                'name': clean_name,
                'x': float(x),
                'y': float(y),
                'w': float(width),
                'h': float(height),
                'rows': []
            }
            
    # Now find rows belonging to each table
    # In Draw.io tables, rows usually have parent attribute pointing to the table ID
    # or the table container's row containers. Let's map parents.
    for cell in cells:
        parent = cell.get('parent')
        if parent in tables:
            val = cell.get('value', '')
            style = cell.get('style', '')
            cid = cell.get('id')
            
            # Clean HTML
            clean_val = val.replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', '').strip()
            clean_val = clean_val.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
            
            # Rows are typically partial rectangles or tables
            tables[parent]['rows'].append({
                'id': cid,
                'value': clean_val,
                'style': style
            })
            
    # For rows that are part of nested groups or layouts, let's also resolve parents iteratively
    # Many Draw.io tables have a cell parent, which itself has a parent that is the table.
    # Let's map parent-child chain
    parent_map = {}
    for cell in cells:
        cid = cell.get('id')
        parent = cell.get('parent')
        if cid and parent:
            parent_map[cid] = parent
            
    def get_table_ancestor(cid):
        curr = cid
        visited = set()
        while curr in parent_map:
            p = parent_map[curr]
            if p in tables:
                return p
            if p in visited:
                break
            visited.add(p)
            curr = p
        return None

    # Let's assign cells to tables based on ancestors
    for cell in cells:
        cid = cell.get('id')
        parent = cell.get('parent')
        if not parent or parent == '1' or parent == '0':
            continue
        
        # Check if already added direct child
        ancestor = get_table_ancestor(cid)
        if ancestor and ancestor != parent:  # it's a nested child (like row components: key, type, constraint)
            val = cell.get('value', '')
            clean_val = val.replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', '').strip()
            clean_val = clean_val.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
            
            tables[ancestor]['rows'].append({
                'id': cid,
                'parent': parent,
                'value': clean_val,
                'style': cell.get('style', '')
            })

    # Let's clean and write the tables to a text file
    output_path = r"d:\porjects\capstone_system\scratch\erd_v1_summary.txt"
    with open(output_path, "w", encoding="utf-8") as f_out:
        f_out.write(f"Parsed {len(tables)} tables successfully.\n\n")
        for tid, t in tables.items():
            f_out.write(f"Table: {t['name']} (ID: {tid}) at ({t['x']}, {t['y']}) size {t['w']}x{t['h']}\n")
            
            # Group by parent to group columns into rows
            direct_rows = [r for r in t['rows'] if r.get('parent') is None]
            for dr in direct_rows:
                # Find sub-cells of this row
                sub_cells = [r for r in t['rows'] if r.get('parent') == dr['id']]
                if sub_cells:
                    vals = [sc['value'] for sc in sub_cells if sc['value']]
                    f_out.write(f"  - Row cell ID {dr['id']}: {repr(dr['value'])} -> Sub-cells: {vals}\n")
                else:
                    if dr['value']:
                        f_out.write(f"  - Row cell ID {dr['id']}: {repr(dr['value'])} \n")
            f_out.write("-" * 50 + "\n")
    print(f"Summary written to {output_path}")

if __name__ == '__main__':
    parse_detailed_erd()
