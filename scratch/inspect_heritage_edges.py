import xml.etree.ElementTree as ET
import sys

# Force stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

# Obsolete store containers & child labels
obsolete_ids = [
    'dfd_7048', 'dfd_7049', # 16
    'dfd_7051', 'dfd_7052', # 17
    'dfd_7054', 'dfd_7055', # 10
    'dfd_7057', 'dfd_7058', # 11
    'dfd_7060', 'dfd_7061', 'dfd_7062', # 12
    'dfd_7063', 'dfd_7064', 'dfd_7065', # 13
    'dfd_7066', 'dfd_7067', 'dfd_7068'  # 14
]

print("--- INCOMING / OUTGOING EDGES FOR OBSOLETE STORES ---")
for cell in mx_root.findall('mxCell'):
    if cell.attrib.get('edge') == "1":
        src = cell.attrib.get('source')
        tgt = cell.attrib.get('target')
        val = cell.attrib.get('value', '')
        cid = cell.attrib.get('id')
        
        # Check if source or target is in the obsolete list or nested children of obsolete parents
        is_linked = (src in obsolete_ids or tgt in obsolete_ids)
        
        # Or check if parent of source/target is in obsolete list
        src_cell = mx_root.find(f".//mxCell[@id='{src}']") if src else None
        tgt_cell = mx_root.find(f".//mxCell[@id='{tgt}']") if tgt else None
        
        src_parent = src_cell.attrib.get('parent') if src_cell is not None else None
        tgt_parent = tgt_cell.attrib.get('parent') if tgt_cell is not None else None
        
        if is_linked or src_parent in obsolete_ids or tgt_parent in obsolete_ids:
            print(f"Edge ID: {cid:15} | Val: '{val:25}' | Src: {src} (Parent: {src_parent}) | Tgt: {tgt} (Parent: {tgt_parent})")
