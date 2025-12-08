import streamlit as st

def render_auth_header():
    """
    Renders authentication links and custom navigation in the sidebar.
    Shows Login/Register for non-authenticated users, or user info for authenticated users.
    """
    
    # Check authentication status
    is_client_logged_in = st.session_state.get('client_logged_in', False)
    is_professional_logged_in = st.session_state.get('professional_logged_in', False)
    
    # Add authentication section to sidebar
    with st.sidebar:
        # Custom Navigation Section
        st.markdown("### 📍 Navigation")
        
        # Main pages navigation
        if st.button("🏠 Home", use_container_width=True, key="nav_home"):
            st.switch_page("Home.py")
        
        if st.button("💰 Request Quote", use_container_width=True, key="nav_quote"):
            st.switch_page("pages/1_Request_Quote_Estimate.py")
        
        if st.button("🎵 DJs", use_container_width=True, key="nav_djs"):
            st.switch_page("pages/2_DJs.py")
        
        if st.button("📸 Photographers", use_container_width=True, key="nav_photographers"):
            st.switch_page("pages/3_Photographers.py")
        
        if st.button("🎉 Event Coordinators", use_container_width=True, key="nav_coordinators"):
            st.switch_page("pages/4_Event_Coordinators.py")
        
        if st.button("⚙️ Services", use_container_width=True, key="nav_services"):
            st.switch_page("pages/5_Services.py")
        
        if st.button("📋 Questionnaires", use_container_width=True, key="nav_questionnaires"):
            st.switch_page("pages/6_Questionnaires.py")
        
        if st.button("💡 Event Planning Tips", use_container_width=True, key="nav_tips"):
            st.switch_page("pages/8_Event_Planning_Tips.py")
        
        st.markdown("---")
        
        # Authentication Section
        if is_client_logged_in:
            # Client is logged in
            client_name = st.session_state.get('client_data', {}).get('first_name', 'Client')
            st.markdown(f"### 👤 {client_name}")
            if st.button("🏠 Dashboard", use_container_width=True, key="dashboard_btn"):
                st.switch_page("pages/93_Client_Dashboard.py")
            if st.button("📅 My Events", use_container_width=True, key="my_events_btn"):
                st.switch_page("pages/95_My_Events.py")
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
            if st.button("📊 Quote Requests", use_container_width=True, key="quotes_btn"):
                st.switch_page("pages/97_Professional_Quotes.py")
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
