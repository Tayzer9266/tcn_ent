import streamlit as st

def render_auth_header():
    """
    Renders authentication links in the top right corner of the page.
    Shows Login/Register for non-authenticated users, or user info for authenticated users.
    """
    
    # Custom CSS for the header
    st.markdown("""
        <style>
        .auth-header {
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
        }
        
        .auth-link {
            color: #e63946;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            padding: 8px 16px;
            border-radius: 5px;
            transition: all 0.3s;
            border: 2px solid #e63946;
            background: white;
        }
        
        .auth-link:hover {
            background: #e63946;
            color: white;
            text-decoration: none;
        }
        
        .auth-link-register {
            background: #e63946;
            color: white;
        }
        
        .auth-link-register:hover {
            background: #d62839;
            border-color: #d62839;
        }
        
        .user-info {
            color: #333;
            font-weight: 600;
            font-size: 14px;
            padding: 8px 16px;
        }
        
        .logout-link {
            color: #e63946;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            padding: 8px 16px;
            border-radius: 5px;
            border: 2px solid #e63946;
            background: white;
            cursor: pointer;
        }
        
        .logout-link:hover {
            background: #e63946;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Check authentication status
    is_client_logged_in = st.session_state.get('client_logged_in', False)
    is_professional_logged_in = st.session_state.get('professional_logged_in', False)
    
    if is_client_logged_in:
        # Client is logged in
        client_name = st.session_state.get('client_data', {}).get('first_name', 'Client')
        st.markdown(f"""
            <div class="auth-header">
                <span class="user-info">👤 {client_name}</span>
                <a href="93_Client_Dashboard" target="_self" class="auth-link">Dashboard</a>
            </div>
        """, unsafe_allow_html=True)
        
    elif is_professional_logged_in:
        # Professional is logged in
        professional_name = st.session_state.get('professional_data', {}).get('name', 'Professional')
        st.markdown(f"""
            <div class="auth-header">
                <span class="user-info">👤 {professional_name}</span>
                <a href="92_Profile_Management" target="_self" class="auth-link">Profile</a>
            </div>
        """, unsafe_allow_html=True)
        
    else:
        # Not logged in - show login and register links
        st.markdown("""
            <div class="auth-header">
                <a href="90_Login" target="_self" class="auth-link">Login</a>
                <a href="91_Client_Registration" target="_self" class="auth-link auth-link-register">Register</a>
            </div>
        """, unsafe_allow_html=True)
