import xml.etree.ElementTree as ET
import sys

# Force stdout to use utf-8
sys.stdout.reconfigure(encoding='utf-8')

file_path = "d:/porjects/capstone_system/docs/diagrams/dfd/dfd-level-1-clean_v3.drawio"
tree = ET.parse(file_path)
root = tree.getroot()
mx_root = root.find('.//root')

if mx_root is None:
    print("Error: Could not find XML root.")
    sys.exit(1)

# Collect all valid cell IDs in the file
cell_ids = set()
for cell in mx_root.findall('mxCell'):
    cid = cell.attrib.get('id')
    if cid:
        cell_ids.add(cid)

print(f"Total valid cells in DFD: {len(cell_ids)}")

errors = 0
verified_edges = 0

print("--- STARTING RIGOROUS EDGE AUDIT ---")
for cell in mx_root.findall('mxCell'):
    if cell.attrib.get('edge') == "1":
        cid = cell.attrib.get('id')
        val = cell.attrib.get('value', '').replace('\n', ' ')
        src = cell.attrib.get('source')
        tgt = cell.attrib.get('target')
        
        # Check 1: Must have source and target
        if not src:
            print(f"ERROR: Edge ID {cid} ('{val}') is missing a source!")
            errors += 1
        elif src not in cell_ids:
            print(f"ERROR: Edge ID {cid} ('{val}') source '{src}' does not exist in DFD cells!")
            errors += 1
            
        if not tgt:
            print(f"ERROR: Edge ID {cid} ('{val}') is missing a target!")
            errors += 1
        elif tgt not in cell_ids:
            print(f"ERROR: Edge ID {cid} ('{val}') target '{tgt}' does not exist in DFD cells!")
            errors += 1
            
        # Check 2: Geometry overrides
        geom = cell.find('mxGeometry')
        if geom is not None:
            source_pt = geom.find("mxPoint[@as='sourcePoint']")
            target_pt = geom.find("mxPoint[@as='targetPoint']")
            points_node = geom.find('Array')
            
            if source_pt is not None:
                print(f"ERROR: Edge ID {cid} ('{val}') contains an absolute sourcePoint override!")
                errors += 1
            if target_pt is not None:
                print(f"ERROR: Edge ID {cid} ('{val}') contains an absolute targetPoint override!")
                errors += 1
            if points_node is not None:
                print(f"ERROR: Edge ID {cid} ('{val}') contains a custom control points array!")
                errors += 1
                
        verified_edges += 1

print("\n--- AUDIT SUMMARY ---")
print(f"Total edges audited: {verified_edges}")
print(f"Total alignment or connection errors found: {errors}")

if errors == 0:
    print("SUCCESS: 100% of data flow lines are mathematically snapped, fully connected at both ends, and free from coordinate overlays!")
    sys.exit(0)
else:
    sys.exit(1)
