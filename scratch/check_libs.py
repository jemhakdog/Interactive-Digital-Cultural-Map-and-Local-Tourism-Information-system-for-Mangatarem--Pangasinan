import sys

try:
    import pypdf
    print("pypdf is available")
except ImportError:
    print("pypdf is NOT available")

try:
    import pdfplumber
    print("pdfplumber is available")
except ImportError:
    print("pdfplumber is NOT available")

try:
    import docx
    print("python-docx is available")
except ImportError:
    print("python-docx is NOT available")
