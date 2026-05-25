import xml.etree.ElementTree as ET

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

cell = mx_root.find(".//mxCell[@id='dfd_7126']")
if cell is not None:
    print(f"ID: {cell.attrib.get('id')}")
    print(f"Value: '{cell.attrib.get('value')}'")
    print(f"Source: {cell.attrib.get('source')}")
    print(f"Target: {cell.attrib.get('target')}")
    # print all attributes
    for k, v in cell.attrib.items():
        print(f"  {k}: {v}")
