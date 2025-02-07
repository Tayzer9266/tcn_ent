import streamlit as st  
from streamlit_option_menu import option_menu
from st_social_media_links import SocialMediaIcons

import firebase_admin
from firebase_admin import credentials #pip install firebase_admin
from firebase_admin import auth
import io
from PIL import Image
import base64
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder  #add import for GridOptionsBuilder
import psycopg2
from streamlit_option_menu import option_menu


################################################## SET PAGE ############################################################################  
st.set_page_config(
    page_title="Song Requests",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Make your dream a reality!"
    }
)
# Use local CSS
with open("pages/style/style.css") as source_style:
    st.markdown(f"<style>{source_style.read()}</style>", unsafe_allow_html=True)

with open("pages/style/style.css") as source_style:
    st.markdown(f"<style>{source_style.read()}</style>", unsafe_allow_html=True)
st.image("pages/images/song_request.png", width=1750)  

# Inject CSS for background color
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
 
################################################## social media ############################################################################    
social_media_links = [
    "https://www.youtube.com/@DJTayzer",
    "https://www.instagram.com/Tayzer",
]

social_media_icons = SocialMediaIcons(social_media_links)
social_media_icons.render()

 

# ---- HEADER SECTION ----

contact_form = """
<form 
style = "
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    width: 50%;
    margin: auto;
    "
    action="https://formsubmit.co/tnguyen9266@GMAIL.COM" method="POST" >
        <input type="hidden" name="_captcha" value="false" >
        <br><h1 style="font-size: 50px; color: grey">Add a Song</h1></br>
        <br><input type="text" name="event" placeholder="Event name" required style="width: 800px;"></br>
        <br><input type="text" name="name" placeholder="Your name" required style="width: 800px;"></br>
        <br><input type="text" name="artist" placeholder="Artist name" required style="width: 800px;"></br>
        <br><input type="text" name="song" placeholder="Song name" required style="width: 800px;"></br>
        <br><input type="email" name="email" placeholder="Your email" required style="width: 800px;"></br>
        <br><textarea name="message"  placeholder="Your message here" style="width: 800px; height: 100px"></textarea></br>
        <br><button type="submit"  >Send</button></br>
    </form>
    """
st.markdown(contact_form, unsafe_allow_html=True)

# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
 
 


