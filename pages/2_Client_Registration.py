import streamlit as st
import os
import sys
import re

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client_manager import client_manager

# Page configuration
st.set_page_config(
    page_title="Client Registration",
    page_icon="pages/images/TCN logo black.jpg",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# Register for TCN Entertainment Services"
    }
)

# Custom CSS
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
.registration-container {
    background: white;
    border-radius: 15px;
    padding: 2em;
    box-shadow: 0 4px 20px rgba(230,57,70,0.15);
    max-width: 600px;
    margin: 2em auto;
}
.registration-title {
    font-size: 2em;
    font-weight: 700;
    color: #457b9d;
    text-align: center;
    margin-bottom: 0.5em;
}
.registration-subtitle {
    font-size: 1em;
    color: #666;
    text-align: center;
    margin-bottom: 1.5em;
}
.form-section {
    margin-bottom: 1.5em;
}
.section-header {
    font-size: 1.2em;
    font-weight: 600;
    color: #457b9d;
    margin-bottom: 0.5em;
    border-bottom: 2px solid #e63946;
    padding-bottom: 0.3em;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    # Remove common formatting characters
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    # Check if it's 10 digits
    return len(cleaned) >= 10 and cleaned.isdigit()

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Password is strong"

# Main content
st.markdown('<div class="registration-container">', unsafe_allow_html=True)
st.markdown('<div class="registration-title">📝 Client Registration</div>', unsafe_allow_html=True)
st.markdown('<div class="registration-subtitle">Create your account to request quotes and manage events</div>', unsafe_allow_html=True)

# Registration form
with st.form("registration_form"):
    # Personal Information
    st.markdown('<div class="section-header">👤 Personal Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name *", placeholder="John")
    with col2:
        last_name = st.text_input("Last Name *", placeholder="Doe")
    
    # Contact Information
    st.markdown('<div class="section-header">📞 Contact Information</div>', unsafe_allow_html=True)
    
    email = st.text_input("Email Address *", placeholder="john.doe@example.com")
    phone_number = st.text_input("Phone Number *", placeholder="(214) 555-0100")
    
    # Account Security
    st.markdown('<div class="section-header">🔒 Account Security</div>', unsafe_allow_html=True)
    
    password = st.text_input("Password *", type="password", placeholder="Enter a strong password")
    confirm_password = st.text_input("Confirm Password *", type="password", placeholder="Re-enter your password")
    
    # Password requirements
    with st.expander("📋 Password Requirements"):
        st.markdown("""
        Your password must contain:
        - At least 8 characters
        - At least one uppercase letter (A-Z)
        - At least one lowercase letter (a-z)
        - At least one number (0-9)
        """)
    
    # Terms and conditions
    st.markdown("---")
    agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy *")
    
    # Submit buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        submit = st.form_submit_button("Create Account", type="primary", use_container_width=True)
    with col2:
        clear = st.form_submit_button("Clear Form", use_container_width=True)
    
    if submit:
        # Validation
        errors = []
        
        if not first_name:
            errors.append("First name is required")
        if not last_name:
            errors.append("Last name is required")
        if not email:
            errors.append("Email address is required")
        elif not validate_email(email):
            errors.append("Invalid email format")
        if not phone_number:
            errors.append("Phone number is required")
        elif not validate_phone(phone_number):
            errors.append("Invalid phone number format (must be 10 digits)")
        if not password:
            errors.append("Password is required")
        else:
            is_valid, msg = validate_password(password)
            if not is_valid:
                errors.append(msg)
        if not confirm_password:
            errors.append("Please confirm your password")
        elif password != confirm_password:
            errors.append("Passwords do not match")
        if not agree_terms:
            errors.append("You must agree to the Terms of Service")
        
        # Display errors or proceed with registration
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
        else:
            # Attempt registration
            success, message, client_id = client_manager.register_client(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                password=password
            )
            
            if success:
                st.success(f"✅ {message}")
                st.balloons()
                st.info("🔑 You can now login with your email and password")
                
                # Provide login button
                if st.button("Go to Login Page", type="primary"):
                    st.switch_page("pages/1_Login.py")
            else:
                st.error(f"❌ {message}")
    
    if clear:
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Additional information
st.markdown("---")
st.markdown("### 🎉 Why Register?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **📋 Easy Quotes**
    
    Request quotes for DJ, Photography, and Event Coordination services
    """)

with col2:
    st.markdown("""
    **💬 Direct Chat**
    
    Communicate directly with professionals about your event
    """)

with col3:
    st.markdown("""
    **📊 Track Events**
    
    Manage all your events and quotes in one place
    """)

# Already have account
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.markdown("**Already have an account?**")
    if st.button("Login Here", use_container_width=True):
        st.switch_page("pages/1_Login.py")
