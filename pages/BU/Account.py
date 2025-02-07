import streamlit as st
import firebase_admin
from firebase_admin import credentials #pip install firebase_admin
from firebase_admin import auth
import io
from PIL import Image
import base64

st.set_page_config(
    page_title="Account",
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
# Inject CSS for background color
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
 
 
def f():
    try:
        user = auth.get_user_by_email(email)
         #print(user.uid)
        st.write('Login Successful')
    except:
        st.warning('Login Failed')

        
st.title('Welcome to TCN')
with st.form("my_form"):
    choice = st.selectbox('Login/Signup',['Login', 'Signup'])

    if choice=='Login':
            email=st.text_input('Email Address')
            password=st.text_input('Password', type='password')
            st.form_submit_button('Login', on_click=f)
    else: 
            email=st.text_input('Email Address')
            password=st.text_input('Password', type='password')
            username = st.text_input('Enter your unique username')
    if st.form_submit_button('Create my account'):
            user = auth.create_user(email = email, password = password, uid=username)
            st.success('Account created successfully!')
            st.markdown('Please Login using your email and password')
            st.balloons()

 