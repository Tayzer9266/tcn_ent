import streamlit as st

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

# Fake Event Coordinators Data
coordinators = [
    {
        "name": "Isabella Moreno",
        "title": "Wedding & Party Coordinator",
        "short_bio": "Expert in planning seamless weddings and private parties. Making your vision a reality.",
        "image": "pages/images/corporate event.jpg",
    },
    {
        "name": "David Lee",
        "title": "Corporate & Fundraiser Coordinator",
        "short_bio": "Specializing in corporate events and fundraisers. Driving success through meticulous planning.",
        "image": "pages/images/party.jpg",
    },
    {
        "name": "Olivia Chen",
        "title": "School & Milestone Coordinator",
        "short_bio": "Coordinating school events and milestones. Creating memorable experiences for all ages.",
        "image": "pages/images/school prom.jpg",
    }
]

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
        # Image
        st.image(coord["image"], width=200)
        st.markdown(f'**{coord["name"]}**')
        st.markdown(f'*{coord["title"]}*')
        st.markdown(coord["short_bio"])
        st.markdown('</div>', unsafe_allow_html=True)
