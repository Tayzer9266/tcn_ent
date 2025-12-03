import streamlit as st
import streamlit.components.v1 as components

def render_auth_header():
    """
    Renders authentication links in a fixed header bar at the very top of the page.
    Shows Login/Register for non-authenticated users, or user info for authenticated users.
    Only displays on the Home page.
    """
    
    # Check authentication status
    is_client_logged_in = st.session_state.get('client_logged_in', False)
    is_professional_logged_in = st.session_state.get('professional_logged_in', False)
    
    # Build the header HTML based on authentication status
    if is_client_logged_in:
        # Client is logged in
        client_name = st.session_state.get('client_data', {}).get('first_name', 'Client')
        auth_buttons = f"""
            <div class="auth-buttons">
                <span class="welcome-text">👤 Welcome, {client_name}!</span>
                <a href="/93_Client_Dashboard" class="auth-btn auth-btn-primary">Dashboard</a>
                <a href="javascript:void(0)" onclick="logout()" class="auth-btn">Logout</a>
            </div>
        """
        
    elif is_professional_logged_in:
        # Professional is logged in
        professional_name = st.session_state.get('professional_data', {}).get('name', 'Professional')
        auth_buttons = f"""
            <div class="auth-buttons">
                <span class="welcome-text">👤 Welcome, {professional_name}!</span>
                <a href="/92_Profile_Management" class="auth-btn auth-btn-primary">Profile</a>
                <a href="javascript:void(0)" onclick="logout()" class="auth-btn">Logout</a>
            </div>
        """
        
    else:
        # Not logged in - show login and register buttons
        auth_buttons = """
            <div class="auth-buttons">
                <a href="/90_Login" class="auth-btn auth-btn-primary">🔑 Login</a>
                <a href="/91_Client_Registration" class="auth-btn auth-btn-register">📝 Register</a>
            </div>
        """
    
    # Inject the fixed header with CSS
    header_html = f"""
    <style>
        /* Fixed header bar at the very top */
        .auth-header-bar {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 50px;
            background: linear-gradient(90deg, #1e1e1e 0%, #2d2d2d 100%);
            z-index: 999999;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding: 0 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }}
        
        /* Push content down to avoid overlap */
        .main .block-container {{
            padding-top: 70px !important;
        }}
        
        /* Auth buttons container */
        .auth-buttons {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}
        
        /* Welcome text */
        .welcome-text {{
            color: #ffffff;
            font-weight: 600;
            font-size: 14px;
            margin-right: 10px;
        }}
        
        /* Auth button styles */
        .auth-btn {{
            color: #ffffff;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            padding: 8px 20px;
            border-radius: 5px;
            transition: all 0.3s;
            border: 2px solid #e63946;
            background: transparent;
            cursor: pointer;
            display: inline-block;
        }}
        
        .auth-btn:hover {{
            background: #e63946;
            color: white;
            text-decoration: none;
            transform: translateY(-1px);
        }}
        
        .auth-btn-primary {{
            background: #e63946;
            color: white;
            border-color: #e63946;
        }}
        
        .auth-btn-primary:hover {{
            background: #d62839;
            border-color: #d62839;
        }}
        
        .auth-btn-register {{
            background: #ffffff;
            color: #e63946;
            border-color: #ffffff;
        }}
        
        .auth-btn-register:hover {{
            background: #e63946;
            color: #ffffff;
            border-color: #e63946;
        }}
    </style>
    
    <div class="auth-header-bar">
        {auth_buttons}
    </div>
    
    <script>
        function logout() {{
            // Send message to Streamlit to handle logout
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                data: {{ action: 'logout' }}
            }}, '*');
            
            // Reload the page
            window.location.reload();
        }}
    </script>
    """
    
    # Render the header using components.html with minimal height
    components.html(header_html, height=0)
