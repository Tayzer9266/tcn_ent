import streamlit as st
import streamlit.components.v1 as components

def render_auth_header():
    """
    Renders authentication links in the top right corner of the page.
    Shows Login/Register for non-authenticated users, or user info for authenticated users.
    """
    
    # Check authentication status
    is_client_logged_in = st.session_state.get('client_logged_in', False)
    is_professional_logged_in = st.session_state.get('professional_logged_in', False)
    
    # Build the header HTML based on authentication status
    if is_client_logged_in:
        # Client is logged in
        client_name = st.session_state.get('client_data', {}).get('first_name', 'Client')
        header_html = f"""
        <div class="auth-header">
            <span class="user-info">👤 {client_name}</span>
            <a href="?page=93_Client_Dashboard" class="auth-link">Dashboard</a>
        </div>
        """
        
    elif is_professional_logged_in:
        # Professional is logged in
        professional_name = st.session_state.get('professional_data', {}).get('name', 'Professional')
        header_html = f"""
        <div class="auth-header">
            <span class="user-info">👤 {professional_name}</span>
            <a href="?page=92_Profile_Management" class="auth-link">Profile</a>
        </div>
        """
        
    else:
        # Not logged in - show login and register links
        header_html = """
        <div class="auth-header">
            <a href="?page=90_Login" class="auth-link">Login</a>
            <a href="?page=91_Client_Registration" class="auth-link auth-link-register">Register</a>
        </div>
        """
    
    # Inject the header with CSS and JavaScript for navigation
    full_html = f"""
    <style>
        .auth-header {{
            position: fixed;
            top: 0;
            right: 0;
            z-index: 999999;
            background: rgba(255, 255, 255, 0.95);
            padding: 10px 20px;
            border-bottom-left-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            display: flex;
            gap: 15px;
            align-items: center;
        }}
        
        .auth-link {{
            color: #e63946;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            padding: 8px 16px;
            border-radius: 5px;
            transition: all 0.3s;
            border: 2px solid #e63946;
            background: white;
            cursor: pointer;
        }}
        
        .auth-link:hover {{
            background: #e63946;
            color: white;
            text-decoration: none;
        }}
        
        .auth-link-register {{
            background: #e63946;
            color: white;
        }}
        
        .auth-link-register:hover {{
            background: #d62839;
            border-color: #d62839;
        }}
        
        .user-info {{
            color: #333;
            font-weight: 600;
            font-size: 14px;
            padding: 8px 16px;
        }}
    </style>
    
    {header_html}
    
    <script>
        // Handle navigation clicks
        document.querySelectorAll('.auth-link').forEach(link => {{
            link.addEventListener('click', function(e) {{
                e.preventDefault();
                const url = new URL(this.href);
                const page = url.searchParams.get('page');
                if (page) {{
                    // Use Streamlit's navigation
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        data: {{ page: page }}
                    }}, '*');
                    
                    // Fallback: try direct navigation
                    window.location.href = '/' + page;
                }}
            }});
        }});
    </script>
    """
    
    # Render the header using components.html with proper height for visibility
    components.html(full_html, height=60)
