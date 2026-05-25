import xml.etree.ElementTree as ET
import re
import sys

# Force stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

print("--- DETECTING FLOATING AND CONTROL POINT EDGES IN ERD ---")
count = 0
for cell in mx_root.findall('mxCell'):
    if cell.attrib.get('edge') == "1":
        cid = cell.attrib.get('id')
        val = cell.attrib.get('value', '')
        clean_val = re.sub('<[^<]+?>', '', val).strip().replace('\n', ' ')
        
        geom = cell.find('mxGeometry')
        if geom is not None:
            source_pt = geom.find("mxPoint[@as='sourcePoint']")
            target_pt = geom.find("mxPoint[@as='targetPoint']")
            points_node = geom.find('Array')
            
            has_absolute = (source_pt is not None) or (target_pt is not None) or (points_node is not None)
            
            if has_absolute:
                count += 1
                print(f"Edge ID: {cid:15} | Val: '{clean_val:30}'")
                if source_pt is not None:
                    print(f"  -> Absolute SourcePoint: {source_pt.attrib}")
                if target_pt is not None:
                    print(f"  -> Absolute TargetPoint: {target_pt.attrib}")
                if points_node is not None:
                    pts = points_node.findall('mxPoint')
                    print(f"  -> Custom Control Points: {len(pts)} points found.")

print(f"\nTotal jumbled/floating edges found in ERD: {count}")
