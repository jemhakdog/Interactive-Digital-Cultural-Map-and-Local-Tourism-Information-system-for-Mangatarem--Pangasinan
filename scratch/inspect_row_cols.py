import xml.etree.ElementTree as ET

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

print("Row 0:")
row = mx_root.find(".//*[@id='erd_table_2001_row_0']")
if row is not None:
    print(ET.tostring(row, encoding='utf-8').decode('utf-8'))
    for col in mx_root.findall(f".//*[@parent='erd_table_2001_row_0']"):
        print(f"  Col: {ET.tostring(col, encoding='utf-8').decode('utf-8')}")
