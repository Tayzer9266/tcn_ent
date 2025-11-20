import streamlit as st
import base64

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

# Fake DJs Data
djs = [
    {
        "id": "dj_1",
        "name": "DJ Tayzer",
        "title": "Master DJ & Event Specialist",
        "short_bio": "Expert in mixing beats and creating unforgettable atmospheres. Specializing in weddings and parties.",
        "image": "pages/images/djs_tay.png",
        "full_bio": "DJ Tayzer is a seasoned professional with over 10 years of experience in the DJ industry. Known for his seamless transitions and crowd-engaging sets, he specializes in weddings, corporate events, and private parties. Based in Dallas, TX, he brings energy and professionalism to every gig.",
        "youtube": "https://www.youtube.com/@djtayzer",
        "instagram": "https://www.instagram.com/tayzer/",
        "facebook": "https://www.facebook.com/profile.php?id=61574735690575"
    },
    {
        "id": "dj_2",
        "name": "DJ Tyler",
        "title": "House Music DJ",
        "short_bio": "Master of house music beats, creating energetic and soulful atmospheres. Specializing in dance parties and festivals.",
        "image": "pages/images/djs_tyler.png",
        "full_bio": "DJ Tyler is a passionate house music enthusiast with over 8 years of experience in the DJ industry. Known for his deep house sets and infectious vibes, he specializes in dance parties, festivals, and private events. Based in Dallas, TX, he brings soulful energy and professionalism to every gig.",
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
        img_base64 = get_base64_image(dj["image"])
        if img_base64:
            st.markdown(
                f'<img src="data:image/png;base64,{img_base64}" width="200" style="border-radius: 10px;">',
                unsafe_allow_html=True
            )
        else:
            st.markdown('<p>Image not available</p>', unsafe_allow_html=True)
        st.markdown(f'**{dj["name"]}**')
        st.markdown(f'*{dj["title"]}*')
        st.markdown(dj["short_bio"])
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
