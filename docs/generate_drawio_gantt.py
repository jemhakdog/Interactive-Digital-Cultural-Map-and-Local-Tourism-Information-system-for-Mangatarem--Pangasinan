import xml.etree.ElementTree as ET


def create_cell(parent, id, value, x, y, width, height, style):
    cell = ET.SubElement(parent, 'mxCell', id=str(id), value=value, style=style, vertex="1", parent="1")
    geo = ET.SubElement(cell, 'mxGeometry', x=str(x), y=str(y), width=str(width), height=str(height))
    geo.set('as', 'geometry')
    return id + 1

def generate_drawio():
    mxfile = ET.Element('mxfile', version="21.6.8", type="device")
    diagram = ET.SubElement(mxfile, 'diagram', id="timeline", name="Gantt")
    model = ET.SubElement(diagram, 'mxGraphModel', dx="1434", dy="836", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="1169", pageHeight="827", math="0", shadow="0")
    root = ET.SubElement(model, 'root')
    
    ET.SubElement(root, 'mxCell', id="0")
    ET.SubElement(root, 'mxCell', id="1", parent="0")

    cell_id = 2
    
    # Styles
    header_style = "rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;fontColor=#000000;fontStyle=1;"
    cell_style = "rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;fontColor=#000000;"
    fill_style = "rounded=0;whiteSpace=wrap;html=1;fillColor=#99ccff;strokeColor=#000000;fontColor=#000000;"
    
    start_x = 40
    start_y = 40
    
    col_task_w = 160
    col_month_w = 160
    col_week_w = 40
    col_personnel_w = 160
    
    row_h = 40
    header_h = 30
    
    # Row 1: Top Headers
    # Task (spans 2 rows)
    cell_id = create_cell(root, cell_id, "Task", start_x, start_y, col_task_w, header_h * 2, header_style)
    
    # Months
    months = ["Feb 2026", "March 2026", "April 2026", "May 2026"]
    for i, month in enumerate(months):
        cell_id = create_cell(root, cell_id, month, start_x + col_task_w + (i * col_month_w), start_y, col_month_w, header_h, header_style)
        
    # Key Personnel (spans 2 rows)
    cell_id = create_cell(root, cell_id, "Key personnel", start_x + col_task_w + (4 * col_month_w), start_y, col_personnel_w, header_h * 2, header_style)
    
    # Row 2: Weeks
    for m in range(4):
        for w in range(4):
            x = start_x + col_task_w + (m * col_month_w) + (w * col_week_w)
            cell_id = create_cell(root, cell_id, f"W{w+1}", x, start_y + header_h, col_week_w, header_h, header_style)

    # Tasks Data
    tasks = [
        {"name": "Requirements\nplanning", "personnel": "Team B3 and\nstakeholder", "start_m": 0, "start_w": 0, "dur": 1},
        {"name": "User Design", "personnel": "Team B3 and\nstakeholder", "start_m": 0, "start_w": 1, "dur": 1},
        {"name": "Rapid Construction\n(development)", "personnel": "Team B3 Leader", "start_m": 0, "start_w": 2, "dur": 12}, # Feb W3 to May W2 = 2 (Feb) + 4 (Mar) + 4 (Apr) + 2 (May) = 12 weeks
        {"name": "Cutover\n(Deployment, testing,\nuser training)", "personnel": "Team B3 and\nsystem users", "start_m": 3, "start_w": 2, "dur": 2}
    ]
    
    current_y = start_y + (header_h * 2)
    
    for r, task in enumerate(tasks):
        # Task Name
        cell_id = create_cell(root, cell_id, task["name"], start_x, current_y, col_task_w, row_h, cell_style)
        
        # Grid and Fills
        for m in range(4):
            for w in range(4):
                week_idx = (m * 4) + w
                task_start_idx = (task["start_m"] * 4) + task["start_w"]
                task_end_idx = task_start_idx + task["dur"] - 1
                
                style = fill_style if (task_start_idx <= week_idx <= task_end_idx) else cell_style
                val = ""
                x = start_x + col_task_w + (m * col_month_w) + (w * col_week_w)
                cell_id = create_cell(root, cell_id, val, x, current_y, col_week_w, row_h, style)
                
        # Key Personnel
        cell_id = create_cell(root, cell_id, task["personnel"], start_x + col_task_w + (4 * col_month_w), current_y, col_personnel_w, row_h, cell_style)
        
        current_y += row_h

    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space="\t", level=0)
    tree.write("d:/porjects/capstone_system/docs/capstone/screenshots/timeline_rad.drawio", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    generate_drawio()
