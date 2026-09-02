import xml.etree.ElementTree as ET

file_path = 'docs/diagrams/final/dfd-level-1-clean_v1.drawio'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

try:
    tree = ET.fromstring(content)
    root = tree.find('.//root')
    
    # Just print all cells with value containing 'Heritage Management'
    for cell in root.findall('.//mxCell'):
        val = cell.get('value', '')
        if 'Heritage Management' in val and cell.get('edge') != '1':
            print(f"FOUND Heritage Management: ID={cell.get('id')} Value={val[:20]}")
            
    # Also print all cells with 'Built_Heritage'
    for cell in root.findall('.//mxCell'):
        val = cell.get('value', '')
        if 'Built_Heritage' in val and cell.get('edge') != '1':
            print(f"FOUND Built_Heritage: ID={cell.get('id')} Value={val[:20]}")

    print("\nEDGES connected to Heritage Management:")
    for cell in root.findall('.//mxCell'):
        if cell.get('edge') == '1':
            s = cell.get('source')
            t = cell.get('target')
            
            # Print if source or target looks like one of the nodes
            if s and t:
                # We will check manually based on the IDs
                print(f"Edge {cell.get('id')}: {s} -> {t}")

except ET.ParseError as e:
    print(f"Error parsing XML: {e}")
