import streamlit as st

def render_auth_header():
    """
    Renders authentication links horizontally in the top header.
    Shows Login/Register for non-authenticated users, or user info for authenticated users.
    Only displays on the Home page.
    """
    
    # Check authentication status
    is_client_logged_in = st.session_state.get('client_logged_in', False)
    is_professional_logged_in = st.session_state.get('professional_logged_in', False)
    
    # Create a container at the top of the page for authentication
    auth_container = st.container()
    
    with auth_container:
        # Create columns for layout - left spacer, right for auth buttons
        col1, col2, col3 = st.columns([3, 1, 1])
        
        if is_client_logged_in:
            # Client is logged in
            client_name = st.session_state.get('client_data', {}).get('first_name', 'Client')
            with col1:
                st.markdown(f"**👤 Welcome, {client_name}!**")
            with col2:
                if st.button("Dashboard", key="dashboard_btn", use_container_width=True):
                    st.switch_page("pages/93_Client_Dashboard.py")
            with col3:
                if st.button("Logout", key="logout_btn", use_container_width=True):
                    st.session_state.client_logged_in = False
                    st.session_state.client_data = {}
                    st.rerun()
                
        elif is_professional_logged_in:
            # Professional is logged in
            professional_name = st.session_state.get('professional_data', {}).get('name', 'Professional')
            with col1:
                st.markdown(f"**👤 Welcome, {professional_name}!**")
            with col2:
                if st.button("Profile", key="profile_btn", use_container_width=True):
                    st.switch_page("pages/92_Profile_Management.py")
            with col3:
                if st.button("Logout", key="logout_btn_prof", use_container_width=True):
                    st.session_state.professional_logged_in = False
                    st.session_state.professional_data = {}
                    st.rerun()
                
        else:
            # Not logged in - show login and register buttons horizontally
            with col2:
                if st.button("🔑 Login", key="login_btn", type="primary", use_container_width=True):
                    st.switch_page("pages/90_Login.py")
            with col3:
                if st.button("📝 Register", key="register_btn", use_container_width=True):
                    st.switch_page("pages/91_Client_Registration.py")
        
        # Add a divider after the auth section
        st.markdown("---")
