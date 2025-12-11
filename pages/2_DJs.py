import streamlit as st
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import base64
from profiles_data import profile_manager
from components.header_auth import render_auth_header

# Page Tab
st.set_page_config(
    page_title="DJs",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# Professional DJs for Your Events!"
    }
)

# Render authentication header with custom navigation
render_auth_header()


# Background for page
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
.section-title {
    font-size: 1.5em;
    font-weight: 700;
    color: #457b9d;
    margin-top: 1.2em;
    margin-bottom: 0.5em;
}
.profile-card {
    background: linear-gradient(90deg, #f8fafc 70%, #D9D4D2 100%);
    border-radius: 10px;
    padding: 1em;
    margin-bottom: 1em;
    box-shadow: 0 2px 12px rgba(230,57,70,0.08);
    text-align: center;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Function to encode image to base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# Helper function to render star rating
def render_stars(rating):
    """Render star rating"""
    if rating == 0:
        return "No ratings yet"
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    stars = "⭐" * full_stars
    if half_star:
        stars += "✨"
    stars += "☆" * empty_stars
    
    return f"{stars} {rating:.1f}/5.0"

# Get DJs Data from database (exclude admin profiles)
all_djs = profile_manager.get_all_profiles("djs")
djs = [d for d in all_djs if d.get('role') != 'admin']

# Load the images
youtube_img = base64.b64encode(open("pages/images/youtube.png", "rb").read()).decode()
instagram_img = base64.b64encode(open("pages/images/instagram.png", "rb").read()).decode()
facebook_img = base64.b64encode(open("pages/images/facebook.png", "rb").read()).decode()

# Header Section
st.markdown('<div class="section-title">Meet Our Professional DJs</div>', unsafe_allow_html=True)
st.markdown(
    """
    Our talented DJs are experts in creating the perfect soundtrack for your event. From weddings to fundraisers, we deliver high-energy performances and professional service.
    """
)

# Profiles Grid
cols = st.columns(3)
for i, dj in enumerate(djs):
    with cols[i % 3]:
        st.markdown(f'<div class="profile-card">', unsafe_allow_html=True)
        # Image using base64
        img_base64 = get_base64_image(dj["image_path"])
        if img_base64:
            st.markdown(
                f'<img src="data:image/png;base64,{img_base64}" width="200" style="border-radius: 10px;">',
                unsafe_allow_html=True
            )
        else:
            st.markdown('<p>Image not available</p>', unsafe_allow_html=True)
        st.markdown(f'**{dj["name"]}**')
        st.markdown(f'*{dj["title"]}*')
        
        # Rating and Reviews
        rating = dj.get('average_rating', 0)
        total_reviews = dj.get('total_reviews', 0)
        st.markdown(f'**{render_stars(rating)}**')
        st.markdown(f'*({total_reviews} reviews)*')
        
        st.markdown(dj["short_bio"])
        
        # View Full Profile Button
        if st.button(f"👁️ View Full Profile", key=f"view_{dj['profile_id']}", use_container_width=True, type="primary"):
            st.session_state.profile_type = "djs"
            st.session_state.profile_id = dj['profile_id']
            st.switch_page("pages/98_Professional_Profile.py")
        
        # Contact Information
        st.markdown("---")
        if dj.get("email"):
            st.markdown(f'📧 {dj["email"]}')
        if dj.get("phone"):
            st.markdown(f'📞 {dj["phone"]}')
        if dj.get("website"):
            st.markdown(f'🌐 [{dj["website"]}]({dj["website"]})')
        
        # Social media links
        social_cols = st.columns(3)
        if dj.get("youtube"):
            with social_cols[0]:
                st.markdown(
                    f"""<a href="{dj["youtube"]}">
                    <img src="data:image/png;base64,{youtube_img}" width="30">
                    </a>""",
                    unsafe_allow_html=True,
                )
        if dj.get("instagram"):
            with social_cols[1]:
                st.markdown(
                    f"""<a href="{dj["instagram"]}">
                    <img src="data:image/png;base64,{instagram_img}" width="30">
                    </a>""",
                    unsafe_allow_html=True,
                )
        if dj.get("facebook"):
            with social_cols[2]:
                st.markdown(
                    f"""<a href="{dj["facebook"]}">
                    <img src="data:image/png;base64,{facebook_img}" width="30">
                    </a>""",
                    unsafe_allow_html=True,
                )
        st.markdown('</div>', unsafe_allow_html=True)
