import xml.etree.ElementTree as ET
from collections import Counter

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

ids = []
for cell in mx_root.findall('.//mxCell'):
    cid = cell.attrib.get('id')
    if cid:
        ids.append(cid)

duplicates = [item for item, count in Counter(ids).items() if count > 1]
print("Duplicate IDs found in erd_v3.drawio:")
for dup in duplicates:
    count = ids.count(dup)
    print(f" - {dup}: {count} occurrences")
