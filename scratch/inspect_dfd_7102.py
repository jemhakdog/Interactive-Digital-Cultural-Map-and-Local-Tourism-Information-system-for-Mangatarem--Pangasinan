import xml.etree.ElementTree as ET

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

cell = mx_root.find(".//mxCell[@id='dfd_7102']")
if cell is not None:
    print("--- EDGE dfd_7102 (Map View Request) ---")
    for k, v in cell.attrib.items():
        print(f"  {k}: {v}")
