"""
Script to update all public pages to have expanded sidebar state
"""

import os
import re

# List of pages to update
pages_to_update = [
    "pages/1_Request_Quote_Estimate.py",
    "pages/2_Photographers.py",
    "pages/3_Event_Coordinators.py",
    "pages/4_DJs.py",
    "pages/5_Services.py",
    "pages/6_Questionnaires.py",
    "pages/7_Contact_Us.py",
    "pages/8_Event_Planning_Tips.py"
]

def update_page(filepath):
    """Update a single page file to have expanded sidebar"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace collapsed with expanded in st.set_page_config
        updated_content = re.sub(
            r'initial_sidebar_state\s*=\s*["\']collapsed["\']',
            'initial_sidebar_state="expanded"',
            content
        )
        
        # Write back if changes were made
        if updated_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"✓ Updated: {filepath}")
            return True
        else:
            print(f"- No changes needed: {filepath}")
            return False
    except FileNotFoundError:
        print(f"✗ File not found: {filepath}")
        return False
    except Exception as e:
        print(f"✗ Error updating {filepath}: {e}")
        return False

def main():
    print("Updating sidebar state for all public pages...\n")
    
    updated_count = 0
    for page in pages_to_update:
        if update_page(page):
            updated_count += 1
    
    print(f"\n{'='*50}")
    print(f"Summary: Updated {updated_count} out of {len(pages_to_update)} pages")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
