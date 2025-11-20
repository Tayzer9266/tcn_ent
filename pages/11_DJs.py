import streamlit as st

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



# Fake DJs Data
djs = [
    {
        "id": "dj_1",
        "name": "DJ Tayzer",
        "title": "Master DJ & Event Specialist",
        "short_bio": "Expert in mixing beats and creating unforgettable atmospheres. Specializing in weddings and parties.",
        "image": "pages/images/djs_tay.png",
        "full_bio": "DJ Tayzer is a seasoned professional with over 10 years of experience in the DJ industry. Known for his seamless transitions and crowd-engaging sets, he specializes in weddings, corporate events, and private parties. Based in Dallas, TX, he brings energy and professionalism to every gig."
    },
    {
        "id": "dj_2",
        "name": "DJ SpinMaster",
        "title": "Karaoke & Dance Floor DJ",
        "short_bio": "Master of karaoke sessions and dance floor vibes. Keeping the party going all night.",
        "image": "pages/images/work_karaoke.png",
        "full_bio": "DJ SpinMaster excels in karaoke and interactive DJ services, ensuring guests have a blast. With a vast library of songs and a knack for reading the crowd, he creates dynamic experiences for school dances, fundraisers, and celebrations. Available for unlimited hours."
    },
    {
        "id": "dj_3",
        "name": "DJ NightVibe",
        "title": "Lighting & Sound DJ",
        "short_bio": "Combining top-tier sound and lighting effects. Elevating events with professional setups.",
        "image": "pages/images/work_night.jpg",
        "full_bio": "DJ NightVibe focuses on full-service DJ packages including premium sound systems, moving heads, and LED effects. He handles everything from setup to breakdown, making events seamless. Ideal for proms, bar mitzvahs, and corporate gatherings."
    }
]

# Header Section
st.markdown('<div class="section-title">Meet Our Professional DJs</div>', unsafe_allow_html=True)
st.markdown(
    """
    Our talented DJs are experts in creating the perfect soundtrack for your event. From weddings to fundraisers, we deliver high-energy performances and professional service. Click on any image to view their full profile.
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

# cols = st.columns(3)
# for i, dj in enumerate(djs):
#     with cols[i % 3]:
#         st.markdown(f'<div class="profile-card">', unsafe_allow_html=True)
#         # Clickable Image
#         st.markdown(
#             f'<a href="?profile={dj["id"]}" target="_self"><img src="{dj["image"]}" width="200" style="border-radius: 10px;"></a>',
#             unsafe_allow_html=True
#         )
#         st.markdown(f'**{dj["name"]}**')
#         st.markdown(f'*{dj["title"]}*')
#         st.markdown(dj["short_bio"])
#         st.markdown('</div>', unsafe_allow_html=True)
