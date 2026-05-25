import xml.etree.ElementTree as ET
import sys

# Force stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

# Helper to find cell clean value
def get_cell_val(cid):
    if not cid:
        return "None"
    cell = mx_root.find(f".//mxCell[@id='{cid}']")
    if cell is None:
        return "Not Found"
    val = cell.attrib.get('value', '')
    import re
    clean_val = re.sub('<[^<]+?>', '', val).strip().replace('\n', ' ')
    if not clean_val and cell.attrib.get('parent') != '1':
        # try parent
        parent_id = cell.attrib.get('parent')
        parent_val = get_cell_val(parent_id)
        return f"[Child of {parent_id}: {parent_val}]"
    return clean_val if clean_val else "[Empty]"

print("--- ALL EDGES IN DFD ---")
for cell in mx_root.findall('mxCell'):
    if cell.attrib.get('edge') == "1":
        cid = cell.attrib.get('id')
        src = cell.attrib.get('source')
        tgt = cell.attrib.get('target')
        val = cell.attrib.get('value', '')
        style = cell.attrib.get('style', '')
        
        # Check mxGeometry children (points)
        geom = cell.find('mxGeometry')
        points_info = "No points"
        has_source_point = False
        has_target_point = False
        if geom is not None:
            points_node = geom.find('Array')
            if points_node is not None:
                points_info = f"Has {len(points_node.findall('mxPoint'))} custom points"
            
            source_pt = geom.find("mxPoint[@as='sourcePoint']")
            target_pt = geom.find("mxPoint[@as='targetPoint']")
            if source_pt is not None:
                has_source_point = True
            if target_pt is not None:
                has_target_point = True
                
        src_val = get_cell_val(src)
        tgt_val = get_cell_val(tgt)
        
        print(f"Edge ID: {cid:15} | Val: '{val:25}'")
        print(f"  Source: {src} ('{src_val}') | Target: {tgt} ('{tgt_val}')")
        print(f"  Geom: {points_info} | HasSourcePt: {has_source_point} | HasTargetPt: {has_target_point}")
        print(f"  Style: {style[:80]}...")
