import xml.etree.ElementTree as ET
import re

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v2.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

print("--- DATA STORES & PROCESSES IN DFD V2 ---")
for cell in mx_root.findall('mxCell'):
    val = cell.attrib.get('value', '')
    if val:
        clean_val = re.sub('<[^<]+?>', '', val).strip()
        clean_val = clean_val.replace('&amp;', '&').replace('\n', ' ')
        cid = cell.attrib.get('id')
        style = cell.attrib.get('style', '')
        
        # Check if it looks like a data store or a process
        # Data stores often have values starting with "D" (e.g., "D1", "D2", "D1: USER") or contain "Data Store" style
        # Processes have numbers like "1.0", "2.0"
        if any(keyword in clean_val for keyword in ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15", "D16", "D17", "D18", "D19", "D20", "D21", "D22", "D23", "D24", "D25", "D26", "D27"]):
            print(f"Data Store? ID: {cid} | Val: {clean_val}")
        elif re.match(r'^\d+\.\d+$', clean_val) or any(p in clean_val for p in ["Authentication", "Management", "Approval", "Map", "Discovery", "Booking", "Chat", "Analytics", "Notification"]):
            print(f"Process/Component? ID: {cid} | Val: {clean_val} | Style: {style[:30]}...")
