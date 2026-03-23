import xml.etree.ElementTree as ET
import sys
import os

def update_gpt_flowchart(file_path):
    print(f"Parsing {file_path}...")
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Iterate through diagrams
    # <diagram ...> <mxGraphModel> <root> ...
    for diagram in root.findall('diagram'):
        d_id = diagram.get('id')
        mx_graph = diagram.find('.//mxGraphModel')
        if mx_graph is None:
            continue
        graph_root = mx_graph.find('.//root')
        if graph_root is None:
            continue

        if d_id == 'page1':
            print(f"Processing Page 1 ({d_id})...")
            # 1. Remove p1_e4 (Click Login)
            e4 = graph_root.find(".//mxCell[@id='p1_e4']")
            if e4 is not None:
                print("  Removing p1_e4 (Click Login edge)")
                graph_root.remove(e4)
            
            # 2. Rename p1_role to "Is Admin?"
            role = graph_root.find(".//mxCell[@id='p1_role']")
            if role is not None:
                print("  Renaming p1_role to 'Is Admin?'")
                role.set('value', 'Is Admin?')
            
            # 3. Rename p1_e8 (Admin) to "Yes"
            e8 = graph_root.find(".//mxCell[@id='p1_e8']")
            if e8 is not None:
                print("  Renaming p1_e8 to 'Yes'")
                e8.set('value', 'Yes')

            # 4. Rename p1_e7 (Barangay Rep) to "No"
            e7 = graph_root.find(".//mxCell[@id='p1_e7']")
            if e7 is not None:
                print("  Renaming p1_e7 to 'No'")
                e7.set('value', 'No')

        elif d_id == 'page2':
            print(f"Processing Page 2 ({d_id})...")
            # Insert Manual Process
            # Existing: p2_dash -> p2_e2 -> p2_create
            
            # 1. Remove p2_e2
            e2 = graph_root.find(".//mxCell[@id='p2_e2']")
            if e2 is not None:
                print("  Removing p2_e2 (Old edge)")
                graph_root.remove(e2)

            # 2. Cleanup previous runs
            for mid in ['manual_collect', 'manual_digitize', 'edge_manual_1', 'edge_manual_2', 'edge_manual_3']:
               existing = graph_root.find(f".//mxCell[@id='{mid}']")
               if existing is not None:
                   graph_root.remove(existing)

            # 3. Shift nodes down to make space (Shift by 250px)
            shift_amount = 250
            ids_to_shift = ['p2_create', 'p2_submit', 'p2_db', 'p2_note', 'p2_footer']
            # Also need to shift edges? Edges usually are relative or automatic, 
            # but if they have checkpoints (mxPoint), those might need shifting.
            # However, standard straight edges should auto-adjust if source/target move.
            # p2_e3, p2_e4, p2_e5 might be affected.
            # For simplicity, we just shift vertices.
            
            for nid in ids_to_shift:
                cell = graph_root.find(f".//mxCell[@id='{nid}']/mxGeometry")
                if cell is not None:
                     try:
                        y = int(float(cell.get('y')))
                        cell.set('y', str(y + shift_amount))
                     except ValueError:
                         pass
            
            print(f"  Shifted {len(ids_to_shift)} nodes down by {shift_amount}px")

            # 4. Add Manual Process Nodes
            # p2_dash is at y=170.
            # insert manual_collect at y=280
            manual_collect = ET.SubElement(graph_root, 'mxCell', {
                'id': 'manual_collect',
                'value': 'Manual Field Surveys<br/>(Forms 01A-07)',
                'style': 'whiteSpace=wrap;strokeWidth=2;fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1',
                'vertex': '1',
                'parent': '1'
            })
            ET.SubElement(manual_collect, 'mxGeometry', {
                'x': '450', 'y': '280', 'width': '200', 'height': '60', 'as': 'geometry'
            })

            # insert manual_digitize at y=380
            manual_digitize = ET.SubElement(graph_root, 'mxCell', {
                'id': 'manual_digitize',
                'value': 'Manual Encoding<br/>(Word/Excel)',
                'style': 'whiteSpace=wrap;strokeWidth=2;fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1',
                'vertex': '1',
                'parent': '1'
            })
            ET.SubElement(manual_digitize, 'mxGeometry', {
                'x': '450', 'y': '380', 'width': '200', 'height': '60', 'as': 'geometry'
            })

            # 5. Add New Edges
            # p2_dash -> manual_collect
            edge1 = ET.SubElement(graph_root, 'mxCell', {
                'id': 'edge_manual_1', 'edge': '1', 'parent': '1',
                'source': 'p2_dash', 'target': 'manual_collect',
                'style': 'endArrow=block;rounded=0;entryX=0.5;entryY=0;exitX=0.5;exitY=1;' 
            })
            ET.SubElement(edge1, 'mxGeometry', {'relative': '1', 'as': 'geometry'})

            # manual_collect -> manual_digitize
            edge2 = ET.SubElement(graph_root, 'mxCell', {
                'id': 'edge_manual_2', 'edge': '1', 'parent': '1',
                'source': 'manual_collect', 'target': 'manual_digitize',
                'style': 'endArrow=block;rounded=0;entryX=0.5;entryY=0;exitX=0.5;exitY=1;' 
            })
            ET.SubElement(edge2, 'mxGeometry', {'relative': '1', 'as': 'geometry'})

            # manual_digitize -> p2_create
            edge3 = ET.SubElement(graph_root, 'mxCell', {
                'id': 'edge_manual_3', 'edge': '1', 'parent': '1',
                'source': 'manual_digitize', 'target': 'p2_create',
                'style': 'endArrow=block;rounded=0;entryX=0.5;entryY=0;exitX=0.5;exitY=1;' 
            })
            ET.SubElement(edge3, 'mxGeometry', {'relative': '1', 'as': 'geometry'})
            
            print("  Added manual nodes and edges")

    tree.write(file_path, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    file_path = 'docs/diagrams/flowchart_ppt.drawio'
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    
    if os.path.exists(file_path):
        update_gpt_flowchart(file_path)
        print("Done.")
    else:
        print(f"File not found: {file_path}")
