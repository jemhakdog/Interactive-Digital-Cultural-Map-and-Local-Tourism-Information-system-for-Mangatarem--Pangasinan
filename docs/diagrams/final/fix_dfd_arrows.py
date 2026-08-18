import xml.etree.ElementTree as ET

file_path = 'docs/diagrams/final/dfd-level-1-clean_v1.drawio'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

try:
    tree = ET.fromstring(content)
    root = tree.find('.//root')
    
    labels = ["Natural_Heritage", "Intangible_Heritage", "Cultural_Inst", "LGU_Program", "Personality", "Built_Heritage", "Movable_Heritage", "Heritage Management"]
    
    node_mapping = {}
    
    for cell in root.findall('.//mxCell'):
        value = cell.get('value', '')
        cell_id = cell.get('id', '')
        
        for label in labels:
            if label in value and cell.get('edge') != '1':
                node_mapping[cell_id] = label
                
    edges_to_update = 0
    for cell in root.findall('.//mxCell'):
        if cell.get('edge') == '1':
            s = cell.get('source')
            t = cell.get('target')
            
            s_label = node_mapping.get(s, "")
            t_label = node_mapping.get(t, "")
            
            if (s_label == "Heritage Management" and t_label in labels and t_label != "Heritage Management") or \
               (t_label == "Heritage Management" and s_label in labels and s_label != "Heritage Management"):
                
                print(f"Match: {cell.get('id')}")
                style = cell.get('style', '')
                print(f"Old Style: {style}")
                if 'startArrow=' not in style and 'endArrow=classic' in style:
                    new_style = style.replace('endArrow=classic', 'endArrow=classic;startArrow=classic;startFill=1')
                    cell.set('style', new_style)
                    edges_to_update += 1
                elif 'startArrow=classic' not in style and 'endArrow=classic' not in style:
                    new_style = style + ';startArrow=classic;startFill=1;endArrow=classic;endFill=1'
                    cell.set('style', new_style)
                    edges_to_update += 1
                
    if edges_to_update > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(ET.tostring(tree, encoding='unicode', method='xml'))
        print(f"Updated {edges_to_update} arrows to be bidirectional in dfd-level-1-clean_v1!")
    else:
        print("No edges needed updating or already updated.")

except Exception as e:
    print(f"Error parsing XML: {e}")
