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
        "full_bio": "Elena Vasquez is a passionate photographer with over 10 years of experience in capturing the essence of special occasions. Her work focuses on creating stunning visuals that tell the story of your event, from intimate portraits to grand celebrations. Based in Dallas, TX, she works closely with event planners to ensure every shot is perfect."
    },
    {
        "id": "photographer_2",
        "name": "Marcus Thompson",
        "title": "Portrait & Reception Photographer",
        "short_bio": "Expert in candid shots and elegant portraits. Bringing your memories to life.",
        "image": "pages/images/reception.jpg",
        "full_bio": "Marcus Thompson specializes in reception photography, capturing the joy and energy of your guests. With a keen eye for detail and a background in fine arts, he delivers high-quality images that preserve your event's magic. Available for private parties, weddings, and corporate gatherings."
    },
    {
        "id": "photographer_3",
        "name": "Sophia Ramirez",
        "title": "Entrance & Ceremony Photographer",
        "short_bio": "Focusing on grand entrances and ceremonies. Professional and creative photography services.",
        "image": "pages/images/wedding_entrance.jpg",
        "full_bio": "Sophia Ramirez excels in photographing entrances and ceremonies, ensuring every significant moment is documented beautifully. Her portfolio includes weddings, bar mitzvahs, and quinceañeras. She uses state-of-the-art equipment to provide clients with gallery-quality images."
    }
]

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
                f'<img src="data:image/jpeg;base64,{img_base64}" width="200" style="border-radius: 10px;">',
                unsafe_allow_html=True
            )
        else:
            st.markdown('<p>Image not available</p>', unsafe_allow_html=True)
        st.markdown(f'**{photo["name"]}**')
        st.markdown(f'*{photo["title"]}*')
        st.markdown(photo["short_bio"])
        st.markdown('</div>', unsafe_allow_html=True)
