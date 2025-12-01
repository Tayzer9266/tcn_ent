import streamlit as st
import base64

# Page Tab
st.set_page_config(
    page_title="Login",
    page_icon="pages/images/TCN logo black.jpg",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# TCN Entertainment Admin Login"
    }
)

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

# Hardcoded password
ADMIN_PASSWORD = "Siepe2025!"

def login(email, password):
    """Validate login credentials"""
    if password == ADMIN_PASSWORD and email:
        st.session_state.logged_in = True
        st.session_state.user_email = email
        return True
    return False

def logout():
    """Logout user"""
    st.session_state.logged_in = False
    st.session_state.user_email = None

# Check if already logged in
if st.session_state.logged_in:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">✅ Already Logged In</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="login-subtitle">Welcome back, {st.session_state.user_email}!</div>', unsafe_allow_html=True)
    
    st.success(f"You are currently logged in as: **{st.session_state.user_email}**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Go to Profile Management", type="primary", use_container_width=True):
            st.switch_page("pages/13_Profile_Management.py")
    
    with col2:
        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Login Form
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔐 Admin Login</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">Access Profile Management</div>', unsafe_allow_html=True)
    
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
            elif login(email, password):
                st.success("Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("Invalid password. Please try again.")
        
        if clear:
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Info section
    st.markdown("---")
    st.info("💡 **Note:** This login page provides access to the profile management system where you can edit Event Coordinator, Photographer, and DJ profiles.")
