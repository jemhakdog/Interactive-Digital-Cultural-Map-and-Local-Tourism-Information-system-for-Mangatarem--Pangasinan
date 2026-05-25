import xml.etree.ElementTree as ET
import sys

# Force stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

heritage_edges = [
    'dfd_7116', 'dfd_7117', 'dfd_7118', 'dfd_7119', 'dfd_7120', 'dfd_7122', 'dfd_7123', 'dfd_7124', 'dfd_7126'
]

print("--- HERITAGE CLUSTER EDGES DETAIL ---")
for eid in heritage_edges:
    cell = mx_root.find(f".//mxCell[@id='{eid}']")
    if cell is not None:
        print(f"Edge ID: {eid} | Val: '{cell.attrib.get('value')}'")
        print(f"  Src: {cell.attrib.get('source')} | Tgt: {cell.attrib.get('target')}")
        print(f"  Style: {cell.attrib.get('style')}")
        geom = cell.find('mxGeometry')
        if geom is not None:
            print(f"  Geom: relative={geom.attrib.get('relative')}")
            for child in geom:
                # print points, sourcePoint, targetPoint
                print(f"    Child tag: {child.tag} | attrs: {child.attrib}")
