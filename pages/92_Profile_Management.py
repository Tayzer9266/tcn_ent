import streamlit as st
import base64
import os
import sys
import json
import re
from datetime import datetime

# Add parent directory to path to import profiles_data
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from profiles_data import profile_manager
from auth_utils import require_professional_auth
from components.header_auth import render_auth_header

# Page Tab
# Require professional authentication
require_professional_auth()

# Render navigation header in sidebar
render_auth_header()

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

# Function to save gallery images
def save_gallery_image(uploaded_file, profile_type, profile_id):
    """Save uploaded gallery image and return the path"""
    if uploaded_file is not None:
        # Create gallery directory if it doesn't exist
        upload_dir = f"pages/images/uploads/{profile_type}/gallery"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate filename
        file_extension = uploaded_file.name.split('.')[-1]
        filename = f"{profile_id}_gallery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
        file_path = os.path.join(upload_dir, filename)
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path
    return None

# Function to validate YouTube URL
def validate_youtube_url(url):
    """Validate if URL is a valid YouTube URL"""
    if not url:
        return False
    
    youtube_patterns = [
        r'(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+',
        r'(https?://)?(www\.)?youtu\.be/[\w-]+',
        r'(https?://)?(www\.)?youtube\.com/embed/[\w-]+'
    ]
    
    for pattern in youtube_patterns:
        if re.match(pattern, url):
            return True
    return False

# Function to extract YouTube video ID
def extract_youtube_id(url):
    """Extract YouTube video ID from URL"""
    if 'youtube.com/watch?v=' in url:
        return url.split('watch?v=')[1].split('&')[0]
    elif 'youtu.be/' in url:
        return url.split('youtu.be/')[1].split('?')[0]
    elif 'youtube.com/embed/' in url:
        return url.split('embed/')[1].split('?')[0]
    return None

# Function to get YouTube thumbnail
def get_youtube_thumbnail(url):
    """Get YouTube video thumbnail URL"""
    video_id = extract_youtube_id(url)
    if video_id:
        return f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
    return None

# Function to get YouTube embed URL
def get_youtube_embed_url(url):
    """Convert YouTube URL to embed URL"""
    video_id = extract_youtube_id(url)
    if video_id:
        return f"https://www.youtube.com/embed/{video_id}"
    return url

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
            
            # MEDIA GALLERY SECTION
            st.markdown("---")
            st.markdown("### 🎬 Media Gallery Management")
            
            # Parse current gallery data
            try:
                current_gallery_images = json.loads(profile.get('gallery_images', '[]')) if profile.get('gallery_images') else []
            except:
                current_gallery_images = []
            
            try:
                current_gallery_videos = json.loads(profile.get('gallery_videos', '[]')) if profile.get('gallery_videos') else []
            except:
                current_gallery_videos = []
            
            # Main Profile Video
            st.markdown("**📹 Main Profile Video (YouTube):**")
            profile_video_url = st.text_input(
                "Main Profile Video URL",
                value=profile.get('profile_video_url', '') or "",
                help="Enter your main YouTube video URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)",
                key="profile_video_url"
            )
            
            if profile_video_url and validate_youtube_url(profile_video_url):
                st.success("✅ Valid YouTube URL")
                # Show preview thumbnail
                thumbnail_url = get_youtube_thumbnail(profile_video_url)
                if thumbnail_url:
                    st.image(thumbnail_url, width=200, caption="Video Preview")
            elif profile_video_url:
                st.error("❌ Invalid YouTube URL. Please use a valid YouTube link.")
            
            st.markdown("---")
            
            # Gallery Photos Section
            st.markdown("**📸 Gallery Photos:**")
            
            if current_gallery_images:
                st.markdown(f"*Current gallery has {len(current_gallery_images)} photo(s)*")
                
                # Display current images in a grid
                cols_per_row = 4
                for i in range(0, len(current_gallery_images), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, col in enumerate(cols):
                        idx = i + j
                        if idx < len(current_gallery_images):
                            with col:
                                img_path = current_gallery_images[idx]
                                img_base64 = get_base64_image(img_path)
                                if img_base64:
                                    st.markdown(
                                        f'<img src="data:image/png;base64,{img_base64}" style="width:100%; border-radius:5px; margin-bottom:5px;">',
                                        unsafe_allow_html=True
                                    )
                                else:
                                    st.markdown("🖼️ Image not found")
                                
                                # Delete button for each image
                                if st.checkbox("Delete", key=f"delete_img_{idx}"):
                                    st.warning(f"⚠️ Will delete image {idx + 1}")
            else:
                st.info("No gallery photos yet. Upload some below!")
            
            # Upload new gallery photos
            st.markdown("**Upload New Gallery Photos:**")
            gallery_uploads = st.file_uploader(
                "Choose gallery images",
                type=['png', 'jpg', 'jpeg'],
                accept_multiple_files=True,
                key="gallery_uploads",
                help="You can select multiple images at once"
            )
            
            if gallery_uploads:
                st.success(f"✅ {len(gallery_uploads)} image(s) ready to upload")
            
            st.markdown("---")
            
            # Gallery Videos Section
            st.markdown("**🎥 Gallery Videos (YouTube):**")
            
            if current_gallery_videos:
                st.markdown(f"*Current gallery has {len(current_gallery_videos)} video(s)*")
                
                # Display current videos
                for idx, video_url in enumerate(current_gallery_videos):
                    video_col1, video_col2 = st.columns([3, 1])
                    
                    with video_col1:
                        thumbnail_url = get_youtube_thumbnail(video_url)
                        if thumbnail_url:
                            st.image(thumbnail_url, width=200, caption=f"Video {idx + 1}")
                        st.text(video_url)
                    
                    with video_col2:
                        if st.checkbox("Delete", key=f"delete_video_{idx}"):
                            st.warning(f"⚠️ Will delete video {idx + 1}")
            else:
                st.info("No gallery videos yet. Add some below!")
            
            # Add new gallery video
            st.markdown("**Add New Gallery Video:**")
            new_video_url = st.text_input(
                "YouTube Video URL",
                key="new_video_url",
                help="Enter a YouTube video URL to add to your gallery"
            )
            
            if new_video_url:
                if validate_youtube_url(new_video_url):
                    st.success("✅ Valid YouTube URL - will be added when you save")
                    thumbnail_url = get_youtube_thumbnail(new_video_url)
                    if thumbnail_url:
                        st.image(thumbnail_url, width=200, caption="Video Preview")
                else:
                    st.error("❌ Invalid YouTube URL. Please use a valid YouTube link.")
            
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
                
                # Handle profile image upload
                if uploaded_file:
                    new_image_path = save_uploaded_image(
                        uploaded_file,
                        st.session_state.selected_profile_type,
                        st.session_state.selected_profile_id
                    )
                    if new_image_path:
                        update_data['image_path'] = new_image_path
                
                # Handle main profile video URL
                if profile_video_url and validate_youtube_url(profile_video_url):
                    update_data['profile_video_url'] = profile_video_url
                elif not profile_video_url:
                    update_data['profile_video_url'] = None
                
                # Handle gallery images
                updated_gallery_images = current_gallery_images.copy()
                
                # Remove deleted images
                for idx in range(len(current_gallery_images)):
                    if st.session_state.get(f"delete_img_{idx}", False):
                        img_path = current_gallery_images[idx]
                        if img_path in updated_gallery_images:
                            updated_gallery_images.remove(img_path)
                            # Optionally delete the physical file
                            try:
                                if os.path.exists(img_path):
                                    os.remove(img_path)
                            except:
                                pass
                
                # Add new gallery images
                if gallery_uploads:
                    for uploaded_gallery_file in gallery_uploads:
                        new_gallery_path = save_gallery_image(
                            uploaded_gallery_file,
                            st.session_state.selected_profile_type,
                            st.session_state.selected_profile_id
                        )
                        if new_gallery_path:
                            updated_gallery_images.append(new_gallery_path)
                
                update_data['gallery_images'] = json.dumps(updated_gallery_images)
                
                # Handle gallery videos
                updated_gallery_videos = current_gallery_videos.copy()
                
                # Remove deleted videos
                for idx in range(len(current_gallery_videos)):
                    if st.session_state.get(f"delete_video_{idx}", False):
                        video_url = current_gallery_videos[idx]
                        if video_url in updated_gallery_videos:
                            updated_gallery_videos.remove(video_url)
                
                # Add new gallery video
                if new_video_url and validate_youtube_url(new_video_url):
                    if new_video_url not in updated_gallery_videos:
                        updated_gallery_videos.append(new_video_url)
                
                update_data['gallery_videos'] = json.dumps(updated_gallery_videos)
                
                # Update profile
                success = profile_manager.update_profile(
                    st.session_state.selected_profile_type,
                    st.session_state.selected_profile_id,
                    update_data
                )
                
                if success:
                    st.success("✅ Profile updated successfully!")
                    # Clear delete checkboxes from session state
                    for key in list(st.session_state.keys()):
                        if key.startswith('delete_img_') or key.startswith('delete_video_'):
                            del st.session_state[key]
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
