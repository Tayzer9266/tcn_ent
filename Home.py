import streamlit as st
import base64
import streamlit.components.v1 as components
# from st_social_media_links import SocialMediaIcons
# import firebase_admin
# from firebase_admin import credentials #pip install firebase_admin
# from firebase_admin import auth
 
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder  #add import for GridOptionsBuilder
import psycopg2
 
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
 

# Sumamry Section
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Reviews")
        st.write("##")
    

html_content2 = """
<div style="display: flex; align-items: center;">
    <a href="https://www.gigsalad.com/tcn_entertainment_dallas" style="margin-right: 20px;">
        <img src="https://cress.gigsalad.com/images/svg/standalone/promokit-links/top-performer/top-performer--blue.svg" alt="Top Performer on GigSalad" height="128" width="116">
    </a>
    <a href="https://www.gigsalad.com/tcn_entertainment_dallas">
        <img src="https://cress.gigsalad.com/images/svg/standalone/promokit-links/read-reviews/read-reviews--dark.svg" alt="Read My Reviews on GigSalad" height="100" width="300">
    </a>
</div>
"""

# Display the HTML content
components.html(html_content2, height=150)

# HTML content
html_content = """
<div id="gigsalad-reviews-widget"></div><script>var gsReviewWidget;(function(d,t){var s=d.createElement(t),options={path:'254761',maxWidth:600,count:4};s.src='https://www.gigsalad.com/js/gigsalad-reviews-widget.min.js';s.onload=s.onreadystatechange=function(){var rs=this.readyState;if(rs)if(rs!='complete')if(rs!='loaded')return;try{gsReviewWidget=new GsReviewsWidget(options);gsReviewWidget.display();}catch(e){}};var scr=d.getElementsByTagName(t)[0];var par=scr.parentNode;par.insertBefore(s,scr);})(document,'script');</script>
"""

# Display the HTML content
components.html(html_content, height=2000)





 


 
 


