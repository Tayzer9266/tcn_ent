import streamlit as st
import base64
import os
import sys

# Add parent directory to path to import profiles_data
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from profiles_data import profile_manager
from client_manager import client_manager
from components.header_auth import render_auth_header

# Page Tab
st.set_page_config(
    page_title="Login",
    page_icon="pages/images/TCN logo black.jpg",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# TCN Entertainment Login"
    }
)

# Render authentication header
render_auth_header()

# Background for page
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
.login-container {
    background: white;
    border-radius: 15px;
    padding: 2em;
    box-shadow: 0 4px 20px rgba(230,57,70,0.15);
    max-width: 500px;
    margin: 2em auto;
}
.login-title {
    font-size: 2em;
    font-weight: 700;
    color: #457b9d;
    text-align: center;
    margin-bottom: 0.5em;
}
.login-subtitle {
    font-size: 1em;
    color: #666;
    text-align: center;
    margin-bottom: 1.5em;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'user_profile_type' not in st.session_state:
    st.session_state.user_profile_type = None
if 'user_type' not in st.session_state:
    st.session_state.user_type = None  # 'professional' or 'client'

def login(email, password):
    """Validate login credentials against database - supports both professionals and clients"""
    # Try professional login first
    success, user_data, profile_type = profile_manager.authenticate_user(email, password)
    
    if success:
        st.session_state.logged_in = True
        st.session_state.user_email = email
        st.session_state.user_data = user_data
        st.session_state.user_profile_type = profile_type
        st.session_state.user_type = 'professional'
        return True, 'professional'
    
    # Try client login
    success, client_data = client_manager.authenticate_client(email, password)
    
    if success:
        st.session_state.logged_in = True
        st.session_state.user_email = email
        st.session_state.user_data = client_data
        st.session_state.user_profile_type = 'client'
        st.session_state.user_type = 'client'
        return True, 'client'
    
    return False, None

def logout():
    """Logout user"""
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.user_data = None
    st.session_state.user_profile_type = None
    st.session_state.user_type = None

# Check if already logged in
if st.session_state.logged_in:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">✅ Already Logged In</div>', unsafe_allow_html=True)
    
    # Display different info based on user type
    if st.session_state.user_type == 'client':
        # Client display
        client_name = f"{st.session_state.user_data['first_name']} {st.session_state.user_data['last_name']}"
        st.markdown(f'<div class="login-subtitle">Welcome back, {client_name}!</div>', unsafe_allow_html=True)
        
        st.success(f"**Email:** {st.session_state.user_email}")
        st.info(f"**Account Type:** 👤 Client")
        st.info(f"**Phone:** {st.session_state.user_data.get('phone_number', 'Not provided')}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Go to Dashboard", type="primary", use_container_width=True):
                st.switch_page("pages/93_Client_Dashboard.py")
        
        with col2:
            if st.button("Logout", use_container_width=True):
                logout()
                st.rerun()
    else:
        # Professional display
        user_role = st.session_state.user_data.get('role', 'user')
        role_badge = "🔑 Admin" if user_role == 'admin' else "👤 Professional"
        
        st.markdown(f'<div class="login-subtitle">Welcome back, {st.session_state.user_data["name"]}!</div>', unsafe_allow_html=True)
        
        st.success(f"**Email:** {st.session_state.user_email}")
        st.info(f"**Role:** {role_badge}")
        st.info(f"**Title:** {st.session_state.user_data['title']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Go to Profile Management", type="primary", use_container_width=True):
                st.switch_page("pages/92_Profile_Management.py")
        
        with col2:
            if st.button("Logout", use_container_width=True):
                logout()
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Login Form
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔐 Login</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">Access Your Account</div>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        email = st.text_input("Email Address", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            submit = st.form_submit_button("Login", type="primary", use_container_width=True)
        with col2:
            clear = st.form_submit_button("Clear", use_container_width=True)
        
        if submit:
            if not email:
                st.error("Please enter your email address")
            elif not password:
                st.error("Please enter your password")
            else:
                success, user_type = login(email, password)
                if success:
                    if user_type == 'client':
                        st.success("✅ Client login successful! Redirecting to dashboard...")
                    else:
                        st.success("✅ Professional login successful! Redirecting to profile management...")
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password. Please try again.")
        
        if clear:
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Client Registration CTA
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("**New Client?**")
        if st.button("Register Here", type="primary", use_container_width=True):
            st.switch_page("pages/91_Client_Registration.py")
    
    # Info section
    st.markdown("---")
    st.info("💡 **Note:** This login page supports both client and professional accounts. Clients can request quotes and manage events. Professionals can manage their profiles and respond to client requests.")
    
    with st.expander("📧 Need Help?"):
        st.markdown("""
        **For Clients:**
        - New to TCN Entertainment? Click "Register Here" above to create an account
        - Already registered? Use your email and password to login
        
        **For Professionals:**
        - Use the email address provided to you by TCN Entertainment
        - Default password: `Siepe2025!`
        - Contact admin if you need to reset your password
        
        **For Administrators:**
        - Use your admin credentials to access all profiles
        - Admin email: `tcnentertainmen7@gmail.com`
        """)
