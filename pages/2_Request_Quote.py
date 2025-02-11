import streamlit as st
import time
import datetime
import io
from PIL import Image
import base64

st.set_page_config(
    page_title="Questionnaires",
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


# Use local CSS
with open("pages/style/style.css") as source_style:
    st.markdown(f"<style>{source_style.read()}</style>", unsafe_allow_html=True)
st.image("pages/images/quote.png", width=1750)  

# Inject CSS for background color
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
 
#Event Quote
# st.title("Questions")
st.write(
        """Easily tell us about your upcoming event by filling out our quick and simple form below.  This will ensure that we provide you
        with an accurate quote. Get started today and make your event one to remember with the best in entertainment!"""
)

 
with st.form("my_form"):
    if "my_input_first_name" not in st.session_state:
        st.session_state["my_input_first_name"] = ""

    my_input_first_name = st.text_input("First Name", st.session_state["my_input_first_name"]) #FirstName
    my_input_last_name = st.text_input("Last Name", "") #LastName
    my_input_phone_number = st.text_input("Phone Number", "") #Phone
    my_email = st.text_input("Email Address", "") #Email
    my_contact_time = st.text_input("Best Time to Contact", "") #Contact
    my_start_time = st.text_input("Start Time", "") #Start
    my_end_time = st.text_input("End Time", "") #End
    my_budget = st.text_input("Buget Amount", "") #Buget
    event_type = st.selectbox("Event Type?", ("Wedding", "Birthday", "Annaversary", "Corporate Function","Engagement", "Club", "Concert", "Other"))
    st.write("#")
    my_venue_location= st.text_input("Venue Location", "") #LastName
    event_date = st.date_input("Event Date", value=None) 
    st.write("#")
    guest_count = st.slider('Number of guests', 0, 1, 600)
    st.write("#")
    service_hour_count = st.slider('Number of hours professional needed', 0, 1, 9)
    st.write("#")
    mc_service = st.radio(
        "Do you need MC Service?",
        ('Yes', 'No'))
    kj_service = st.radio(
        "Do you need Karoake Service?",
        ('Yes', 'No'))
    pa_system = st.radio(
        "Do you need a PA system?",
        ('Yes', 'No'))
    microphone = st.radio(
        "Do you need microphones?",
        ('Yes', 'No'))
    dance_lights = st.radio(
        "Do you need dance floor lighting effects?",
        ('Yes', 'No'))
    disco_ball = st.radio(
        "Do you need a disco ball with lighting?",
        ('Yes', 'No'))
    uplighting = st.radio(
        "Do you need uplighting for the venue?",
        ('Yes', 'No'))
    st.write("#")
    photo_booth = st.radio(
        "Do you need a photo booth?",
        ('Yes', 'No'))
    photo_booth_prints = st.radio(
        "If yes, do you need a backdrop?",
        ('Yes', 'No'))
    photo_booth_prints = st.radio(
        "If yes, do you need unlimited photo prints?",
        ('Yes', 'No'))
    additional_comment= st.text_area("Additional comments", "")  

    submit = st.form_submit_button("Submit")
 
    if submit:
        st.session_state["my_input"] = my_input_first_name
        st.success('Thank you! We will be intouch shortly.', icon="✅")

 
 

 

 
 
 

 