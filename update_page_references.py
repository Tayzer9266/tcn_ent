"""
Update all references to renamed pages throughout the codebase
"""
import os
import re

# Mapping of old page names to new page names
page_mappings = {
    'pages/1_Login.py': 'pages/90_Login.py',
    'pages/2_Client_Registration.py': 'pages/91_Client_Registration.py',
    'pages/13_Profile_Management.py': 'pages/92_Profile_Management.py',
    'pages/14_Client_Dashboard.py': 'pages/93_Client_Dashboard.py',
    'pages/15_Request_Quote.py': 'pages/94_Request_Quote.py',
    'pages/16_My_Events.py': 'pages/95_My_Events.py',
    'pages/17_Event_Chat.py': 'pages/96_Event_Chat.py',
    'pages/18_Professional_Quotes.py': 'pages/97_Professional_Quotes.py',
}

def update_file(filepath):
    """Update page references in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update all page references
        for old_page, new_page in page_mappings.items():
            # Update st.switch_page() calls
            content = content.replace(f'st.switch_page("{old_page}")', f'st.switch_page("{new_page}")')
            content = content.replace(f"st.switch_page('{old_page}')", f"st.switch_page('{new_page}')")
        
        # Only write if content changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

# Files to update
files_to_check = [
    'Home.py',
    'auth_utils.py',
    'client_manager.py',
]

# Add all Python files in pages directory
pages_dir = 'pages'
for filename in os.listdir(pages_dir):
    if filename.endswith('.py'):
        files_to_check.append(os.path.join(pages_dir, filename))

print("=" * 70)
print("UPDATING PAGE REFERENCES")
print("=" * 70)

updated_count = 0
for filepath in files_to_check:
    if os.path.exists(filepath):
        if update_file(filepath):
            print(f"✅ Updated: {filepath}")
            updated_count += 1
        else:
            print(f"⏭️  No changes: {filepath}")
    else:
        print(f"⚠️  Not found: {filepath}")

print("=" * 70)
print(f"✅ Updated {updated_count} files")
print("=" * 70)
