import streamlit as st

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

# Fake Photographers Data
photographers = [
    {
        "name": "Samantha Lee",
        "title": "Wedding & Event Photographer",
        "short_bio": "Capturing timeless moments with artistic flair. Specializing in weddings and corporate events.",
        "image": "pages/images/photographer_sam.jpg",
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
        # Image
        st.image(photo["image"], width=200)
        st.markdown(f'**{photo["name"]}**')
        st.markdown(f'*{photo["title"]}*')
        st.markdown(photo["short_bio"])
        st.markdown('</div>', unsafe_allow_html=True)
