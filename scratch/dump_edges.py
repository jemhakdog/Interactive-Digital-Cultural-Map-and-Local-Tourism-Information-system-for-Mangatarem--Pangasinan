import xml.etree.ElementTree as ET

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v2.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

ar_table_id = "erd_table_6009"
rp_table_id = "erd_table_2009"

print("Edges in erd_v2.drawio:")
for cell in mx_root.findall('mxCell'):
    if cell.attrib.get('edge') == '1':
        src = cell.attrib.get('source', '')
        tgt = cell.attrib.get('target', '')
        val = cell.attrib.get('value', '')
        
        # Check if src or tgt belongs to either table or its rows/columns
        is_relevant = False
        for table_id in [ar_table_id, rp_table_id]:
            if src == table_id or tgt == table_id:
                is_relevant = True
            elif src.startswith(table_id) or tgt.startswith(table_id):
                is_relevant = True
            elif src.startswith("erd_table_11011") or src.startswith("erd_table_11012"):
                is_relevant = True
            elif tgt.startswith("erd_table_11011") or tgt.startswith("erd_table_11012"):
                is_relevant = True
                
        if is_relevant or "review" in val.lower() or "photo" in val.lower():
            print(f"\nEdge ID={cell.attrib.get('id')}, Value={repr(val)}")
            print(f"  Source: {src}")
            print(f"  Target: {tgt}")
            print(f"  Style: {cell.attrib.get('style', '')}")
            geom = cell.find('mxGeometry')
            if geom is not None:
                print(f"  Geometry: {geom.attrib}")
                # check if there are mxPoints (sourcePoint, targetPoint)
                for pt in geom.findall('mxPoint'):
                    print(f"    Point: {pt.attrib}")
