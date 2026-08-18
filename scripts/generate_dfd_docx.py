from docx import Document
from docx.oxml import parse_xml
from docx.shared import Pt
from pathlib import Path

# --- Constants & Config ---
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "docs"
OUTPUT_FILE = OUTPUT_DIR / "DFD_Level_1_Recreation.docx"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Colors
COLOR_ENTITY = "BDD7EE"  # Light Blue
COLOR_PROCESS = "FFF2CC" # Light Yellow
COLOR_DATASTORE = "FFFFFF" # White (with side lines)
COLOR_TEXT = "000000"

def create_vml_shape(shape_type, x, y, w, h, text, fill_color="FFFFFF", stroke_weight="1pt", dashed=False):
    """
    Creates a VML shape XML string for Word.
    VML is widely compatible and easy for absolute positioning.
    """
    stroke_style = 'dashstyle="dash"' if dashed else ""
    
    # Escape XML characters and handle newlines for Word
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", '<w:br/>')
    
    xml = f"""
    <w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" 
         xmlns:v="urn:schemas-microsoft-com:vml" 
         xmlns:o="urn:schemas-microsoft-com:office:office">
        <w:pict>
            <v:{shape_type} style="position:absolute;left:{x}pt;top:{y}pt;width:{w}pt;height:{h}pt;z-index:1;visibility:visible"
                fillcolor="#{fill_color}" strokecolor="#000000" strokeweight="{stroke_weight}">
                {f'<v:stroke {stroke_style}/>' if dashed else ''}
                <v:textbox inset="2pt,2pt,2pt,2pt">
                    <w:p>
                        <w:pPr><w:jc w:val="center"/></w:pPr>
                        <w:r><w:rPr><w:sz w:val="18"/><w:b/></w:rPr><w:t>{text}</w:t></w:r>
                    </w:p>
                </v:textbox>
            </v:{shape_type}>
        </w:pict>
    </w:r>
    """
    return xml

def create_vml_line(x1, y1, x2, y2, text="", arrow=True, color="000000"):
    """Creates a VML line XML string."""
    arrow_xml = '<v:stroke endarrow="block"/>' if arrow else ""
    
    xml = f"""
    <w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" 
         xmlns:v="urn:schemas-microsoft-com:vml">
        <w:pict>
            <v:line style="position:absolute;z-index:2" from="{x1}pt,{y1}pt" to="{x2}pt,{y2}pt" strokecolor="#{color}" strokeweight="1pt">
                {arrow_xml}
            </v:line>
        </w:pict>
    </w:r>
    """
    return xml

def create_vml_text(x, y, w, h, text, font_size=16, bold=False, color="000000", align="center"):
    """Adds floating text."""
    # Escape XML characters and handle newlines for Word
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", '<w:br/>')
    
    xml = f"""
    <w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" 
         xmlns:v="urn:schemas-microsoft-com:vml">
        <w:pict>
            <v:rect style="position:absolute;left:{x}pt;top:{y}pt;width:{w}pt;height:{h}pt;z-index:3" stroked="f" filled="f">
                <v:textbox inset="0,0,0,0">
                    <w:p>
                        <w:pPr><w:jc w:val="{align}"/></w:pPr>
                        <w:r>
                            <w:rPr>
                                <w:sz w:val="{font_size}"/>
                                {'<w:b/>' if bold else ''}
                                <w:color w:val="{color}"/>
                            </w:rPr>
                            <w:t>{text}</w:t>
                        </w:r>
                    </w:p>
                </v:textbox>
            </v:rect>
        </w:pict>
    </w:r>
    """
    return xml

def main():
    doc = Document()
    
    # Set page to Landscape for better DFD fitting
    section = doc.sections[-1]
    new_width, new_height = section.page_height, section.page_width
    section.orientation = 1 # WD_ORIENT.LANDSCAPE
    section.page_width = new_width # 11 inches
    section.page_height = new_height # 8.5 inches
    
    # Margin reduction for more space
    section.top_margin = Pt(36)
    section.bottom_margin = Pt(36)
    section.left_margin = Pt(36)
    section.right_margin = Pt(36)

    p = doc.add_paragraph()
    
    # --- 1. Legend / Notation ---
    p._element.append(parse_xml(create_vml_shape("roundrect", 10, 10, 120, 100, "", fill_color="FFFFFF")))
    p._element.append(parse_xml(create_vml_text(15, 15, 110, 20, "BSIT Capstone Notation", font_size=16, bold=True, align="left")))
    p._element.append(parse_xml(create_vml_shape("rect", 15, 40, 55, 20, "External Entity", fill_color=COLOR_ENTITY)))
    p._element.append(parse_xml(create_vml_shape("roundrect", 75, 40, 45, 20, "Process", fill_color=COLOR_PROCESS)))
    p._element.append(parse_xml(create_vml_text(15, 75, 100, 20, "Data Store (DB)", align="left", font_size=14)))
    p._element.append(parse_xml(create_vml_line(12, 72, 12, 92, arrow=False)))
    p._element.append(parse_xml(create_vml_line(65, 72, 65, 92, arrow=False)))

    # --- 2. Top Group (Process 8.0) ---
    p._element.append(parse_xml(create_vml_shape("roundrect", 220, 10, 480, 140, "", dashed=True)))
    p._element.append(parse_xml(create_vml_shape("rect", 240, 50, 60, 50, "Tourist *", fill_color=COLOR_ENTITY)))
    p._element.append(parse_xml(create_vml_shape("roundrect", 380, 50, 80, 60, "8.0 Review &amp; Feedback", fill_color=COLOR_PROCESS)))
    p._element.append(parse_xml(create_vml_text(600, 65, 100, 20, "D7 | REVIEWS *", bold=True)))
    p._element.append(parse_xml(create_vml_line(590, 50, 590, 100, arrow=False)))
    p._element.append(parse_xml(create_vml_line(690, 50, 690, 100, arrow=False)))
    
    p._element.append(parse_xml(create_vml_line(300, 75, 380, 75)))
    p._element.append(parse_xml(create_vml_text(310, 60, 70, 15, "Submit Rating", font_size=14)))
    p._element.append(parse_xml(create_vml_line(380, 95, 270, 95, arrow=False)))
    p._element.append(parse_xml(create_vml_line(270, 95, 270, 100)))
    p._element.append(parse_xml(create_vml_text(300, 100, 80, 15, "Review Posted", font_size=14)))
    p._element.append(parse_xml(create_vml_line(460, 75, 590, 75)))
    p._element.append(parse_xml(create_vml_text(480, 60, 100, 15, "Add Review", font_size=14)))

    # --- 3. Bottom Left (Process 1.0) ---
    p._element.append(parse_xml(create_vml_shape("roundrect", 20, 180, 220, 320, "", dashed=True)))
    p._element.append(parse_xml(create_vml_shape("rect", 40, 220, 80, 60, "Tourist /\nContributor\n/ Admin *", fill_color=COLOR_ENTITY)))
    p._element.append(parse_xml(create_vml_shape("rect", 150, 230, 80, 60, "Google\nOAuth *", fill_color=COLOR_ENTITY)))
    p._element.append(parse_xml(create_vml_shape("roundrect", 100, 380, 100, 80, "1.0 User\nAuthentication", fill_color=COLOR_PROCESS)))
    p._element.append(parse_xml(create_vml_text(110, 520, 130, 20, "D1 | USER ACCOUNTS *", bold=True)))
    p._element.append(parse_xml(create_vml_line(100, 510, 100, 560, arrow=False)))
    p._element.append(parse_xml(create_vml_line(230, 510, 230, 560, arrow=False)))
    
    p._element.append(parse_xml(create_vml_line(90, 280, 110, 380)))
    p._element.append(parse_xml(create_vml_text(60, 310, 70, 15, "Credentials", font_size=14)))
    p._element.append(parse_xml(create_vml_line(130, 380, 110, 280)))
    p._element.append(parse_xml(create_vml_text(125, 305, 70, 15, "Auth Result", font_size=14)))
    p._element.append(parse_xml(create_vml_line(100, 420, 50, 420, arrow=False)))
    p._element.append(parse_xml(create_vml_line(50, 420, 50, 280, color="FF0000")))
    p._element.append(parse_xml(create_vml_text(35, 330, 80, 15, "Invalid Credentials", color="FF0000", font_size=14)))
    
    p._element.append(parse_xml(create_vml_line(190, 290, 170, 380)))
    p._element.append(parse_xml(create_vml_line(170, 380, 190, 290)))
    p._element.append(parse_xml(create_vml_text(180, 325, 60, 15, "OAuth Token", font_size=14)))

    p._element.append(parse_xml(create_vml_line(125, 460, 125, 510)))
    p._element.append(parse_xml(create_vml_text(125, 480, 100, 15, "Verify Credentials", align="left", font_size=14)))
    p._element.append(parse_xml(create_vml_line(160, 510, 160, 460)))
    p._element.append(parse_xml(create_vml_text(50, 480, 100, 15, "Auth Success", align="right", font_size=14)))

    # --- 4. Bottom Center (Process 2.0) ---
    p._element.append(parse_xml(create_vml_shape("roundrect", 260, 220, 260, 280, "", dashed=True)))
    p._element.append(parse_xml(create_vml_shape("rect", 320, 260, 80, 60, "Contributor *", fill_color=COLOR_ENTITY)))
    p._element.append(parse_xml(create_vml_shape("roundrect", 300, 380, 120, 80, "2.0 Content\nManagement", fill_color=COLOR_PROCESS)))
    p._element.append(parse_xml(create_vml_text(420, 260, 100, 20, "D2 | ATTRACTIONS *", bold=True, align="left")))
    p._element.append(parse_xml(create_vml_line(415, 250, 415, 300, arrow=False)))
    p._element.append(parse_xml(create_vml_line(515, 250, 515, 300, arrow=False)))
    p._element.append(parse_xml(create_vml_text(520, 380, 80, 20, "D3 | EVENTS *", bold=True, align="left")))
    p._element.append(parse_xml(create_vml_line(515, 370, 515, 420, arrow=False)))
    p._element.append(parse_xml(create_vml_line(615, 370, 615, 420, arrow=False)))
    p._element.append(parse_xml(create_vml_text(520, 510, 120, 20, "D5 | BARANGAY INFO *", bold=True, align="left")))
    p._element.append(parse_xml(create_vml_line(515, 500, 515, 550, arrow=False)))
    # p._element.append(parse_xml(create_vml_line(645, 500, 645, 550, arrow=False)))

    p._element.append(parse_xml(create_vml_line(350, 320, 350, 380)))
    p._element.append(parse_xml(create_vml_text(280, 335, 100, 15, "Post/Update Content", font_size=14)))
    p._element.append(parse_xml(create_vml_line(390, 385, 430, 300)))
    p._element.append(parse_xml(create_vml_text(410, 340, 70, 15, "Record Data", align="left", font_size=14)))
    p._element.append(parse_xml(create_vml_line(420, 420, 515, 420)))
    p._element.append(parse_xml(create_vml_text(435, 405, 80, 15, "Record Events", align="left", font_size=14)))
    p._element.append(parse_xml(create_vml_line(390, 450, 515, 520)))
    p._element.append(parse_xml(create_vml_text(405, 480, 120, 15, "Submit Info Suggestion", align="left", font_size=14)))

    # --- 5. Bottom Right (Process 3.0) ---
    p._element.append(parse_xml(create_vml_shape("roundrect", 550, 200, 420, 300, "", dashed=True)))
    p._element.append(parse_xml(create_vml_shape("rect", 570, 250, 60, 60, "Tourist *", fill_color=COLOR_ENTITY)))
    p._element.append(parse_xml(create_vml_shape("rect", 850, 250, 80, 60, "Mapbox API *", fill_color=COLOR_ENTITY)))
    p._element.append(parse_xml(create_vml_shape("roundrect", 700, 380, 120, 80, "3.0 Interactive\nMap Display", fill_color=COLOR_PROCESS)))
    p._element.append(parse_xml(create_vml_text(710, 520, 120, 20, "D2 | ATTRACTIONS *", bold=True)))
    p._element.append(parse_xml(create_vml_line(700, 510, 700, 560, arrow=False)))
    p._element.append(parse_xml(create_vml_line(820, 510, 820, 560, arrow=False)))

    p._element.append(parse_xml(create_vml_line(595, 310, 720, 385)))
    p._element.append(parse_xml(create_vml_text(610, 330, 80, 15, "Map Request", font_size=14)))
    p._element.append(parse_xml(create_vml_line(890, 310, 780, 385)))
    p._element.append(parse_xml(create_vml_text(790, 330, 80, 15, "Map Data/Tiles", font_size=14)))
    p._element.append(parse_xml(create_vml_line(760, 460, 760, 510)))
    p._element.append(parse_xml(create_vml_text(765, 480, 80, 15, "Fetch Location", align="left", font_size=14)))

    doc.save(str(OUTPUT_FILE))
    print(f"Document created: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
