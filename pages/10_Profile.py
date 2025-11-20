import streamlit as st

# Page Tab
st.set_page_config(
    page_title="Profile",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# Professional Profile Details!"
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
.profile-detail {
    background: linear-gradient(90deg, #f8fafc 70%, #D9D4D2 100%);
    border-radius: 10px;
    padding: 2em;
    box-shadow: 0 2px 12px rgba(230,57,70,0.08);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Get query parameter
query_params = st.query_params
profile_id = query_params.get("profile", None)

# Combined Profiles Data
profiles = {
    "photographer_1": {
        "name": "Elena Vasquez",
        "title": "Wedding & Event Photographer",
        "image": "pages/images/wedding.jpg",
        "full_bio": "Elena Vasquez is a passionate photographer with over 10 years of experience in capturing the essence of special occasions. Her work focuses on creating stunning visuals that tell the story of your event, from intimate portraits to grand celebrations. Based in Dallas, TX, she works closely with event planners to ensure every shot is perfect.",
        "contact": "Email: elena@tcnentertainment.com | Phone: (214) 555-1234"
    },
    "photographer_2": {
        "name": "Marcus Thompson",
        "title": "Portrait & Reception Photographer",
        "image": "pages/images/reception.jpg",
        "full_bio": "Marcus Thompson specializes in reception photography, capturing the joy and energy of your guests. With a keen eye for detail and a background in fine arts, he delivers high-quality images that preserve your event's magic. Available for private parties, weddings, and corporate gatherings.",
        "contact": "Email: marcus@tcnentertainment.com | Phone: (214) 555-5678"
    },
    "photographer_3": {
        "name": "Sophia Ramirez",
        "title": "Entrance & Ceremony Photographer",
        "image": "pages/images/wedding_entrance.jpg",
        "full_bio": "Sophia Ramirez excels in photographing entrances and ceremonies, ensuring every significant moment is documented beautifully. Her portfolio includes weddings, bar mitzvahs, and quinceañeras. She uses state-of-the-art equipment to provide clients with gallery-quality images.",
        "contact": "Email: sophia@tcnentertainment.com | Phone: (214) 555-9012"
    },
    "coordinator_1": {
        "name": "Isabella Moreno",
        "title": "Wedding & Party Coordinator",
        "image": "pages/images/corporate event.jpg",
        "full_bio": "Isabella Moreno has been coordinating events for over 8 years, specializing in weddings and private parties. She handles everything from venue selection to timeline management, ensuring a stress-free experience for her clients. Her passion for perfection makes every event seamless and memorable.",
        "contact": "Email: isabella@tcnentertainment.com | Phone: (214) 555-3456"
    },
    "coordinator_2": {
        "name": "David Lee",
        "title": "Corporate & Fundraiser Coordinator",
        "image": "pages/images/party.jpg",
        "full_bio": "David Lee brings expertise in organizing corporate events and fundraisers. He focuses on creating engaging experiences that align with your goals, from networking mixers to charity galas. His strategic planning ensures high attendance and positive outcomes.",
        "contact": "Email: david@tcnentertainment.com | Phone: (214) 555-7890"
    },
    "coordinator_3": {
        "name": "Olivia Chen",
        "title": "School & Milestone Coordinator",
        "image": "pages/images/school prom.jpg",
        "full_bio": "Olivia Chen specializes in coordinating school events like proms and homecomings, as well as milestone celebrations such as quinceañeras and sweet sixteens. She works closely with schools and families to create safe, enjoyable environments filled with excitement and tradition.",
        "contact": "Email: olivia@tcnentertainment.com | Phone: (214) 555-2345"
    }
}

if profile_id and profile_id in profiles:
    profile = profiles[profile_id]
    st.markdown('<div class="section-title">Profile Details</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="profile-detail">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(profile["image"], width=300)
    with col2:
        st.markdown(f'## {profile["name"]}')
        st.markdown(f'### {profile["title"]}')
        st.markdown(profile["full_bio"])
        st.markdown(f'**Contact:** {profile["contact"]}')
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Profile not found. Please navigate from the Photographers or Event Coordinators page.")
