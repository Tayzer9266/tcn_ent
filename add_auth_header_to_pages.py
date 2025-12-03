import os
import re

# List of public pages to add the header to
public_pages = [
    "pages/1_Request_Quote_Estimate.py",
    "pages/2_Photographers.py",
    "pages/3_Event_Coordinators.py",
    "pages/4_DJs.py",
    "pages/5_Services.py",
    "pages/6_Questionnaires.py",
    "pages/7_Contact_Us.py",
    "pages/8_Event_Planning_Tips.py"
]

def add_header_to_file(filepath):
    """Add authentication header import and render call to a page file"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if header is already added
        if 'render_auth_header' in content:
            print(f"✓ {filepath} - Header already added, skipping")
            return
        
        # Find the import section
        import_pattern = r'(import streamlit as st\n)'
        
        # Add the header import after streamlit import
        header_import = '''import streamlit as st
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from components.header_auth import render_auth_header
'''
        
        # Replace the streamlit import with our enhanced version
        new_content = re.sub(import_pattern, header_import, content, count=1)
        
        # Find st.set_page_config and add render_auth_header() after it
        config_pattern = r'(st\.set_page_config\([^)]+\))'
        
        def add_render_call(match):
            return match.group(1) + '\n\n# Render authentication header\nrender_auth_header()'
        
        new_content = re.sub(config_pattern, add_render_call, new_content, flags=re.DOTALL)
        
        # Write the updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ {filepath} - Header added successfully")
        
    except Exception as e:
        print(f"❌ {filepath} - Error: {e}")

def main():
    print("=" * 70)
    print("ADDING AUTHENTICATION HEADER TO PUBLIC PAGES")
    print("=" * 70)
    
    for page in public_pages:
        if os.path.exists(page):
            add_header_to_file(page)
        else:
            print(f"⚠️  {page} - File not found")
    
    print("\n" + "=" * 70)
    print("✅ AUTHENTICATION HEADER ADDITION COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
