import streamlit as st
import base64
import os
import sys
from datetime import datetime

# Add parent directory to path to import profiles_data
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from profiles_data import profile_manager
from auth_utils import require_professional_auth

# Page Tab
# Require professional authentication
require_professional_auth()

st.set_page_config(
    page_title="Profile Management",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# Manage Your Profile"
    }
)

# Background for page
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
.section-title {
    font-size: 1.8em;
    font-weight: 700;
    color: #457b9d;
    margin-top: 1em;
    margin-bottom: 0.5em;
}
.profile-card {
    background: linear-gradient(90deg, #f8fafc 70%, #D9D4D2 100%);
    border-radius: 10px;
    padding: 1em;
    margin-bottom: 1em;
    box-shadow: 0 2px 12px rgba(230,57,70,0.08);
}
.edit-section {
    background: white;
    border-radius: 10px;
    padding: 1.5em;
    margin-top: 1em;
    box-shadow: 0 2px 12px rgba(69,123,157,0.1);
}
.admin-badge {
    background: #e63946;
    color: white;
    padding: 0.3em 0.8em;
    border-radius: 5px;
    font-size: 0.9em;
    font-weight: 600;
}
.user-badge {
    background: #457b9d;
    color: white;
    padding: 0.3em 0.8em;
    border-radius: 5px;
    font-size: 0.9em;
    font-weight: 600;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'selected_profile_type' not in st.session_state:
    st.session_state.selected_profile_type = None
if 'selected_profile_id' not in st.session_state:
    st.session_state.selected_profile_id = None

# Check authentication
if not st.session_state.logged_in:
    st.warning("⚠️ You must be logged in to access this page.")
    st.info("Please login to manage your profile.")
    if st.button("Go to Login Page", type="primary"):
        st.switch_page("pages/90_Login.py")
    st.stop()

# Get user role
user_role = st.session_state.user_data.get('role', 'user')
is_admin = (user_role == 'admin')

# Header with logout button
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    if is_admin:
        st.markdown('<div class="section-title">🔑 Admin Dashboard - Profile Management</div>', unsafe_allow_html=True)
        st.markdown(f'<span class="admin-badge">ADMIN</span> **{st.session_state.user_data["name"]}** ({st.session_state.user_email})', unsafe_allow_html=True)
    else:
        st.markdown('<div class="section-title">👤 My Profile</div>', unsafe_allow_html=True)
        st.markdown(f'<span class="user-badge">USER</span> **{st.session_state.user_data["name"]}** ({st.session_state.user_email})', unsafe_allow_html=True)
with col2:
    if st.button("💼 Quote Requests", type="primary", use_container_width=True):
        st.switch_page("pages/97_Professional_Quotes.py")
with col3:
    if st.button("Logout", type="secondary", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.session_state.user_data = None
        st.session_state.user_profile_type = None
        st.session_state.selected_profile_type = None
        st.session_state.selected_profile_id = None
        st.switch_page("pages/90_Login.py")

st.markdown("---")

# Function to encode image to base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# Function to save uploaded image
def save_uploaded_image(uploaded_file, profile_type, profile_id):
    """Save uploaded image and return the path"""
    if uploaded_file is not None:
        # Create directory if it doesn't exist
        upload_dir = f"pages/images/uploads/{profile_type}"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate filename
        file_extension = uploaded_file.name.split('.')[-1]
        filename = f"{profile_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
        file_path = os.path.join(upload_dir, filename)
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path
    return None

# Initialize add_new_profile state
if 'add_new_profile' not in st.session_state:
    st.session_state.add_new_profile = False

# ADMIN VIEW - Can see all profiles
if is_admin:
    st.markdown('<div class="section-title">Select Profile Type to Manage</div>', unsafe_allow_html=True)
    
    profile_type_col1, profile_type_col2, profile_type_col3 = st.columns(3)
    
    with profile_type_col1:
        if st.button("📸 Photographers", use_container_width=True, type="primary" if st.session_state.selected_profile_type == "photographers" else "secondary"):
            st.session_state.selected_profile_type = "photographers"
            st.session_state.selected_profile_id = None
            st.session_state.add_new_profile = False
            st.rerun()
    
    with profile_type_col2:
        if st.button("🎉 Event Coordinators", use_container_width=True, type="primary" if st.session_state.selected_profile_type == "event_coordinators" else "secondary"):
            st.session_state.selected_profile_type = "event_coordinators"
            st.session_state.selected_profile_id = None
            st.session_state.add_new_profile = False
            st.rerun()
    
    with profile_type_col3:
        if st.button("🎵 DJs", use_container_width=True, type="primary" if st.session_state.selected_profile_type == "djs" else "secondary"):
            st.session_state.selected_profile_type = "djs"
            st.session_state.selected_profile_id = None
            st.session_state.add_new_profile = False
            st.rerun()
    
    # Display profiles if a type is selected
    if st.session_state.selected_profile_type:
        st.markdown("---")
        
        # Get profiles
        profiles = profile_manager.get_all_profiles(st.session_state.selected_profile_type)
        
        # Display profile type title
        type_names = {
            "photographers": "Photographers",
            "event_coordinators": "Event Coordinators",
            "djs": "DJs"
        }
        
        # Header with Add New button
        header_col1, header_col2 = st.columns([3, 1])
        with header_col1:
            st.markdown(f'<div class="section-title">Manage {type_names[st.session_state.selected_profile_type]}</div>', unsafe_allow_html=True)
        with header_col2:
            if st.button("➕ Add New", type="primary", use_container_width=True):
                st.session_state.add_new_profile = True
                st.session_state.selected_profile_id = None
                st.rerun()
        
        # Display profiles in cards
        if profiles:
            for profile in profiles:
                # Skip admin profile in listings
                if profile.get('role') == 'admin':
                    continue
                    
                with st.container():
                    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([1, 3, 1])
                    
                    with col1:
                        # Display profile image
                        img_base64 = get_base64_image(profile['image_path'])
                        if img_base64:
                            st.markdown(
                                f'<img src="data:image/png;base64,{img_base64}" width="100" style="border-radius: 10px;">',
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown("📷 No Image")
                    
                    with col2:
                        st.markdown(f"**{profile['name']}**")
                        st.markdown(f"*{profile['title']}*")
                        if profile.get('email'):
                            st.markdown(f"📧 {profile['email']}")
                        st.markdown(f"{profile['short_bio'][:100]}...")
                    
                    with col3:
                        if st.button("Edit", key=f"edit_{profile['profile_id']}", use_container_width=True):
                            st.session_state.selected_profile_id = profile['profile_id']
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info(f"No {type_names[st.session_state.selected_profile_type].lower()} found.")

# USER VIEW - Can only see their own profile
else:
    st.markdown('<div class="section-title">My Profile Information</div>', unsafe_allow_html=True)
    
    # Automatically set the profile type and ID for the logged-in user
    if not st.session_state.selected_profile_type:
        st.session_state.selected_profile_type = st.session_state.user_profile_type
        st.session_state.selected_profile_id = st.session_state.user_data['profile_id']
    
    # Get user's profile
    profile = profile_manager.get_profile_by_id(
        st.session_state.user_profile_type,
        st.session_state.user_data['profile_id']
    )
    
    if profile:
        # Display profile card
        with st.container():
            st.markdown('<div class="profile-card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Display profile image
                img_base64 = get_base64_image(profile['image_path'])
                if img_base64:
                    st.markdown(
                        f'<img src="data:image/png;base64,{img_base64}" width="150" style="border-radius: 10px;">',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown("📷 No Image")
            
            with col2:
                st.markdown(f"### {profile['name']}")
                st.markdown(f"**{profile['title']}**")
                st.markdown(f"📧 {profile.get('email', 'N/A')}")
                st.markdown(f"**Bio:** {profile['short_bio']}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Edit button
        if st.button("✏️ Edit My Profile", type="primary", use_container_width=True):
            st.session_state.selected_profile_id = profile['profile_id']
            st.rerun()

# Edit Form (for both admin and users)
if st.session_state.selected_profile_id and st.session_state.selected_profile_type:
    st.markdown("---")
    st.markdown('<div class="edit-section">', unsafe_allow_html=True)
    
    # Get selected profile
    profile = profile_manager.get_profile_by_id(
        st.session_state.selected_profile_type,
        st.session_state.selected_profile_id
    )
    
    if profile:
        st.markdown(f'<div class="section-title">✏️ Edit Profile: {profile["name"]}</div>', unsafe_allow_html=True)
        
        with st.form("edit_profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Name", value=profile['name'])
                title = st.text_input("Title", value=profile['title'])
                short_bio = st.text_area("Short Bio", value=profile['short_bio'] or "", height=100)
                
                # Service Location
                st.markdown("**Service Location:**")
                service_col1, service_col2 = st.columns(2)
                with service_col1:
                    service_city = st.text_input("City", value=profile.get('service_city', 'Dallas'), key="service_city")
                with service_col2:
                    service_state = st.text_input("State", value=profile.get('service_state', 'Texas'), key="service_state")
                
                service_radius_miles = st.number_input(
                    "Service Radius (miles)", 
                    min_value=0, 
                    max_value=500, 
                    value=profile.get('service_radius_miles', 50),
                    step=5,
                    help="How many miles outside your city/state you're willing to travel"
                )
            
            with col2:
                full_bio = st.text_area("Full Bio", value=profile['full_bio'] or "", height=100)
                
                # Current image display
                st.markdown("**Current Image:**")
                img_base64 = get_base64_image(profile['image_path'])
                if img_base64:
                    st.markdown(
                        f'<img src="data:image/png;base64,{img_base64}" width="150" style="border-radius: 10px;">',
                        unsafe_allow_html=True
                    )
                
                # Image upload
                uploaded_file = st.file_uploader("Upload New Image (optional)", type=['png', 'jpg', 'jpeg'])
            
            st.markdown("**Contact Information:**")
            
            # Phone Number
            phone = st.text_input("📞 Phone Number", value=profile.get('phone', '') or "", 
                                 help="Your contact phone number (e.g., (214) 555-0100)")
            
            # Personal Website
            website = st.text_input("🌐 Personal Website", value=profile.get('website', '') or "", 
                                   help="Your professional website URL (e.g., https://www.yourwebsite.com)")
            
            st.markdown("**Social Media Links:**")
            
            # Social Media
            social_col1, social_col2, social_col3 = st.columns(3)
            
            with social_col1:
                youtube = st.text_input("YouTube URL", value=profile['youtube'] or "")
            
            with social_col2:
                instagram = st.text_input("Instagram URL", value=profile['instagram'] or "")
            
            with social_col3:
                facebook = st.text_input("Facebook URL", value=profile['facebook'] or "")
            
            # Admin-only: Featured checkbox
            if is_admin:
                st.markdown("---")
                st.markdown("**🌟 Admin Settings:**")
                featured = st.checkbox(
                    "Featured Professional", 
                    value=profile.get('featured', False),
                    help="Featured professionals appear prominently on the website"
                )
            
            # Form buttons
            button_col1, button_col2, button_col3 = st.columns([1, 1, 2])
            
            with button_col1:
                submit = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
            
            with button_col2:
                cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
            
            if submit:
                # Prepare update data
                update_data = {
                    'name': name,
                    'title': title,
                    'short_bio': short_bio,
                    'full_bio': full_bio,
                    'service_city': service_city,
                    'service_state': service_state,
                    'service_radius_miles': service_radius_miles,
                    'phone': phone if phone else None,
                    'website': website if website else None,
                    'youtube': youtube if youtube else None,
                    'instagram': instagram if instagram else None,
                    'facebook': facebook if facebook else None
                }
                
                # Add featured field if admin
                if is_admin:
                    update_data['featured'] = featured
                
                # Handle image upload
                if uploaded_file:
                    new_image_path = save_uploaded_image(
                        uploaded_file,
                        st.session_state.selected_profile_type,
                        st.session_state.selected_profile_id
                    )
                    if new_image_path:
                        update_data['image_path'] = new_image_path
                
                # Update profile
                success = profile_manager.update_profile(
                    st.session_state.selected_profile_type,
                    st.session_state.selected_profile_id,
                    update_data
                )
                
                if success:
                    st.success("✅ Profile updated successfully!")
                    st.session_state.selected_profile_id = None
                    st.rerun()
                else:
                    st.error("❌ Failed to update profile. Please try again.")
            
            if cancel:
                st.session_state.selected_profile_id = None
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
if is_admin:
    st.markdown(
        """
        <div style="text-align: center; color: #666; padding: 1em;">
            <p>🔑 <strong>Admin Access:</strong> You can view and edit all professional profiles.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <div style="text-align: center; color: #666; padding: 1em;">
            <p>💡 <strong>Tip:</strong> Changes made here will be reflected on your public profile page.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
