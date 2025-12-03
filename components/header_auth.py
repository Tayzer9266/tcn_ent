import streamlit as st

def render_auth_header():
    """
    Renders authentication links in the sidebar.
    Shows Login/Register for non-authenticated users, or user info for authenticated users.
    """
    
    # Check authentication status
    is_client_logged_in = st.session_state.get('client_logged_in', False)
    is_professional_logged_in = st.session_state.get('professional_logged_in', False)
    
    # Add authentication section to sidebar
    with st.sidebar:
        st.markdown("---")
        
        if is_client_logged_in:
            # Client is logged in
            client_name = st.session_state.get('client_data', {}).get('first_name', 'Client')
            st.markdown(f"### 👤 {client_name}")
            if st.button("🏠 Dashboard", use_container_width=True, key="dashboard_btn"):
                st.switch_page("pages/93_Client_Dashboard.py")
            if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
                st.session_state.client_logged_in = False
                st.session_state.client_data = {}
                st.rerun()
                
        elif is_professional_logged_in:
            # Professional is logged in
            professional_name = st.session_state.get('professional_data', {}).get('name', 'Professional')
            st.markdown(f"### 👤 {professional_name}")
            if st.button("👤 Profile", use_container_width=True, key="profile_btn"):
                st.switch_page("pages/92_Profile_Management.py")
            if st.button("🚪 Logout", use_container_width=True, key="logout_btn_prof"):
                st.session_state.professional_logged_in = False
                st.session_state.professional_data = {}
                st.rerun()
                
        else:
            # Not logged in - show login and register buttons
            st.markdown("### 🔐 Account")
            if st.button("🔑 Login", use_container_width=True, key="login_btn", type="primary"):
                st.switch_page("pages/90_Login.py")
            if st.button("📝 Register", use_container_width=True, key="register_btn"):
                st.switch_page("pages/91_Client_Registration.py")
        
        st.markdown("---")
