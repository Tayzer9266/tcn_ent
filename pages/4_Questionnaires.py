import streamlit as st
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

st.image("pages/images/event_questionnaire.png", width=1750)  

# Inject CSS for background color and enhanced card styling 717171
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
.questionnaire-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 15px;
    padding: 25px;
    margin: 20px 0;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    border-left: 5px solid #717171; /* Changed to light grey */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.questionnaire-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.15);
}
.questionnaire-card h3 {
    color: #717171; /* Changed to light grey */
    margin-bottom: 15px;
    font-size: 1.4em;
}
.questionnaire-card p {
    color: #555;
    font-size: 1em;
    margin-bottom: 20px;
}
.questionnaire-button {
    background: linear-gradient(135deg, #717171 0%, #b0b0b0 100%); /* Changed to light grey */
    color: white;
    border: none;
    padding: 12px 25px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    font-weight: 600;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 8px;
    transition: all 0.3s ease;
    width: 100%;
}
.questionnaire-button:hover {
    background: linear-gradient(135deg, #b0b0b0 0%, #a0a0a0 100%);
    box-shadow: 0 6px 15px rgba(230, 57, 70, 0.4);
    transform: translateY(-2px);
}
.questionnaire-button:active {
    transform: translateY(1px);
}
.section-title {
    color: #717171; /* Changed to light grey */
    font-size: 2em;
    font-weight: 700;
    margin-bottom: 20px;
    text-align: center;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Page title and introduction
st.markdown('<div class="section-title"></div>', unsafe_allow_html=True)
st.markdown(
    """
    Help us tailor the ultimate experience just for you! We're passionate about making your event unforgettable. 
    By answering a few quick questions, you can help us craft the perfect atmosphere for your celebration. 
    From song preferences to special requests, your input ensures our performance hits all the right notes. 
    We're here to help!
    """
)

st.markdown("---")

# Questionnaire download section
st.markdown('<div class="section-title">📥 Download Editable PDF Questionnaires</div>', unsafe_allow_html=True)
st.markdown(
    """
    Please download and fill out the appropriate questionnaire for your event type. 
    Once completed, you can return it to us via email or bring it to our consultation meeting.
    """
)

# Create columns for better layout
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="questionnaire-card">', unsafe_allow_html=True)
    st.markdown("### 💍 Wedding Questionnaire")
    st.markdown("For wedding ceremonies and receptions.")
    with open("pages/documents/Wedding DJ Questionnaire.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        st.download_button(
            label="Download Wedding Questionnaire",
            data=PDFbyte,
            file_name="Wedding Questionnaire.pdf",
            mime='application/octet-stream',
            key="wedding"
        )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="questionnaire-card">', unsafe_allow_html=True)
    st.markdown("### 🎉 Party Questionnaire")
    st.markdown("For birthday parties, corporate events, and other celebrations.")
    with open("pages/documents/Party Song Questionnaire v2.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        st.download_button(
            label="Download Party Questionnaire",
            data=PDFbyte,
            file_name="Party Questionnaire.pdf",
            mime='application/octet-stream',
            key="party"
        )
    st.markdown("### 🎭 Mitzvah Questionnaire")
    st.markdown("For Bar/Bat Mitzvah celebrations.")
    with open("pages/documents/Mitzvah Song Questionnaire v1.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        st.download_button(
            label="Download Mitzvah Questionnaire",
            data=PDFbyte,
            file_name="Mitzvah Questionnaire.pdf",
            mime='application/octet-stream',
            key="mitzvah"
        )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="questionnaire-card">', unsafe_allow_html=True)
    st.markdown("### 🎂 Sweet Sixteen Questionnaire")
    st.markdown("For Sweet Sixteen birthday celebrations.")
    with open("pages/documents/Sweet Sixteen Questionnaire.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        st.download_button(
            label="Download Sweet Sixteen Questionnaire",
            data=PDFbyte,
            file_name="Sweet Sixteen Questionnaire.pdf",
            mime='application/octet-stream',
            key="sweet_sixteen"
        )
    st.markdown("### 📸 Photo Booth Questionnaire")
    st.markdown("For photo booth services at your event.")
    with open("pages/documents/Photo Booth Questionnaire.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        st.download_button(
            label="Download Photo Booth Questionnaire",
            data=PDFbyte,
            file_name="Photo Booth Questionnaire.pdf",
            mime='application/octet-stream',
            key="photo_booth"
        )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Contact information
st.markdown('<div class="section-title">📞 Need Help?</div>', unsafe_allow_html=True)
st.markdown(
    """
    If you have any questions about filling out the questionnaire or need assistance, 
    please don't hesitate to contact us:
    - 📧 Email: info@tcnentertainment.com
    - 📞 Phone: (555) 123-4567
    """
)
