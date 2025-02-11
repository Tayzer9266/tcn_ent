import streamlit as st  
import io
from PIL import Image
import base64


################################################## SET PAGE ############################################################################  
st.set_page_config(
    page_title="Song Requests",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
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

################################################## Email Form ############################################################################    

 
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
        <br><input type="text" name="name" placeholder="Your name" required style="width: 300px;"></br>
        <br><input type="text" name="artist" placeholder="Artist name" required style="width: 300px;"></br>
        <br><input type="text" name="song" placeholder="Song name" required style="width: 300px;"></br>
        <br><textarea name="message"  placeholder="Your message here" style="width: 300px; height: 100px"></textarea></br>
        <br><button type="submit"  >Send</button></br>
    </form>
    """
st.markdown(contact_form, unsafe_allow_html=True)

# Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)