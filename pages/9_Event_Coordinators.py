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
        "id": "coordinator_1",
        "name": "Isabella Moreno",
        "title": "Wedding & Party Coordinator",
        "short_bio": "Expert in seamless wedding and party planning. Ensuring every detail is perfect.",
        "image": "pages/images/corporate event.jpg",
        "full_bio": "Isabella Moreno has been coordinating events for over 8 years, specializing in weddings and private parties. She handles everything from venue selection to timeline management, ensuring a stress-free experience for her clients. Her passion for perfection makes every event seamless and memorable."
    },
    {
        "id": "coordinator_2",
        "name": "David Lee",
        "title": "Corporate & Fundraiser Coordinator",
        "short_bio": "Specializing in corporate events and fundraisers. Strategic planning for successful outcomes.",
        "image": "pages/images/party.jpg",
        "full_bio": "David Lee brings expertise in organizing corporate events and fundraisers. He focuses on creating engaging experiences that align with your goals, from networking mixers to charity galas. His strategic planning ensures high attendance and positive outcomes."
    },
    {
        "id": "coordinator_3",
        "name": "Olivia Chen",
        "title": "School & Milestone Coordinator",
        "short_bio": "Coordinating school events and milestones. Creating safe and exciting experiences.",
        "image": "pages/images/school prom.jpg",
        "full_bio": "Olivia Chen specializes in coordinating school events like proms and homecomings, as well as milestone celebrations such as quinceañeras and sweet sixteens. She works closely with schools and families to create safe, enjoyable environments filled with excitement and tradition."
    }
]

# Header Section
st.markdown('<div class="section-title">Meet Our Professional Event Coordinators</div>', unsafe_allow_html=True)
st.markdown(
    """
    Our dedicated event coordinators bring years of experience to ensure your event runs smoothly from start to finish. From weddings to corporate gatherings, we handle all the details so you can focus on enjoying the moment. Click on any image to view their full profile.
    """
)

# Profiles Grid
cols = st.columns(3)
for i, coord in enumerate(coordinators):
    with cols[i % 3]:
        st.markdown(f'<div class="profile-card">', unsafe_allow_html=True)
        # Clickable Image
        st.markdown(
            f'<a href="?profile={coord["id"]}" target="_self"><img src="{coord["image"]}" width="200" style="border-radius: 10px;"></a>',
            unsafe_allow_html=True
        )
        st.markdown(f'**{coord["name"]}**')
        st.markdown(f'*{coord["title"]}*')
        st.markdown(coord["short_bio"])
        st.markdown('</div>', unsafe_allow_html=True)
