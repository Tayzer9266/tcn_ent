"""
Authentication utilities for page access control
"""
import streamlit as st

def require_client_auth():
    """
    Require client authentication to access a page.
    Redirects to login if not authenticated or not a client.
    """
    if not st.session_state.get('logged_in', False):
        st.error("⚠️ Please login to access this page")
        st.info("This page is only accessible to registered clients.")
        if st.button("Go to Login", type="primary"):
            st.switch_page("pages/1_Login.py")
        st.stop()
    
    if st.session_state.get('user_type') != 'client':
        st.error("⚠️ Access Denied")
        st.info("This page is only accessible to registered clients.")
        if st.button("Go to Home", type="primary"):
            st.switch_page("Home.py")
        st.stop()

def require_professional_auth():
    """
    Require professional authentication to access a page.
    Redirects to login if not authenticated or not a professional.
    """
    if not st.session_state.get('logged_in', False):
        st.error("⚠️ Please login to access this page")
        st.info("This page is only accessible to professionals.")
        if st.button("Go to Login", type="primary"):
            st.switch_page("pages/1_Login.py")
        st.stop()
    
    if st.session_state.get('user_type') != 'professional':
        st.error("⚠️ Access Denied")
        st.info("This page is only accessible to professionals.")
        if st.button("Go to Home", type="primary"):
            st.switch_page("Home.py")
        st.stop()

def is_client_logged_in():
    """Check if a client is logged in"""
    return st.session_state.get('logged_in', False) and st.session_state.get('user_type') == 'client'

def is_professional_logged_in():
    """Check if a professional is logged in"""
    return st.session_state.get('logged_in', False) and st.session_state.get('user_type') == 'professional'
