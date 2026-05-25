import xml.etree.ElementTree as ET

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

for edge_id in ['dfd_7103', 'dfd_7105', 'dfd_7107']:
    cell = mx_root.find(f".//mxCell[@id='{edge_id}']")
    if cell is not None:
        print(f"--- EDGE {edge_id} ---")
        for k, v in cell.attrib.items():
            print(f"  {k}: {v}")
