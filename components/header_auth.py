import streamlit as st
from streamlit_navigation_bar import st_navbar

def render_navigation_bar():
    """
    Renders a navigation bar at the top of the page with grouped professional categories.
    Includes Login/Register buttons based on authentication status.
    """
    
    # Check authentication status
    is_client_logged_in = st.session_state.get('client_logged_in', False)
    is_professional_logged_in = st.session_state.get('professional_logged_in', False)
    
    # Define navigation pages
    pages = ["Home", "Request Quote", "Services", "Questionnaires", "Event Planning Tips", "DJs", "Photographers", "Event Coordinators"]
    
    # Add authentication options based on login status
    if is_client_logged_in:
        pages.extend(["Dashboard", "Logout"])
    elif is_professional_logged_in:
        pages.extend(["Profile", "Logout"])
    else:
        pages.extend(["Login", "Register"])
    
    # Render navigation bar
    page = st_navbar(
        pages,
        styles={
            "nav": {
                "background-color": "#1e1e1e",
                "justify-content": "left",
            },
            "div": {
                "max-width": "100%",
            },
            "span": {
                "color": "white",
                "padding": "14px 20px",
                "font-weight": "600",
            },
            "active": {
                "background-color": "#e63946",
                "color": "white",
                "font-weight": "bold",
            },
            "hover": {
                "background-color": "#d62839",
            },
        }
    )
    
    # Handle navigation only if page is different from current and not None
    if page and page != "Home":
        if page == "Request Quote":
            st.switch_page("pages/1_Request_Quote_Estimate.py")
        elif page == "DJs":
            st.switch_page("pages/4_DJs.py")
        elif page == "Photographers":
            st.switch_page("pages/2_Photographers.py")
        elif page == "Event Coordinators":
            st.switch_page("pages/3_Event_Coordinators.py")
        elif page == "Services":
            st.switch_page("pages/5_Services.py")
        elif page == "Questionnaires":
            st.switch_page("pages/6_Questionnaires.py")
        elif page == "Event Planning Tips":
            st.switch_page("pages/8_Event_Planning_Tips.py")
        elif page == "Login":
            st.switch_page("pages/90_Login.py")
        elif page == "Register":
            st.switch_page("pages/91_Client_Registration.py")
        elif page == "Dashboard":
            st.switch_page("pages/93_Client_Dashboard.py")
        elif page == "Profile":
            st.switch_page("pages/92_Profile_Management.py")
        elif page == "Logout":
            # Handle logout
            if is_client_logged_in:
                st.session_state.client_logged_in = False
                st.session_state.client_data = {}
            elif is_professional_logged_in:
                st.session_state.professional_logged_in = False
                st.session_state.professional_data = {}
            st.rerun()
    
    return page
