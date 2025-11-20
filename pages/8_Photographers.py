import streamlit as st
import base64

# Page Tab
st.set_page_config(
    page_title="Photographers",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# Professional Photographers for Your Events!"
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

# Fake Photographers Data
photographers = [
    {
        "id": "photographer_1",
        "name": "Samantha Lee",
        "title": "Wedding & Event Photographer",
        "short_bio": "Capturing timeless moments with artistic flair. Specializing in weddings and corporate events.",
        "image": "pages/images/photographer_sam.png",
        "full_bio": "Elena Vasquez is a passionate photographer with over 10 years of experience in capturing the essence of special occasions. Her work focuses on creating stunning visuals that tell the story of your event, from intimate portraits to grand celebrations. Based in Dallas, TX, she works closely with event planners to ensure every shot is perfect.",
        "youtube": None,
        "instagram": None,
        "facebook": None
    }
]

# Load the images
youtube_img = base64.b64encode(open("pages/images/youtube.png", "rb").read()).decode()
instagram_img = base64.b64encode(open("pages/images/instagram.png", "rb").read()).decode()
facebook_img = base64.b64encode(open("pages/images/facebook.png", "rb").read()).decode()

# Header Section
st.markdown('<div class="section-title">Meet Our Professional Photographers</div>', unsafe_allow_html=True)
st.markdown(
    """
    Our team of skilled photographers is dedicated to capturing the essence of your event. From weddings to corporate gatherings, we ensure every moment is preserved with professionalism and creativity.
    """
)

# Profiles Grid
cols = st.columns(3)
for i, photo in enumerate(photographers):
    with cols[i % 3]:
        st.markdown(f'<div class="profile-card">', unsafe_allow_html=True)
        # Image using base64
        img_base64 = get_base64_image(photo["image"])
        if img_base64:
            st.markdown(
                f'<img src="data:image/png;base64,{img_base64}" width="200" style="border-radius: 10px;">',
                unsafe_allow_html=True
            )
        else:
            st.markdown('<p>Image not available</p>', unsafe_allow_html=True)
        st.markdown(f'**{photo["name"]}**')
        st.markdown(f'*{photo["title"]}*')
        st.markdown(photo["short_bio"])
        # Social media links
        social_cols = st.columns(3)
        if photo.get("youtube"):
            with social_cols[0]:
                st.markdown(
                    f"""<a href="{photo["youtube"]}">
                    <img src="data:image/png;base64,{youtube_img}" width="30">
                    </a>""",
                    unsafe_allow_html=True,
                )
        if photo.get("instagram"):
            with social_cols[1]:
                st.markdown(
                    f"""<a href="{photo["instagram"]}">
                    <img src="data:image/png;base64,{instagram_img}" width="30">
                    </a>""",
                    unsafe_allow_html=True,
                )
        if photo.get("facebook"):
            with social_cols[2]:
                st.markdown(
                    f"""<a href="{photo["facebook"]}">
                    <img src="data:image/png;base64,{facebook_img}" width="30">
                    </a>""",
                    unsafe_allow_html=True,
                )
        st.markdown('</div>', unsafe_allow_html=True)
