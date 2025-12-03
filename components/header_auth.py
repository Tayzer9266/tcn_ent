import streamlit as st

def render_auth_header():
    """
    Renders authentication links in the top right corner of the page.
    Shows Login/Register for non-authenticated users, or user info for authenticated users.
    """
    
    # Custom CSS for the header
    st.markdown("""
        <style>
        .auth-header-container {
            position: fixed;
            top: 0;
            right: 0;
            z-index: 999999;
            background: rgba(255, 255, 255, 0.95);
            padding: 10px 20px;
            border-bottom-left-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .user-info-text {
            color: #333;
            font-weight: 600;
            font-size: 14px;
            display: inline-block;
            margin-right: 10px;
        }
        
        /* Hide streamlit button styling in header */
        .auth-header-container .stButton button {
            background: white;
            color: #e63946;
            border: 2px solid #e63946;
            border-radius: 5px;
            padding: 8px 16px;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.3s;
            margin: 0 5px;
        }
        
        .auth-header-container .stButton button:hover {
            background: #e63946;
            color: white;
            border-color: #e63946;
        }
        
        /* Special styling for register button */
        .auth-header-container .stButton:nth-child(2) button {
            background: #e63946;
            color: white;
        }
        
        .auth-header-container .stButton:nth-child(2) button:hover {
            background: #d62839;
            border-color: #d62839;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Check authentication status
    is_client_logged_in = st.session_state.get('client_logged_in', False)
    is_professional_logged_in = st.session_state.get('professional_logged_in', False)
    
    # Create a container for the header
    st.markdown('<div class="auth-header-container">', unsafe_allow_html=True)
    
    if is_client_logged_in:
        # Client is logged in
        client_name = st.session_state.get('client_data', {}).get('first_name', 'Client')
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f'<span class="user-info-text">👤 {client_name}</span>', unsafe_allow_html=True)
        with col2:
            if st.button("Dashboard", key="header_dashboard"):
                st.switch_page("pages/93_Client_Dashboard.py")
        
    elif is_professional_logged_in:
        # Professional is logged in
        professional_name = st.session_state.get('professional_data', {}).get('name', 'Professional')
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f'<span class="user-info-text">👤 {professional_name}</span>', unsafe_allow_html=True)
        with col2:
            if st.button("Profile", key="header_profile"):
                st.switch_page("pages/92_Profile_Management.py")
        
    else:
        # Not logged in - show login and register buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", key="header_login"):
                st.switch_page("pages/90_Login.py")
        with col2:
            if st.button("Register", key="header_register"):
                st.switch_page("pages/91_Client_Registration.py")
    
    st.markdown('</div>', unsafe_allow_html=True)
