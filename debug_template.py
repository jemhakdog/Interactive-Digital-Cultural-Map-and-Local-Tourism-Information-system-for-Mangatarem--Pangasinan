from flask import Flask, render_template
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from app import app, db, User, Attraction
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def debug_render():
    with app.app_context():
        try:
            print("--- Rendering map.html ---")
            # Mock data for map.html
            render_template('map.html', barangays=['Poblacion'])
            print("SUCCESS: map.html rendered")
        except Exception as e:
            print(f"ERROR in map.html: {e}")
            import traceback
            traceback.print_exc()

        print("\n")

        try:
            print("--- Rendering barangay_profile.html ---")
            # Mock data for barangay_profile.html
            render_template('barangay_profile.html', 
                          barangay_name='Poblacion', 
                          attractions=[], 
                          events=[], 
                          gallery_items=[], 
                          barangay_info=None)
            print("SUCCESS: barangay_profile.html rendered")
        except Exception as e:
            print(f"ERROR in barangay_profile.html: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    debug_render()
