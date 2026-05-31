import xml.etree.ElementTree as ET
import os

def create_dfd_v4_3():
    print("Initializing Draw.io Level-1 DFD V4.3 generator with localized Datastores Col 3 & Col 3.5...")
    
    # Create the root structures
    mxfile = ET.Element('mxfile', attrib={'host': 'Electron'})
    diagram = ET.SubElement(mxfile, 'diagram', attrib={'name': 'Chronological DFD V4.3', 'id': 'DFD_V4_3'})
    mxGraphModel = ET.SubElement(diagram, 'mxGraphModel', attrib={
        'dx': '3000', 'dy': '2500', 'grid': '1', 'gridSize': '10',
        'guides': '1', 'tooltips': '1', 'connect': '1', 'arrows': '1',
        'fold': '1', 'page': '1', 'pageScale': '1', 'pageWidth': '2400',
        'pageHeight': '2200', 'background': '#F5F9F5', 'math': '0', 'shadow': '0'
    })
    root = ET.SubElement(mxGraphModel, 'root')
    
    # Draw.io default layer cells
    ET.SubElement(root, 'mxCell', attrib={'id': '0'})
    ET.SubElement(root, 'mxCell', attrib={'id': '1', 'parent': '0'})
    
    # Common dimensions
    entity_w, entity_h = 130, 400
    proc_w, proc_h = 180, 80
    store_w, store_h = 160, 45
    
    # External Entities
    entities = {
        'TOURIST': {'id': 'ent_tourist', 'x': 50, 'y': 150, 'w': 130, 'h': 400, 'color': '#BDD7EE'},
        'TOURIST_2': {'id': 'ent_tourist_2', 'x': 50, 'y': 800, 'w': 130, 'h': 400, 'color': '#BDD7EE'},
        'TOURIST_3': {'id': 'ent_tourist_3', 'x': 50, 'y': 1250, 'w': 130, 'h': 240, 'color': '#BDD7EE'},
        'BUSINESS_OWNER': {'id': 'ent_business', 'x': 1350, 'y': 380, 'w': 130, 'h': 110, 'color': '#FFE6CC'},
        'HERITAGE_GUARDIAN': {'id': 'ent_guardian', 'x': 1350, 'y': 250, 'w': 130, 'h': 110, 'color': '#D5E8D4'},
        'ADMIN': {'id': 'ent_admin', 'x': 2150, 'y': 150, 'w': 130, 'h': 1400, 'color': '#C5E1A5'}
    }
    
    # Helper APIs (External Interfaces)
    apis = {
        'api_google': {'id': 'api_g', 'name': 'Google OAuth API', 'x': 450, 'y': 40, 'w': 180, 'h': 40},
        'api_mapbox': {'id': 'api_m', 'name': 'Mapbox Directions API', 'x': 450, 'y': 250, 'w': 180, 'h': 40}
    }

    # Processes
    processes = {
        # Col 2: Public/User-Facing Journey (1.0 - 8.0)
        'p1': {'id': 'proc_1', 'num': '1.0', 'name': 'User Onboarding\n& Authentication', 'x': 450, 'y': 150, 'col': 2},
        'p2': {'id': 'proc_2', 'num': '2.0', 'name': 'Interactive Map\nExploration', 'x': 450, 'y': 330, 'col': 2},
        'p3': {'id': 'proc_3', 'num': '3.0', 'name': 'Heritage Catalog\nDiscovery', 'x': 450, 'y': 510, 'col': 2},
        'p4': {'id': 'proc_4', 'num': '4.0', 'name': 'Review &\nFeedback Management', 'x': 450, 'y': 690, 'col': 2},
        'p5': {'id': 'proc_5', 'num': '5.0', 'name': 'Favorite Spotlight\nManagement', 'x': 450, 'y': 870, 'col': 2},
        'p6': {'id': 'proc_6', 'num': '6.0', 'name': 'Booking &\nReservations Network', 'x': 450, 'y': 1050, 'col': 2},
        'p7': {'id': 'proc_7', 'num': '7.0', 'name': 'Chat Messaging\nNetwork', 'x': 450, 'y': 1230, 'col': 2},
        'p8': {'id': 'proc_8', 'num': '8.0', 'name': 'Newsletter\nSubscription', 'x': 450, 'y': 1410, 'col': 2},
        
        # Col 4: Contributor & Admin Journey (9.0 - 15.0)
        'p9': {'id': 'proc_9', 'num': '9.0', 'name': 'Attraction Content\nManagement', 'x': 1650, 'y': 150, 'col': 4},
        'p10': {'id': 'proc_10', 'num': '10.0', 'name': 'Heritage Form\nSubmissions', 'x': 1650, 'y': 330, 'col': 4},
        'p11': {'id': 'proc_11', 'num': '11.0', 'name': 'Establishment\nListing Management', 'x': 1650, 'y': 510, 'col': 4},
        'p12': {'id': 'proc_12', 'num': '12.0', 'name': 'Media Gallery\nManagement', 'x': 1650, 'y': 690, 'col': 4},
        'p13': {'id': 'proc_13', 'num': '13.0', 'name': 'Content Verification\n& Approval', 'x': 1650, 'y': 870, 'col': 4},
        'p14': {'id': 'proc_14', 'num': '14.0', 'name': 'Analytics &\nReporting Engine', 'x': 1650, 'y': 1050, 'col': 4},
        'p15': {'id': 'proc_15', 'num': '15.0', 'name': 'Audit Logging &\nSecurity Registry', 'x': 1650, 'y': 1230, 'col': 4}
    }

    # Separated Datastores Col 3 (X:1050) & Col 3.5 (X:1350)
    # This prevents lines from having to cross vertically!
    datastores = {
        # --- Column 3: Datastores used primarily by Col 2 (User Processes) ---
        'db_user': {'id': 'db_1', 'num': 'D1', 'name': 'User_db', 'x': 1050, 'y': 150},
        'db_attr': {'id': 'db_2', 'num': 'D2', 'name': 'Attraction_db', 'x': 1050, 'y': 240},
        'db_event': {'id': 'db_3', 'num': 'D3', 'name': 'Event_db', 'x': 1050, 'y': 330},
        'db_brgy': {'id': 'db_4', 'num': 'D4', 'name': 'Barangay_db', 'x': 1050, 'y': 420},
        'db_rev': {'id': 'db_5', 'num': 'D5', 'name': 'Review_db', 'x': 1050, 'y': 690}, # Realigned vertically to align with reviews (P4.0)
        'db_fav': {'id': 'db_6', 'num': 'D6', 'name': 'Favorite_db', 'x': 1050, 'y': 870}, # Realigned to P5.0 favorite spotlight
        'db_book': {'id': 'db_7', 'num': 'D7', 'name': 'Booking_db', 'x': 1050, 'y': 1050}, # Realigned to P6.0
        'db_chat': {'id': 'db_8', 'num': 'D8', 'name': 'Chat_db', 'x': 1050, 'y': 1230}, # Realigned to P7.0
        'db_news': {'id': 'db_9', 'num': 'D9', 'name': 'Newsletter_db', 'x': 1050, 'y': 1410}, # Realigned to P8.0
        'db_mapfeed': {'id': 'db_14', 'num': 'D14', 'name': 'Map_Feedback_db', 'x': 1050, 'y': 780},
        
        # --- Column 3.5: Datastores used primarily by Col 4 (Admin / Contributor Processes) ---
        'db_est': {'id': 'db_10', 'num': 'D10', 'name': 'Establishment_db', 'x': 1350, 'y': 510}, # Aligned to listing P11
        'db_gal': {'id': 'db_11', 'num': 'D11', 'name': 'Gallery_db', 'x': 1350, 'y': 690}, # Aligned to gallery P12
        'db_verify': {'id': 'db_15', 'num': 'D15', 'name': 'Business_Verification_db', 'x': 1350, 'y': 870}, # Aligned to P13
        'db_vlog': {'id': 'db_12', 'num': 'D12', 'name': 'Visitor_Log_db', 'x': 1350, 'y': 1050}, # Aligned to P14
        'db_alog': {'id': 'db_13', 'num': 'D13', 'name': 'Audit_Log_db', 'x': 1350, 'y': 1230}, # Aligned to P15
        'db_notif': {'id': 'db_16', 'num': 'D16', 'name': 'Notification_db', 'x': 1350, 'y': 1140},
        
        # Local Duplicated Datastore nodes for zero crossover routing lines!
        'db_attr_dup': {'id': 'db_2_dup', 'num': 'D2', 'name': 'Attraction_db (Copy)', 'x': 1350, 'y': 150},
        'db_event_dup': {'id': 'db_3_dup', 'num': 'D3', 'name': 'Event_db (Copy)', 'x': 1350, 'y': 70},
        'db_fav_dup': {'id': 'db_6_dup', 'num': 'D6', 'name': 'Favorite_db (Copy)', 'x': 1350, 'y': 960}
    }

    # Render Entities
    for key, info in entities.items():
        entity_cell = ET.SubElement(root, 'mxCell', attrib={
            'id': info['id'],
            'parent': '1',
            'style': f'rounded=0;whiteSpace=wrap;html=1;fillColor={info["color"]};strokeColor=#000000;fontStyle=1;fontColor=#000000;fontSize=13;horizontal=0;strokeWidth=2;',
            'value': key.split('_')[0],
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

    # Render Processes (Level-1 Double Rounded Style)
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

    # Render Datastores
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

    # Render Connections with perfect local routing (no long crossover lines!)
    flows = [
        # --- USER ONBOARDING & AUTH (1.0) ---
        ('ent_tourist', 'proc_1', 'Credentials', 'exitX=1;exitY=0.08;entryX=0;entryY=0.25;'),
        ('proc_1', 'api_g', 'OAuth Handshake', 'exitX=0.5;exitY=0;entryX=0.5;entryY=1;'),
        ('proc_1', 'db_1', 'User Accounts', 'exitX=1;exitY=0.5;entryX=0;entryY=0.5;'),
        ('proc_1', 'ent_tourist', 'Access Token', 'exitX=0;exitY=0.75;entryX=1;entryY=0.15;'),
        
        # --- MAP EXPLORATION (2.0) ---
        ('ent_tourist', 'proc_2', 'Search Locality', 'exitX=1;exitY=0.22;entryX=0;entryY=0.25;'),
        ('proc_2', 'api_m', 'Get Routing Tiles', 'exitX=0.5;exitY=0;entryX=0.5;entryY=1;'),
        ('db_2', 'proc_2', 'Map Highlights', 'exitX=0;exitY=0.5;entryX=1;entryY=0.25;'),
        ('db_4', 'proc_2', 'Barangay Spatial Data', 'exitX=0;exitY=0.5;entryX=1;entryY=0.5;'),
        ('proc_2', 'ent_tourist', 'Interactive Map', 'exitX=0;exitY=0.75;entryX=1;entryY=0.28;'),

        # --- HERITAGE DISCOVERY (3.0) ---
        ('ent_tourist', 'proc_3', 'Browse Categories', 'exitX=1;exitY=0.35;entryX=0;entryY=0.25;'),
        ('db_3', 'proc_3', 'Event Schedule', 'exitX=0;exitY=0.5;entryX=1;entryY=0.25;'),
        ('db_2', 'proc_3', 'Heritage Details', 'exitX=0;exitY=0.5;entryX=1;entryY=0.5;'),
        ('proc_3', 'ent_tourist', 'Cultural Content Feed', 'exitX=0;exitY=0.75;entryX=1;entryY=0.38;'),

        # --- REVIEW & FEEDBACK (4.0) ---
        ('ent_tourist_2', 'proc_4', 'Submit Review', 'exitX=1;exitY=0.08;entryX=0;entryY=0.25;'),
        ('proc_4', 'db_5', 'Post Review Content', 'exitX=1;exitY=0.5;entryX=0;entryY=0.5;'),
        ('proc_4', 'db_14', 'Map Feedback Logs', 'exitX=1;exitY=0.75;entryX=0;entryY=0.5;'),
        ('proc_4', 'ent_tourist_2', 'Action Status', 'exitX=0;exitY=0.75;entryX=1;entryY=0.15;'),

        # --- FAVORITE SPOTLIGHT (5.0) ---
        ('ent_tourist_2', 'proc_5', 'Toggle Bookmark', 'exitX=1;exitY=0.35;entryX=0;entryY=0.25;'),
        ('proc_5', 'db_6', 'Persist Favorites', 'exitX=1;exitY=0.5;entryX=0;entryY=0.5;'),
        ('proc_5', 'ent_tourist_2', 'Spotlight Feed', 'exitX=0;exitY=0.75;entryX=1;entryY=0.45;'),

        # --- BOOKING & RESERVATIONS (6.0) ---
        ('ent_tourist_2', 'proc_6', 'Reserve Slot', 'exitX=1;exitY=0.62;entryX=0;entryY=0.25;'),
        ('proc_6', 'db_7', 'Booking Details', 'exitX=1;exitY=0.5;entryX=0;entryY=0.5;'),
        ('proc_6', 'db_16', 'Notification Request', 'exitX=1;exitY=0.75;entryX=0;entryY=0.5;'),
        ('proc_6', 'ent_tourist_2', 'Booking Confirmed', 'exitX=0;exitY=0.75;entryX=1;entryY=0.75;'),

        # --- CHAT messaging (7.0) ---
        ('ent_tourist_3', 'proc_7', 'Message Input', 'exitX=1;exitY=0.15;entryX=0;entryY=0.25;'),
        ('proc_7', 'db_8', 'Direct Message', 'exitX=1;exitY=0.5;entryX=0;entryY=0.5;'),
        ('proc_7', 'ent_tourist_3', 'Message Receipt', 'exitX=0;exitY=0.75;entryX=1;entryY=0.38;'),

        # --- NEWSLETTER (8.0) ---
        ('ent_tourist_3', 'proc_8', 'Subscribe Email', 'exitX=1;exitY=0.68;entryX=0;entryY=0.25;'),
        ('proc_8', 'db_9', 'Add Subscriber', 'exitX=1;exitY=0.5;entryX=0;entryY=0.5;'),
        ('proc_8', 'ent_tourist_3', 'Verification Link', 'exitX=0;exitY=0.75;entryX=1;entryY=0.88;'),

        # --- ATTRACTION CONTENT MANAGEMENT (9.0) ---
        ('ent_guardian', 'proc_9', 'Asset Registry', 'exitX=1;exitY=0.15;entryX=0;entryY=0.25;'),
        ('proc_9', 'db_2_dup', 'Register Attraction', 'exitX=0;exitY=0.5;entryX=1;entryY=0.5;'),
        ('proc_9', 'db_3_dup', 'Register Event', 'exitX=0;exitY=0.75;entryX=1;entryY=0.5;'),
        ('proc_9', 'ent_guardian', 'Registry Status', 'exitX=0;exitY=0.75;entryX=1;entryY=0.45;'),

        # --- HERITAGE SUBMISSIONS (10.0) ---
        ('ent_guardian', 'proc_10', 'Heritage Form (01-07)', 'exitX=1;exitY=0.78;entryX=0;entryY=0.25;'),
        ('proc_10', 'db_2_dup', 'Forms Registry Data', 'exitX=0;exitY=0.5;entryX=1;entryY=0.5;'),
        ('proc_10', 'ent_guardian', 'Submission Status', 'exitX=0;exitY=0.75;entryX=1;entryY=0.85;'),

        # --- ESTABLISHMENT LISTING (11.0) ---
        ('ent_business', 'proc_11', 'Listing Details / Permit', 'exitX=1;exitY=0.25;entryX=0;entryY=0.25;'),
        ('proc_11', 'db_10', 'Establishment Records', 'exitX=0;exitY=0.5;entryX=1;entryY=0.5;'),
        ('proc_11', 'db_15', 'Verification Logs', 'exitX=0;exitY=0.75;entryX=1;entryY=0.5;'),
        ('proc_11', 'ent_business', 'Verification Pending', 'exitX=0;exitY=0.75;entryX=1;entryY=0.75;'),

        # --- MEDIA GALLERY (12.0) ---
        ('proc_12', 'db_11', 'Save Media Record', 'exitX=0;exitY=0.5;entryX=1;entryY=0.5;'),

        # --- CONTENT VERIFICATION & APPROVAL (13.0) ---
        ('ent_admin', 'proc_13', 'Screen Request', 'exitX=0;exitY=0.25;entryX=1;entryY=0.25;'),
        ('db_15', 'proc_13', 'Verification Data', 'exitX=1;exitY=0.5;entryX=0;entryY=0.5;'),
        ('proc_13', 'db_2_dup', 'Approve Content', 'exitX=0;exitY=0.5;entryX=1;entryY=0.5;'),
        ('proc_13', 'ent_admin', 'Approval Results', 'exitX=1;exitY=0.75;entryX=0;entryY=0.32;'),

        # --- ANALYTICS & REPORTING ENGINE (14.0) ---
        ('ent_admin', 'proc_14', 'Generate Report Request', 'exitX=0;exitY=0.48;entryX=1;entryY=0.25;'),
        ('db_12', 'proc_14', 'Visitor Metrics', 'exitX=1;exitY=0.5;entryX=0;entryY=0.5;'),
        ('db_6_dup', 'proc_14', 'Engagement Logs', 'exitX=1;exitY=0.5;entryX=0;entryY=0.75;'),
        ('proc_14', 'ent_admin', 'Analytics Dashboard', 'exitX=1;exitY=0.75;entryX=0;entryY=0.52;'),

        # --- AUDIT LOGGING & SECURITY (15.0) ---
        ('proc_15', 'db_13', 'Log Audit Summary', 'exitX=0;exitY=0.5;entryX=1;entryY=0.5;'),
        ('proc_15', 'db_12', 'Log Page Metrics', 'exitX=0;exitY=0.75;entryX=1;entryY=0.5;'),
        ('ent_admin', 'proc_15', 'Audit View Request', 'exitX=0;exitY=0.68;entryX=1;entryY=0.25;'),
        ('proc_15', 'ent_admin', 'System Activity Logs', 'exitX=1;exitY=0.75;entryX=0;entryY=0.72;')
    ]

    for i, (src, dest, lbl, *geom) in enumerate(flows):
        geom_style = geom[0] if geom else ""
        edge_style = f"edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#000000;strokeWidth=2;fontColor=#000000;fontSize=11;labelBackgroundColor=#F5F9F5;endArrow=classic;"
        
        flow_cell = ET.SubElement(root, 'mxCell', attrib={
            'id': f"flow_{1000 + i}",
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

    # Save to drawio file
    xml_str = ET.tostring(mxfile, encoding='utf-8')
    import xml.dom.minidom
    dom = xml.dom.minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ")
    
    dest_path = r"d:\porjects\capstone_system\docs\diagrams\dfd\dfd-level-1-clean_v4.drawio"
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
        
    print(f"Data Flow Diagram Level-1 V4.3 saved successfully at: {dest_path}")

if __name__ == "__main__":
    create_dfd_v4_3()
