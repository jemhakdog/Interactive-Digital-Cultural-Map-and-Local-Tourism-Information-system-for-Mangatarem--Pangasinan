import xml.etree.ElementTree as ET

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

labels = []
for cell in mx_root.findall('mxCell'):
    val = cell.attrib.get('value', '')
    if val:
        labels.append(val)

print("Unique labels in DFD:")
for l in sorted(list(set(labels))):
    print(f" - {l}")
