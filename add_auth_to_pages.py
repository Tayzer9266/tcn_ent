"""
Script to add authentication checks to client and professional pages
"""

# Pages to update with their authentication requirements
pages_to_update = {
    # Client pages
    'pages/16_My_Events.py': 'client',
    'pages/17_Event_Chat.py': 'client',
    # Professional pages  
    'pages/18_Professional_Quotes.py': 'professional',
    'pages/13_Profile_Management.py': 'professional'
}

for page_path, auth_type in pages_to_update.items():
    try:
        # Read the file
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has auth
        if 'require_client_auth' in content or 'require_professional_auth' in content:
            print(f"✅ {page_path} already has authentication")
            continue
        
        # Find the imports section
        if auth_type == 'client':
            auth_import = "from auth_utils import require_client_auth"
            auth_call = "\n# Require client authentication\nrequire_client_auth()\n"
        else:
            auth_import = "from auth_utils import require_professional_auth"
            auth_call = "\n# Require professional authentication\nrequire_professional_auth()\n"
        
        # Add import after other imports
        if 'from client_manager import client_manager' in content:
            content = content.replace(
                'from client_manager import client_manager',
                f'from client_manager import client_manager\n{auth_import}'
            )
        elif 'from profiles_data import profile_manager' in content:
            content = content.replace(
                'from profiles_data import profile_manager',
                f'from profiles_data import profile_manager\n{auth_import}'
            )
        
        # Add auth call before st.set_page_config
        content = content.replace(
            '\n# Page configuration\nst.set_page_config(',
            f'{auth_call}\n# Page configuration\nst.set_page_config('
        )
        
        # If no "# Page configuration" comment, add before st.set_page_config
        if auth_call not in content:
            content = content.replace(
                '\nst.set_page_config(',
                f'{auth_call}\nst.set_page_config('
            )
        
        # Write back
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {page_path} with {auth_type} authentication")
        
    except Exception as e:
        print(f"❌ Error updating {page_path}: {e}")

print("\n✅ All pages updated!")
