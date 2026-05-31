import xml.etree.ElementTree as ET

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

table = mx_root.find(".//*[@id='erd_table_2001']")
if table is not None:
    print(f"Style: {table.attrib.get('style')}")
