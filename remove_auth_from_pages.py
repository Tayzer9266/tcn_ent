"""
Script to remove auth header calls from all pages except Home.py
"""

import os
import re

# List of pages to update (remove auth header from these)
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

def remove_auth_header(filepath):
    """Remove auth header import and call from a page"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove the import line for header_auth
        content = re.sub(
            r'from components\.header_auth import render_auth_header\n?',
            '',
            content
        )
        
        # Remove the render_auth_header() call and any comment above it
        content = re.sub(
            r'# Render authentication header.*?\n?render_auth_header\(\)\n?',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Also try without comment
        content = re.sub(
            r'render_auth_header\(\)\n?',
            '',
            content
        )
        
        # Write back if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Removed auth header from: {filepath}")
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
    print("Removing auth header from all pages except Home.py...\n")
    
    updated_count = 0
    for page in pages_to_update:
        if remove_auth_header(page):
            updated_count += 1
    
    print(f"\n{'='*50}")
    print(f"Summary: Removed auth header from {updated_count} out of {len(pages_to_update)} pages")
    print(f"Auth header now only appears on Home.py")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
