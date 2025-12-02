import streamlit as st
import base64
import os
import sys

# Add parent directory to path to import profiles_data
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from profiles_data import profile_manager

# Page Tab
st.set_page_config(
    page_title="Event Coordinators",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# Professional Event Coordinators for Your Events!"
    }
)

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

# Get Event Coordinators Data from database (exclude admin profiles)
all_coordinators = profile_manager.get_all_profiles("event_coordinators")
coordinators = [c for c in all_coordinators if c.get('role') != 'admin']

# Load the images
youtube_img = base64.b64encode(open("pages/images/youtube.png", "rb").read()).decode()
instagram_img = base64.b64encode(open("pages/images/instagram.png", "rb").read()).decode()
facebook_img = base64.b64encode(open("pages/images/facebook.png", "rb").read()).decode()

# Header Section
st.markdown('<div class="section-title">Meet Our Professional Event Coordinators</div>', unsafe_allow_html=True)
st.markdown(
    """
    Our experienced event coordinators handle every detail to ensure your event runs smoothly. From weddings to corporate gatherings, we bring expertise and creativity to make your occasion unforgettable.
    """
)

# Profiles Grid
cols = st.columns(3)
for i, coord in enumerate(coordinators):
    with cols[i % 3]:
        st.markdown(f'<div class="profile-card">', unsafe_allow_html=True)
        # Image using base64
        img_base64 = get_base64_image(coord["image_path"])
        if img_base64:
            st.markdown(
                f'<img src="data:image/jpeg;base64,{img_base64}" width="200" style="border-radius: 10px;">',
                unsafe_allow_html=True
            )
        else:
            st.markdown('<p>Image not available</p>', unsafe_allow_html=True)
        st.markdown(f'**{coord["name"]}**')
        st.markdown(f'*{coord["title"]}*')
        st.markdown(coord["short_bio"])
        
        # Contact Information
        st.markdown("---")
        if coord.get("email"):
            st.markdown(f'📧 {coord["email"]}')
        if coord.get("phone"):
            st.markdown(f'📞 {coord["phone"]}')
        if coord.get("website"):
            st.markdown(f'🌐 [{coord["website"]}]({coord["website"]})')
        
        # Social media links
        social_cols = st.columns(3)
        if coord.get("youtube"):
            with social_cols[0]:
                st.markdown(
                    f"""<a href="{coord["youtube"]}">
                    <img src="data:image/png;base64,{youtube_img}" width="30">
                    </a>""",
                    unsafe_allow_html=True,
                )
        if coord.get("instagram"):
            with social_cols[1]:
                st.markdown(
                    f"""<a href="{coord["instagram"]}">
                    <img src="data:image/png;base64,{instagram_img}" width="30">
                    </a>""",
                    unsafe_allow_html=True,
                )
        if coord.get("facebook"):
            with social_cols[2]:
                st.markdown(
                    f"""<a href="{coord["facebook"]}">
                    <img src="data:image/png;base64,{facebook_img}" width="30">
                    </a>""",
                    unsafe_allow_html=True,
                )
        st.markdown('</div>', unsafe_allow_html=True)
