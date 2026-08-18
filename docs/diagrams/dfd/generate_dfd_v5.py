import xml.etree.ElementTree as ET
import os

def create_dfd_v5():
    print("Initializing Draw.io Level-1 Hub-and-Spoke DFD V5 generator...")
    
    # Create the root structures
    mxfile = ET.Element('mxfile', attrib={'host': 'Electron'})
    diagram = ET.SubElement(mxfile, 'diagram', attrib={'name': 'Hub-and-Spoke DFD V5', 'id': 'DFD_V5'})
    mxGraphModel = ET.SubElement(diagram, 'mxGraphModel', attrib={
        'dx': '4000', 'dy': '3500', 'grid': '1', 'gridSize': '10',
        'guides': '1', 'tooltips': '1', 'connect': '1', 'arrows': '1',
        'fold': '1', 'page': '1', 'pageScale': '1', 'pageWidth': '2600',
        'pageHeight': '2400', 'background': '#F5F9F5', 'math': '0', 'shadow': '0'
    })
    root = ET.SubElement(mxGraphModel, 'root')
    
    # Draw.io default layer cells
    ET.SubElement(root, 'mxCell', attrib={'id': '0'})
    ET.SubElement(root, 'mxCell', attrib={'id': '1', 'parent': '0'})
    
    # 1. HUGE Central Hub Process Box
    proc_0_grp = ET.SubElement(root, 'mxCell', attrib={
        'id': 'proc_0_grp',
        'parent': '1',
        'style': 'group;container=1;collapsible=0;pointerEvents=0;fontSize=14;',
        'value': '',
        'vertex': '1'
    })
    ET.SubElement(proc_0_grp, 'mxGeometry', attrib={
        'x': '950', 'y': '950', 'width': '600', 'height': '350',
        'as': 'geometry'
    })
    
    # Number box at top of central hub
    num_cell = ET.SubElement(root, 'mxCell', attrib={
        'id': 'proc_0_num',
        'parent': 'proc_0_grp',
        'style': 'rounded=1;whiteSpace=wrap;html=1;fillColor=#BDD7EE;strokeColor=#000000;fontStyle=1;fontColor=#000000;align=center;verticalAlign=middle;strokeWidth=2.5;fontSize=14;',
        'value': 'SYSTEM HUB',
        'vertex': '1'
    })
    ET.SubElement(num_cell, 'mxGeometry', attrib={
        'width': '600', 'height': '40',
        'as': 'geometry'
    })
    
    # System title box
    name_cell = ET.SubElement(root, 'mxCell', attrib={
        'id': 'proc_0',
        'parent': 'proc_0_grp',
        'style': 'rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;align=center;verticalAlign=middle;fontSize=16;strokeWidth=3;fontStyle=1;',
        'value': 'Interactive Digital Cultural Map &amp; Tourism Information System',
        'vertex': '1'
    })
    ET.SubElement(name_cell, 'mxGeometry', attrib={
        'y': '40', 'width': '600', 'height': '310',
        'as': 'geometry'
    })

    # Common dimensions
    entity_w, entity_h = 150, 150
    proc_w, proc_h = 180, 80
    store_w, store_h = 160, 45

    # 2. External Entities (On the outer perimeter)
    entities = {
        'TOURIST': {'id': 'ent_tourist', 'x': 50, 'y': 900, 'w': 150, 'h': 500, 'color': '#BDD7EE'},
        'HERITAGE_GUARDIAN': {'id': 'ent_guardian', 'x': 2300, 'y': 700, 'w': 150, 'h': 150, 'color': '#D5E8D4'},
        'BUSINESS_OWNER': {'id': 'ent_business', 'x': 2300, 'y': 1000, 'w': 150, 'h': 150, 'color': '#FFE6CC'},
        'ADMIN': {'id': 'ent_admin', 'x': 2300, 'y': 1300, 'w': 150, 'h': 500, 'color': '#C5E1A5'}
    }
    
    # Helper APIs (External Interfaces)
    apis = {
        'api_google': {'id': 'api_g', 'name': 'Google OAuth API', 'x': 450, 'y': 150, 'w': 180, 'h': 40},
        'api_mapbox': {'id': 'api_m', 'name': 'Mapbox Directions API', 'x': 750, 'y': 150, 'w': 180, 'h': 40}
    }

    # 3. Peripheral Processes (Arrayed in a clean rectangular grid surrounding the hub)
    # Double rounded compartments as per v4
    processes = {
        # Top Row (y = 450)
        'p1': {'id': 'proc_1', 'num': '1.0', 'name': 'User Onboarding\n& Authentication', 'x': 450, 'y': 450},
        'p14': {'id': 'proc_14', 'num': '14.0', 'name': 'Analytics &\nReporting Engine', 'x': 800, 'y': 450},
        'p13': {'id': 'proc_13', 'num': '13.0', 'name': 'Content Verification\n& Approval', 'x': 1150, 'y': 450},
        'p15': {'id': 'proc_15', 'num': '15.0', 'name': 'Audit Logging &\nSecurity Registry', 'x': 1500, 'y': 450},
        'p12': {'id': 'proc_12', 'num': '12.0', 'name': 'Media Gallery\nManagement', 'x': 1850, 'y': 450},
        
        # Left Column (x = 450)
        'p2': {'id': 'proc_2', 'num': '2.0', 'name': 'Interactive Map\nExploration', 'x': 450, 'y': 750},
        'p3': {'id': 'proc_3', 'num': '3.0', 'name': 'Heritage Catalog\nDiscovery', 'x': 450, 'y': 1050},
        'p4': {'id': 'proc_4', 'num': '4.0', 'name': 'Review &\nFeedback Management', 'x': 450, 'y': 1350},
        'p5': {'id': 'proc_5', 'num': '5.0', 'name': 'Favorite Spotlight\nManagement', 'x': 450, 'y': 1650},
        
        # Bottom Row (y = 1950)
        'p6': {'id': 'proc_6', 'num': '6.0', 'name': 'Booking &\nReservations Network', 'x': 600, 'y': 1950},
        'p7': {'id': 'proc_7', 'num': '7.0', 'name': 'Chat Messaging\nNetwork', 'x': 1150, 'y': 1950},
        'p8': {'id': 'proc_8', 'num': '8.0', 'name': 'Newsletter\nSubscription', 'x': 1700, 'y': 1950},
        
        # Right Column (x = 1850)
        'p9': {'id': 'proc_9', 'num': '9.0', 'name': 'Attraction Content\nManagement', 'x': 1850, 'y': 750},
        'p10': {'id': 'proc_10', 'num': '10.0', 'name': 'Heritage Form\nSubmissions', 'x': 1850, 'y': 1100},
        'p11': {'id': 'proc_11', 'num': '11.0', 'name': 'Establishment\nListing Management', 'x': 1850, 'y': 1450}
    }

    # 4. Local Datastores (Placed directly adjacent to or underneath their corresponding processes)
    datastores = {
        'db_user': {'id': 'db_1', 'num': 'D1', 'name': 'User_db', 'x': 450, 'y': 550},
        'db_vlog': {'id': 'db_12', 'num': 'D12', 'name': 'Visitor_Log_db', 'x': 800, 'y': 550},
        'db_verify': {'id': 'db_15', 'num': 'D15', 'name': 'Business_Verification_db', 'x': 1150, 'y': 550},
        'db_alog': {'id': 'db_13', 'num': 'D13', 'name': 'Audit_Log_db', 'x': 1500, 'y': 550},
        'db_gal': {'id': 'db_11', 'num': 'D11', 'name': 'Gallery_db', 'x': 1850, 'y': 550},
        
        'db_attr': {'id': 'db_2', 'num': 'D2', 'name': 'Attraction_db', 'x': 250, 'y': 765},
        'db_event': {'id': 'db_3', 'num': 'D3', 'name': 'Event_db', 'x': 250, 'y': 1065},
        'db_rev': {'id': 'db_5', 'num': 'D5', 'name': 'Review_db', 'x': 250, 'y': 1365},
        'db_fav': {'id': 'db_6', 'num': 'D6', 'name': 'Favorite_db', 'x': 250, 'y': 1665},
        
        'db_book': {'id': 'db_7', 'num': 'D7', 'name': 'Booking_db', 'x': 600, 'y': 2050},
        'db_chat': {'id': 'db_8', 'num': 'D8', 'name': 'Chat_db', 'x': 1150, 'y': 2050},
        'db_news': {'id': 'db_9', 'num': 'D9', 'name': 'Newsletter_db', 'x': 1700, 'y': 2050},
        
        'db_attr_dup': {'id': 'db_2_dup', 'num': 'D2', 'name': 'Attraction_db (Copy)', 'x': 2050, 'y': 765},
        'db_event_dup': {'id': 'db_3_dup', 'num': 'D3', 'name': 'Event_db (Copy)', 'x': 2050, 'y': 1115},
        'db_est': {'id': 'db_10', 'num': 'D10', 'name': 'Establishment_db', 'x': 2050, 'y': 1465},
        
        # Local non-crossover datastores
        'db_brgy': {'id': 'db_4', 'num': 'D4', 'name': 'Barangay_db', 'x': 650, 'y': 750},
        'db_mapfeed': {'id': 'db_14', 'num': 'D14', 'name': 'Map_Feedback_db', 'x': 650, 'y': 1350},
        'db_notif': {'id': 'db_16', 'num': 'D16', 'name': 'Notification_db', 'x': 800, 'y': 1950}
    }

    # Render Entities
    for key, info in entities.items():
        entity_cell = ET.SubElement(root, 'mxCell', attrib={
            'id': info['id'],
            'parent': '1',
            'style': f'rounded=0;whiteSpace=wrap;html=1;fillColor={info["color"]};strokeColor=#000000;fontStyle=1;fontColor=#000000;fontSize=13;horizontal=0;strokeWidth=2;',
            'value': key.replace('_', ' '),
            'vertex': '1'
        })
        ET.SubElement(entity_cell, 'mxGeometry', attrib={
            'x': str(info['x']), 'y': str(info['y']), 'width': str(info['w']), 'height': str(info['h']),
            'as': 'geometry'
        })

    # Render Apis
    for key, info in apis.items():
        api_cell = ET.SubElement(root, 'mxCell', attrib={
            'id': info['id'],
            'parent': '1',
            'style': 'rounded=0;whiteSpace=wrap;html=1;fillColor=#FFF2CC;strokeColor=#D6B656;fontStyle=1;fontColor=#000000;fontSize=12;strokeWidth=1.5;',
            'value': info['name'],
            'vertex': '1'
        })
        ET.SubElement(api_cell, 'mxGeometry', attrib={
            'x': str(info['x']), 'y': str(info['y']), 'width': str(info['w']), 'height': str(info['h']),
            'as': 'geometry'
        })

    # Render Processes (Double compartments)
    for key, info in processes.items():
        grp_cell = ET.SubElement(root, 'mxCell', attrib={
            'id': f"{info['id']}_grp",
            'parent': '1',
            'style': 'group;container=1;collapsible=0;pointerEvents=0;fontSize=13;',
            'value': '',
            'vertex': '1'
        })
        ET.SubElement(grp_cell, 'mxGeometry', attrib={
            'x': str(info['x']), 'y': str(info['y']), 'width': str(proc_w), 'height': str(proc_h),
            'as': 'geometry'
        })
        
        num_cell = ET.SubElement(root, 'mxCell', attrib={
            'id': f"{info['id']}_num",
            'parent': f"{info['id']}_grp",
            'style': 'rounded=1;whiteSpace=wrap;html=1;fillColor=#BDD7EE;strokeColor=#000000;fontStyle=1;fontColor=#000000;align=center;verticalAlign=middle;strokeWidth=1.5;fontSize=13;',
            'value': info['num'],
            'vertex': '1'
        })
        ET.SubElement(num_cell, 'mxGeometry', attrib={
            'width': str(proc_w), 'height': '25',
            'as': 'geometry'
        })
        
        name_cell = ET.SubElement(root, 'mxCell', attrib={
            'id': info['id'],
            'parent': f"{info['id']}_grp",
            'style': 'rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;align=center;verticalAlign=middle;fontSize=13;strokeWidth=1.5;',
            'value': info['name'],
            'vertex': '1'
        })
        ET.SubElement(name_cell, 'mxGeometry', attrib={
            'y': '25', 'width': str(proc_w), 'height': '55',
            'as': 'geometry'
        })

    # Render Datastores (Double compartments)
    for key, info in datastores.items():
        grp_cell = ET.SubElement(root, 'mxCell', attrib={
            'id': f"{info['id']}_grp",
            'parent': '1',
            'style': 'group;fontSize=13;',
            'value': '',
            'vertex': '1'
        })
        ET.SubElement(grp_cell, 'mxGeometry', attrib={
            'x': str(info['x']), 'y': str(info['y']), 'width': str(store_w), 'height': str(store_h),
            'as': 'geometry'
        })
        
        id_cell = ET.SubElement(root, 'mxCell', attrib={
            'id': f"{info['id']}_num",
            'parent': f"{info['id']}_grp",
            'style': 'rounded=0;whiteSpace=wrap;html=1;fillColor=#BDD7EE;strokeColor=#000000;fontStyle=1;fontColor=#000000;align=center;strokeWidth=1.5;fontSize=13;',
            'value': info['num'],
            'vertex': '1'
        })
        ET.SubElement(id_cell, 'mxGeometry', attrib={
            'width': '35', 'height': str(store_h),
            'as': 'geometry'
        })
        
        lbl_cell = ET.SubElement(root, 'mxCell', attrib={
            'id': info['id'],
            'parent': f"{info['id']}_grp",
            'style': 'rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;align=center;fontSize=13;strokeWidth=1.5;',
            'value': info['name'],
            'vertex': '1'
        })
        ET.SubElement(lbl_cell, 'mxGeometry', attrib={
            'x': '35', 'width': str(store_w - 35), 'height': str(store_h),
            'as': 'geometry'
        })

    # 5. Render Connections
    flows = [
        # --- TOURIST INPUTS (TO LEFT COLUMN & BOTTOM COLUMN) ---
        ('ent_tourist', 'proc_1', 'Credentials', 'exitX=1;exitY=0.08;entryX=0;entryY=0.25;'),
        ('ent_tourist', 'proc_2', 'Search Locality', 'exitX=1;exitY=0.25;entryX=0;entryY=0.25;'),
        ('ent_tourist', 'proc_3', 'Browse Categories', 'exitX=1;exitY=0.45;entryX=0;entryY=0.25;'),
        ('ent_tourist', 'proc_4', 'Submit Review', 'exitX=1;exitY=0.65;entryX=0;entryY=0.25;'),
        ('ent_tourist', 'proc_5', 'Toggle Bookmark', 'exitX=1;exitY=0.85;entryX=0;entryY=0.25;'),
        ('ent_tourist', 'proc_6', 'Reserve Slot', 'exitX=0.8;exitY=1.0;entryX=0;entryY=0.25;'),
        ('ent_tourist', 'proc_7', 'Message Input', 'exitX=0.9;exitY=1.0;entryX=0;entryY=0.25;'),

        # --- PROCESS TO CENTRAL SYSTEM CONNECTIONS ---
        ('proc_1', 'proc_0', 'Profile Created', 'exitX=1;exitY=0.75;entryX=0.1;entryY=0;'),
        ('proc_2', 'proc_0', 'Map Intersect Logs', 'exitX=1;exitY=0.5;entryX=0;entryY=0.2;'),
        ('proc_3', 'proc_0', 'Heritage Search Query', 'exitX=1;exitY=0.5;entryX=0;entryY=0.5;'),
        ('proc_4', 'proc_0', 'Approved Review Data', 'exitX=1;exitY=0.5;entryX=0;entryY=0.8;'),
        ('proc_5', 'proc_0', 'Bookmarked Spots', 'exitX=1;exitY=0.5;entryX=0.25;entryY=1;'),
        ('proc_6', 'proc_0', 'Booking Logs', 'exitX=0.5;exitY=0;entryX=0.35;entryY=1;'),
        ('proc_7', 'proc_0', 'Message History', 'exitX=0.5;exitY=0;entryX=0.65;entryY=1;'),
        ('proc_8', 'proc_0', 'Subscribers List', 'exitX=0.25;exitY=0;entryX=0.8;entryY=1;'),
        
        ('proc_9', 'proc_0', 'Assets Updated', 'exitX=0;exitY=0.5;entryX=1;entryY=0.2;'),
        ('proc_10', 'proc_0', 'Forms Saved', 'exitX=0;exitY=0.5;entryX=1;entryY=0.5;'),
        ('proc_11', 'proc_0', 'Establishment Logs', 'exitX=0;exitY=0.5;entryX=1;entryY=0.8;'),
        ('proc_12', 'proc_0', 'Gallery Logs', 'exitX=0;exitY=0.5;entryX=0.85;entryY=0;'),
        ('proc_13', 'proc_0', 'Verifications', 'exitX=0.5;exitY=1;entryX=0.5;entryY=0;'),
        ('proc_14', 'proc_0', 'Metrics Logs', 'exitX=0.5;exitY=1;entryX=0.3;entryY=0;'),
        ('proc_15', 'proc_0', 'Audits Registered', 'exitX=0;exitY=0.75;entryX=0.7;entryY=0;'),

        # --- LOCAL DATABASE CONNECTIONS ---
        ('proc_1', 'db_1', 'Read/Write User', 'exitX=0.5;exitY=1;entryX=0.5;entryY=0;'),
        ('proc_2', 'db_2', 'Query Attraction', 'exitX=0;exitY=0.75;entryX=1;entryY=0.5;'),
        ('proc_2', 'db_4', 'Fetch Barangay', 'exitX=1;exitY=0.75;entryX=0;entryY=0.5;'),
        ('proc_3', 'db_3', 'Query Event', 'exitX=0;exitY=0.75;entryX=1;entryY=0.5;'),
        ('proc_4', 'db_5', 'Write Review', 'exitX=0;exitY=0.75;entryX=1;entryY=0.5;'),
        ('proc_4', 'db_14', 'Write Feedback', 'exitX=1;exitY=0.75;entryX=0;entryY=0.5;'),
        ('proc_5', 'db_6', 'Write Favorite', 'exitX=0;exitY=0.75;entryX=1;entryY=0.5;'),
        ('proc_6', 'db_7', 'Write Booking', 'exitX=0.5;exitY=1;entryX=0.5;entryY=0;'),
        ('proc_6', 'db_16', 'Queue Notif', 'exitX=1;exitY=0.75;entryX=0;entryY=0.5;'),
        ('proc_7', 'db_8', 'Write Chat', 'exitX=0.5;exitY=1;entryX=0.5;entryY=0;'),
        ('proc_8', 'db_9', 'Save Subscriber', 'exitX=0.5;exitY=1;entryX=0.5;entryY=0;'),
        
        ('proc_9', 'db_2_dup', 'Write Attraction', 'exitX=1;exitY=0.75;entryX=0;entryY=0.5;'),
        ('proc_10', 'db_3_dup', 'Save Form Data', 'exitX=1;exitY=0.75;entryX=0;entryY=0.5;'),
        ('proc_11', 'db_10', 'Register Est', 'exitX=1;exitY=0.75;entryX=0;entryY=0.5;'),
        ('proc_12', 'db_11', 'Write Gallery', 'exitX=0.5;exitY=1;entryX=0.5;entryY=0;'),
        ('proc_13', 'db_15', 'Query Verify', 'exitX=0.5;exitY=1;entryX=0.5;entryY=0;'),
        ('proc_14', 'db_12', 'Logs Metrics', 'exitX=0.5;exitY=1;entryX=0.5;entryY=0;'),
        ('proc_15', 'db_13', 'Register Audit', 'exitX=0.5;exitY=1;entryX=0.5;entryY=0;'),

        # --- API INTERACTIONS ---
        ('proc_1', 'api_g', 'OAuth Validation', 'exitX=0.5;exitY=0;entryX=0.5;entryY=1;'),
        ('proc_2', 'api_m', 'Directions API', 'exitX=0.5;exitY=0;entryX=0.5;entryY=1;'),

        # --- CONTRIBUTOR / ADMIN INPUTS ---
        ('ent_guardian', 'proc_9', 'Upload Assets', 'exitX=0;exitY=0.5;entryX=1;entryY=0.25;'),
        ('ent_guardian', 'proc_10', 'Submit Form', 'exitX=0;exitY=0.8;entryX=1;entryY=0.25;'),
        ('ent_business', 'proc_11', 'Submit Permit', 'exitX=0;exitY=0.5;entryX=1;entryY=0.25;'),
        ('ent_admin', 'proc_13', 'Moderate Request', 'exitX=0;exitY=0.15;entryX=1;entryY=0.25;'),
        ('ent_admin', 'proc_14', 'Generate Report', 'exitX=0;exitY=0.45;entryX=1;entryY=0.25;'),
        ('ent_admin', 'proc_15', 'Monitor Logs', 'exitX=0;exitY=0.75;entryX=1;entryY=0.25;')
    ]

    for i, (src, dest, lbl, *geom) in enumerate(flows):
        geom_style = geom[0] if geom else ""
        edge_style = f"edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontSize=11;labelBackgroundColor=#F5F9F5;endArrow=classic;"
        
        flow_cell = ET.SubElement(root, 'mxCell', attrib={
            'id': f"flow_{3000 + i}",
            'edge': '1',
            'parent': '1',
            'source': src,
            'target': dest,
            'style': edge_style + geom_style,
            'value': lbl
        })
        ET.SubElement(flow_cell, 'mxGeometry', attrib={
            'relative': '1',
            'as': 'geometry'
        })

    # Save to drawio files
    xml_str = ET.tostring(mxfile, encoding='utf-8')
    import xml.dom.minidom
    dom = xml.dom.minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ")
    
    dest_path1 = r"d:\porjects\capstone_system\docs\diagrams\dfd\dfd-level-0_v5.drawio"
    with open(dest_path1, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
    print(f"Level-1 Hub-and-Spoke Context DFD V5 saved successfully at: {dest_path1}")
    
    dest_path2 = r"d:\porjects\capstone_system\docs\diagrams\dfd\dfd-level-1-clean_v5.drawio"
    with open(dest_path2, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
    print(f"Level-1 Hub-and-Spoke DFD V5 saved successfully at: {dest_path2}")

if __name__ == "__main__":
    create_dfd_v5()
