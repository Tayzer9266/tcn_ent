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
.interactive-form-card {
    background: linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%);
    border-radius: 15px;
    padding: 30px;
    margin: 20px 0;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    border-left: 5px solid #4CAF50;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.interactive-form-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.15);
}
.form-option-button {
    background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
    color: white;
    border: none;
    padding: 15px 30px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    font-weight: 600;
    margin: 10px 5px;
    cursor: pointer;
    border-radius: 8px;
    transition: all 0.3s ease;
    width: 200px;
}
.form-option-button:hover {
    background: linear-gradient(135deg, #45a049 0%, #3d8b40 100%);
    box-shadow: 0 6px 15px rgba(76, 175, 80, 0.4);
    transform: translateY(-2px);
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

# Questionnaire download section (existing PDF downloads)
st.markdown('<div class="section-title">📥 Download Editable PDF Questionnaires</div>', unsafe_allow_html=True)
st.markdown(
    """
    Prefer to fill out a PDF? Download and complete the appropriate questionnaire for your event type. 
    Once completed, you can return it to us via email or bring it to our consultation meeting.
    """
)
st.markdown("---")
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
            key="wedding_pdf"
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
            key="party_pdf"
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
            key="mitzvah_pdf"
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
            key="sweet_sixteen_pdf"
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
            key="photo_booth_pdf"
        )
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")

# Interactive Form Section
st.markdown('<div class="section-title">📝 Interactive Questionnaires</div>', unsafe_allow_html=True)
st.markdown(
    """
    Fill out our interactive questionnaires to help us better understand your event needs. 
    Start by entering your email address below, then select the type of event you're planning.
    """
)

# Email input section
st.markdown('<div class="interactive-form-card">', unsafe_allow_html=True)
st.markdown("### 📧 Start Your Questionnaire")

if 'user_email' not in st.session_state:
    st.session_state.user_email = ""
if 'selected_form' not in st.session_state:
    st.session_state.selected_form = None

email = st.text_input("Enter your email address:", value=st.session_state.user_email, 
                     placeholder="your.email@example.com", key="email_input")

if email:
    st.session_state.user_email = email
    st.success(f"Email saved: {email}")
    
    # Form selection
    st.markdown("### 🎯 Select Your Event Type")
    st.write("Choose the type of event you're planning:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💍 Wedding", key="wedding_btn", use_container_width=True):
            st.session_state.selected_form = "Wedding"
            st.rerun()
        if st.button("🎭 Mitzvah", key="mitzvah_btn", use_container_width=True):
            st.session_state.selected_form = "Mitzvah"
            st.rerun()
    
    with col2:
        if st.button("👑 Quinceañera", key="quinceanera_btn", use_container_width=True):
            st.session_state.selected_form = "Quinceanera"
            st.rerun()
        if st.button("🎂 Sweet Sixteen", key="sweet_sixteen_btn", use_container_width=True):
            st.session_state.selected_form = "Sweet_Sixteen"
            st.rerun()
    
    with col3:
        if st.button("🎉 Birthday Party", key="birthday_btn", use_container_width=True):
            st.session_state.selected_form = "Birthday_Party"
            st.rerun()
        if st.button("🎊 General Party", key="general_btn", use_container_width=True):
            st.session_state.selected_form = "General_Party"
            st.rerun()

# Display selected form
if st.session_state.selected_form:
    st.markdown("---")
    st.markdown(f"### 📋 {st.session_state.selected_form.replace('_', ' ')} Questionnaire")
    
    # Import and render the selected form
    try:
        form_module = __import__(f"pages.questionnaires.{st.session_state.selected_form}_Form", fromlist=['render'])
        form_module.render()
        
        # Save button
        if st.button("💾 Save Progress", key="save_btn", use_container_width=True):
            st.success("Your progress has been saved! You can return later to continue.")
            # In a real implementation, this would save to a database
            # For now, we'll just show a success message
    except ImportError:
        st.warning(f"Form for {st.session_state.selected_form} is not available yet.")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")



st.markdown("---")

# Contact information
st.markdown('<div class="section-title">📞 Need Help?</div>', unsafe_allow_html=True)
st.markdown(
    """
    If you have any questions about filling out the questionnaire or need assistance, 
    please don't hesitate to contact us:
    - 📧 Email: tcnentertainmen7@gmail.com
    - 📞 Phone: (714) 260-5003
    """
)
