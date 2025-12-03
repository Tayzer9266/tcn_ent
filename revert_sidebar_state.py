"""
Script to revert all public pages back to collapsed sidebar state
"""

import os
import re

# List of pages to update
pages_to_update = [
    "pages/1_Request_Quote_Estimate.py",
    "pages/2_Photographers.py",
    "pages/3_Event_Coordinators.py",
    "pages/4_DJs.py"
]

def update_page(filepath):
    """Update a single page file to have collapsed sidebar"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace expanded with collapsed in st.set_page_config
        updated_content = re.sub(
            r'initial_sidebar_state\s*=\s*["\']expanded["\']',
            'initial_sidebar_state="collapsed"',
            content
        )
        
        # Write back if changes were made
        if updated_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"✓ Reverted: {filepath}")
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
    print("Reverting sidebar state to collapsed for all public pages...\n")
    
    updated_count = 0
    for page in pages_to_update:
        if update_page(page):
            updated_count += 1
    
    print(f"\n{'='*50}")
    print(f"Summary: Reverted {updated_count} out of {len(pages_to_update)} pages")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
