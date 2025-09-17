import streamlit as st
import base64


from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
from PIL import Image
from datetime import datetime, date
from utils.pdf_generator import PDFGenerator, generate_dj_contract_pdf_response

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
################################################## DATABASE CONNECTION ############################################################################

# Load database credentials from Streamlit secrets
db_config = st.secrets["postgres"]

# Create the SQLAlchemy engine using connection string format
def init_connection():
    connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    engine = create_engine(connection_string)
    return engine.connect()

conn = init_connection()

#RUN QUERY
def run_query(query):
    try:
        # Begin a transaction using the context manager
        with conn.begin():
            # Execute the query
            result = conn.execute(text(query))
            
            # Fetch all results and load them into a pandas DataFrame
            rows = result.fetchall()
            if not rows:
                return pd.DataFrame()  # Return an empty DataFrame if no rows
            
            # Get column names and create the DataFrame
            columns = result.keys()
            df = pd.DataFrame(rows, columns=columns)
            df = df.reset_index(drop=True)  # Reset index to avoid displaying it
            
            # Transaction commits automatically if no exception occurs
            return df
    except Exception as e:
        # Log or handle the exception
        raise RuntimeError(f"Error executing query: {e}")
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
# Questionnaire download section (existing PDF downloads)
st.markdown('<div class="section-title">📥 Download Editable PDF Questionnaires</div>', unsafe_allow_html=True)
st.markdown(
    """
    Prefer to fill out a PDF? Download and complete the appropriate questionnaire for your event type. 
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





with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        def main():
            # Ask the user if they want a new quote
            # Create a drop-down menu for new quote or preview existing quotes
            global selected_bookings
            selected_bookings = []
            if 'selected_bookings' not in st.session_state:
                st.session_state.selected_bookings = []
            #photo_booth_options = ['Yes', 'No']
            booth_location= ""
            created_by=""
            option = st.radio(
                        "Select a questionnaire option",
                        ('Your Questionnaires'),
                        index=0)
        
            if option == "New": 
                #create questionnaires type   
                with st.form("my_form"):
                    #display the questionnare they selected

                    # Submit button
                    submitted = st.form_submit_button("Submit")

                    if option == "Your Bookings":
                # Add your logic to preview existing quotes here
                        email = st.text_input("Email Address*", "") 
                        # Add a submit button
                        #try:
                        query = f"""
                            SELECT booking_id, 
                                event_status, 
                                event_date, 
                                event_type, 
                                estimated_guest, 
                                event_location, 
                                start_time, 
                                service_hours, 
                                billing_status, 
                                payment_due_date, 
                                actual_cost,
                                last_name,
                                event_date_ct
                            FROM f_get_bookings('{email}')
                        """
                


                try:
                    rows = run_query(query)              
                except Exception as e:
                            st.error(f"An error occurred while retrieving bookings: {e}")
                if rows.empty:
                    st.error("Please enter a email address.")
                else:
                    st.success("Here are the details of your bookings:")  

                options = []
                
                for index, row in rows.iterrows():
                            option_text = f"{row['booking_id']} - {row['event_status']} - {row['event_date']} - {row['event_type']}"
                            options.append(option_text)

                selected_option = st.radio("", options)

                if selected_option:
                            
                            for index, row in rows.iterrows():
                                if selected_option == f"{row['booking_id']} - {row['event_status']} - {row['event_date']} - {row['event_type']}":
                                    selected_bookings.append(row['booking_id'])

                            booking = selected_bookings[0]
                            #for booking in selected_bookings:

                            # Fetch contract info
                            contract_query = f"""
                            SELECT
                             a.first_name,
                             a.last_name,
                             a.event_date,
                             a.start_time,
                             a.end_time,
                             a.event_type,
                             a.event_location,
                             a.booking_id,
                             a.venue,
                             a.grand_total,
                             a.products,
                             a.professional,
                             a.today
                            FROM f_get_contract_info('{booking}') a
                            """
                            contract_df = run_query(contract_query)

                            query = f"""
                            SELECT a.product as items,
                                    a.units,
                                    a.market_total AS market_price,
                                    a.savings as  savings,
                                    a.amount AS total
                                FROM f_service_product_total('{booking}') as a
                                """


                                # Execute the query and create a DataFrame
                            df = run_query(query)
 


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
