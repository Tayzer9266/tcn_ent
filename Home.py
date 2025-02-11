import streamlit as st
import base64
# from st_social_media_links import SocialMediaIcons

 
# Page Tab
st.set_page_config(
    page_title="Home",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# Make your dream a reality!"
    }
)


# Load the images
youtube_img = base64.b64encode(open("pages/images/youtube.png", "rb").read()).decode()
instagram_img = base64.b64encode(open("pages/images/instagram.png", "rb").read()).decode()

# Create columns in the sidebar with less spacing
col1, col2, col3, col4, col5 , col6  = st.sidebar.columns([1, 1, 1, 1, 1, 1])

with col1:
    st.markdown(
        """<a href="https://www.youtube.com/@djtayzer">
        <img src="data:image/png;base64,{}" width="30">
        </a>""".format(youtube_img),
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """<a href="https://www.instagram.com/tayzer/">
        <img src="data:image/png;base64,{}" width="30">
        </a>""".format(instagram_img),
        unsafe_allow_html=True
    )

# Background for page
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)



# Sumamry Section
with open("pages/style/style.css") as source_style:
    st.markdown(f"<style>{source_style.read()}</style>", unsafe_allow_html=True)
st.image("pages/images/featured_pro.png", width=1750)  
# ---- HEADER SECTION ----
with st.container():
    st.subheader("")
    st.title("Overview")
    st.write("##")
    st.write(
        """Welcome to TCN Entertainment, where the beats meet the streets and the fun never skips a track! I am your ultimate DJ professional with the top-tier sound and lighting. 
        I'm here to turn your event into an epic celebration that'll have everyone talking long after the music fades. 
        But I'm more than just a DJ, I will work closely with you to understand your vision, preferences, and must-play tracks. 
        I'm here to listen, collaborate, and bring your party dreams to life, one beat drop at a time. So, if you're ready to take 
        your event to the next level, let me help you and be your soundtrack to success!"""
    )
    st.write("[Get a Quote>](Request_Quote)")

   

# Sumamry Section
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Services")
        st.write("##")
        st.write(
            """
            Private Events:
            - Weddings
            - Birthdays
            - Anniversaries
            - Corporate Functions
            - Engagement Parties
            
            Public Events:
            - Club Nights
            - Festivals
            - Concerts
            - Product Launches
            - Holiday Parties
            
            Music Genres

            - Top 40 / Pop
            - EDM / House / Techno
            - Hip-Hop / R&B
            - Classic Rock / 80s / 90s Hits
            - Latin / Reggaeton
            - Jazz / Chillout
            - Custom Playlist Creation

            Event Services

            - Event Coordination with Venue & Planner
            - On-Site Setup & Breakdown
            - Full Sound & Lighting Packages
            - Visual Effects (LED, Projection Mapping)
            - Live Remixing & Mashups
            - Karaoke Setup

            Additional Features

            - Photo Booth Rentals
            - Custom Music Production
            - Virtual/Live Streaming DJ Sets
            - Wireless Microphones & PA Systems
            - Interactive Crowd Engagement (Games, Requests)

            Special Services

            - Wedding DJ & MC Services
            - Silent Disco
            - Custom Playlist Curation (Personalized music themes for your event)
            - Rehearsal Dinner DJ Services
            - Event Rehearsal Sessions for Brides & Grooms

            
            """
        )
        st.write("[Learn More >](Services)")

# Sumamry Section
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Live Song Requests")
        st.write("##")
        st.write(
            """
            We want to make sure your event has the perfect soundtrack! Our song request form allows you to share your favorite tunes, and let us know any specific songs or genres you'd like to hear. Whether you have a list of must-play tracks or just want to guide us with a vibe, we’ve got you covered. Fill out the form below to submit your requests, and we'll make sure to incorporate them into the mix to keep the party going all night long!
            """
        )
        st.write("[Learn More >](/Song_Requests)")
 

#st.image("pages/images/company_logo.png", width=200)
 
#Logo
# file = open("pages/images/", "rb")
# contents = file.read()
# img_str = base64.b64encode(contents).decode("utf-8")
# buffer = io.BytesIO()
# file.close()
# img_data = base64.b64decode(img_str)
# img = Image.open(io.BytesIO(img_data))
# resized_img = img.resize((250, 44))  # x, y
# resized_img.save(buffer, format="PNG")
# img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
# st.markdown(
#         f"""
#         <style>
#             [data-testid="stSidebarNav"] {{
#                 background-image: url('data:image/png;base64,{img_b64}');
#                 background-repeat: no-repeat;
#                 padding-top: 0px;
#                 margin-left: auto;
#                 margin-right: auto;
#             }}
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

 
# Use local CSS

# social_media_links = [
#     "https://www.youtube.com/@DJTayzer",
#     "https://www.instagram.com/Tayzer",
# ]
# st.markdown("<h1 style='text-align: center; color: green;'>Get In Touch With Me!</h1>", unsafe_allow_html=True)
# st.markdown("<h3 style='text-align: center; color: green;'>Cell: (714) 260-5003</h3>", unsafe_allow_html=True)
# social_media_icons = SocialMediaIcons(social_media_links)
# social_media_icons.render()

 
 


 
 


