import os
import xml.etree.ElementTree as ET

erd_path = 'D:/porjects/capstone_system/docs/diagrams/erd/erd_v2.drawio'
dfd_path = 'D:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v2.drawio'

tables_to_remove = [
    "BUILT_HERITAGE_DETAIL",
    "NATURAL_HERITAGE_DETAIL",
    "MOVABLE_HERITAGE_DETAIL",
    "INTANGIBLE_HERITAGE_DETAIL",
    "PERSONALITY_DETAIL",
    "INSTITUTION_DETAIL",
    "LGU_PROGRAM_DETAIL",
    "ATTRACTION_REVIEW",
    "ESTABLISHMENT_REVIEW",
    "USER_EVENT_INTEREST",
    "USER_FAVORITE_ATTRACTION",
    "USER_FAVORITE_ESTABLISHMENT"
]

def clean_drawio(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Processing {file_path}")
    
    # Read as text first to handle potential encoding issues, Drawio might be compressed
    # Usually .drawio is uncompressed XML if edited in VS Code
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # In Drawio, the structure is usually:
        # <mxfile> -> <diagram> -> <mxGraphModel> -> <root> -> <mxCell>
        diagram = root.find('.//root')
        if diagram is None:
            print("Could not find <root> in mxGraphModel")
            return
            
        cells = list(diagram)
        
        # 1. Identify IDs of tables to remove
        ids_to_remove = set()
        for cell in cells:
            val = cell.get('value', '')
            # Strip html tags if any
            clean_val = val.replace('<b>', '').replace('</b>', '').strip()
            if clean_val in tables_to_remove:
                ids_to_remove.add(cell.get('id'))
                print(f"Found table to remove: {clean_val} (id={cell.get('id')})")
                
        if not ids_to_remove:
            print("No tables found to remove.")
            return
            
        # 2. Iteratively find all children and edges
        changed = True
        while changed:
            changed = False
            for cell in cells:
                cell_id = cell.get('id')
                parent_id = cell.get('parent')
                source_id = cell.get('source')
                target_id = cell.get('target')
                
                if cell_id not in ids_to_remove:
                    if parent_id in ids_to_remove or source_id in ids_to_remove or target_id in ids_to_remove:
                        ids_to_remove.add(cell_id)
                        changed = True
                        
        # 3. Remove them from the tree
        removed_count = 0
        for cell in cells:
            if cell.get('id') in ids_to_remove:
                diagram.remove(cell)
                removed_count += 1
                
        print(f"Removed {removed_count} cells.")
        
        tree.write(file_path, encoding='utf-8', xml_declaration=False)
        print("Saved.")
        
    except Exception as e:
        print(f"Error: {e}")

clean_drawio(erd_path)
clean_drawio(dfd_path)
