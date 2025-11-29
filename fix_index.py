"""
Apply performance optimizations to index.html
This script applies lazy loading and defer attributes to scripts
"""

def apply_fixes():
    filepath = r"c:\Users\jem\Desktop\Interactive Digital Cultural Map and Local Tourism Information system for Mangatarem, Pangasinan\templates\index.html"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Add lazy loading to church image
    content = content.replace(
        '<img src="https://mangatarem.gov.ph/wp-content/uploads/2022/06/423528622_849734160503800_3042916681464663887_n.jpg"\r\n                    alt="St. Raymond de Penafort Church" />',
        '<img src="https://mangatarem.gov.ph/wp-content/uploads/2022/06/423528622_849734160503800_3042916681464663887_n.jpg"\r\n                    alt="St. Raymond de Penafort Church"\r\n                    loading="lazy"\r\n                    width="600"\r\n                    height="350" />'
    )
    
    # Fix 2: Add lazy loading to spring image
    content = content.replace(
        '<img src="https://mangatarem.gov.ph/wp-content/uploads/2022/06/manleluag-spring.jpg"\r\n                    alt="Manleluag Spring National Park" />',
        '<img src="https://mangatarem.gov.ph/wp-content/uploads/2022/06/manleluag-spring.jpg"\r\n                    alt="Manleluag Spring National Park"\r\n                    loading="lazy"\r\n                    width="600"\r\n                    height="350" />'
    )
    
    # Fix 3: Add lazy loading to map preview image
    content = content.replace(
        '<img src="https://via.placeholder.com/600x400/047857/ffffff?text=Interactive+Map+Preview"\r\n                    alt="Map Preview" />',
        '<img src="https://via.placeholder.com/600x400/047857/ffffff?text=Interactive+Map+Preview"\r\n                    alt="Map Preview"\r\n                    loading="lazy"\r\n                    width="600"\r\n                    height="400" />'
    )
    
    # Fix 4: Defer AOS script and switch to animations-optimized.js
    content = content.replace(
        '<!-- Scripts -->\r\n<script src="https://unpkg.com/aos@next/dist/aos.js"></script>\r\n<script src="{{ url_for(\'static\', filename=\'js/animations.js\') }}"></script>',
        '<!-- Scripts - Deferred for Performance -->\r\n<script src="https://unpkg.com/aos@next/dist/aos.js" defer></script>\r\n<script src="{{ url_for(\'static\', filename=\'js/animations-optimized.js\') }}" defer></script>'
    )
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Successfully applied all performance optimizations to index.html")
    print("  - Added lazy loading to 3 images")
    print("  - Added defer attribute to scripts")
    print("  - Switched to animations-optimized.js")

if __name__ == "__main__":
    apply_fixes()
