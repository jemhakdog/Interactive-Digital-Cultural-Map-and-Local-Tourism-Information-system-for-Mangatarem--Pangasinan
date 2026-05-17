import xml.etree.ElementTree as ET
import os

def parse_erd():
    erd_path = r"d:\porjects\capstone_system\docs\diagrams\erd\erd_v1.drawio"
    if not os.path.exists(erd_path):
        print(f"Error: {erd_path} not found.")
        return
        
    tree = ET.parse(erd_path)
    root = tree.getroot()
    
    # Let's count elements
    total_cells = 0
    tables = []
    
    for cell in root.iter('mxCell'):
        total_cells += 1
        val = cell.get('value', '')
        cid = cell.get('id', '')
        style = cell.get('style', '')
        
        # If value is uppercase or contains common table characteristics
        if val and ('<' not in val or '<b>' in val.lower()):
            # Let's extract clean text
            clean_val = val.replace('<b>', '').replace('</b>', '').replace('<br>', '\n').strip()
            if len(clean_val) > 2 and clean_val.isupper() and '_' not in clean_val:
                tables.append((cid, clean_val, style))
            elif 'table' in style.lower():
                tables.append((cid, clean_val, style))
                
    print(f"Total cells: {total_cells}")
    print(f"Detected potential table headers/containers ({len(tables)}):")
    for t in tables[:30]:
        print(f"ID: {t[0]} | Value: {repr(t[1])} | Style: {t[2][:50]}...")

if __name__ == '__main__':
    parse_erd()
