import xml.etree.ElementTree as ET
import re
import sys

# Force stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

file_path = "d:/porjects/capstone_system/docs/diagrams/erd/erd_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

def get_descendants_info(parent_id):
    for cell in mx_root.findall('mxCell'):
        if cell.attrib.get('parent') == parent_id:
            val = cell.attrib.get('value', '')
            clean_val = re.sub('<[^<]+?>', '', val).strip()
            print(f"Child of {parent_id} -> ID: {cell.attrib.get('id')} | Val: '{clean_val}'")
            # recursively get children
            get_descendants_info(cell.attrib.get('id'))

print("--- DESCENDANTS OF erd_table_6009 (ATTRACTION_REVIEW) ---")
get_descendants_info('erd_table_6009')
