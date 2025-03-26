import streamlit as st
import time
import datetime
import io
from PIL import Image
import base64
#from fpdf import FPDF

st.set_page_config(
    page_title="Questionnaires",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Make your dream a reality!"
    }
)

# Load the images
youtube_img = base64.b64encode(open("pages/images/youtube.png", "rb").read()).decode()
instagram_img = base64.b64encode(open("pages/images/instagram.png", "rb").read()).decode()
facebook_img = base64.b64encode(open("pages/images/facebook.png", "rb").read()).decode()

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
with col3:
    st.markdown(
        """<a href="https://www.facebook.com/profile.php?id=61574735690575">
        <img src="data:image/png;base64,{}" width="50">
        </a>""".format(facebook_img),
        unsafe_allow_html=True
    )


# Use local CSS
with open("pages/style/style.css") as source_style:
    st.markdown(f"<style>{source_style.read()}</style>", unsafe_allow_html=True)


# Use local CSS
with open("pages/style/style.css") as source_style:
    st.markdown(f"<style>{source_style.read()}</style>", unsafe_allow_html=True)
st.image("pages/images/event_questionnaire.png", width=1750)  

# Inject CSS for background color
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
 
 
#st.title("Questionnaires")
st.write(
        """Help us tailor the ultimate experience just for you! We're passionate about making your event unforgettable. By answering a few quick questions, you can help us craft the perfect atmosphere for your celebration. From song preferences to special requests, your input ensures our performance hits all the right notes. 
            We’re here to help!"""
)

st.subheader("Download Editable PDF Questionnaires")
 
with open("pages/documents/Wedding DJ Questionnaire.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()
    st.download_button(label="Wedding Questionnaire",
                        data=PDFbyte,
                        file_name="Wedding Questionnaire.pdf",
                        mime='application/octet-stream')

with open("pages/documents/Mitzvah Song Questionnaire v1.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()
    st.download_button(label="Mitzvah Questionnaire",
                        data=PDFbyte,
                        file_name="Mitzvah Questionnaire.pdf",
                        mime='application/octet-stream')
    
with open("pages/documents/Party Song Questionnaire v2.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()
    st.download_button(label="Party Questionnaire",
                        data=PDFbyte,
                        file_name="Party Questionnaire.pdf",
                        mime='application/octet-stream')
    
with open("pages/documents/Sweet Sixteen Questionnaire.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()
    st.download_button(label="Sweet Sixteen Questionnaire",
                        data=PDFbyte,
                        file_name="Sweet Sixteen Questionnaire.pdf",
                        mime='application/octet-stream')
with open("pages/documents/Photo Booth Questionnaire.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()
    st.download_button(label="Photo Booth Questionnaire",
                        data=PDFbyte,
                        file_name="Photo Booth Questionnaire.pdf",
                        mime='application/octet-stream')

# class PDF(FPDF):
#     def header(self):
#         self.set_font('Arial', 'B', 12)
#         self.cell(0, 10, 'Your PDF Title', 0, 1, 'C')

# pdf = PDF()
# pdf.add_page()
# pdf.set_font('Arial', '', 12)
# pdf.cell(0, 10, 'Hello World in PDF', 0, 1)
# # Assume `pdf` is your generated PDF object
# pdf_output = pdf.output(dest='S').encode('latin1')
# st.download_button(label='Wedding Questionnaire', data=pdf_output, file_name='example.pdf', mime='application/pdf')


# #Logo
# file = open("pages/images/company_logo_padding.png", "rb")
# contents = file.read()
# img_str = base64.b64encode(contents).decode("utf-8")
# buffer = io.BytesIO()
# file.close()
# img_data = base64.b64decode(img_str)
# img = Image.open(io.BytesIO(img_data))
# resized_img = img.resize((310, 56))  # x, y
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

 
 
 

 

 
 
 

 