import sys

# Add the project directory to sys.path
sys.path.append('d:\\porjects\\Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan')

from app import create_app

app = create_app()
with app.app_context():
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")
