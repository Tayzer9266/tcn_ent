import streamlit as st
from PIL import Image
import base64
import streamlit.components.v1 as components
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
from datetime import time


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

# HTML content
html_content = """
<a href="https://www.gigsalad.com/tcn_entertainment_dallas"><img src="https://cress.gigsalad.com/images/svg/standalone/promokit-links/book-securely/book-securely--dark.svg" alt="Hire me on GigSalad" height="100" width="300"></a>
"""
# Display the HTML content
components.html(html_content, height=100)

################################################## DATABASE CONNECTION ############################################################################

# Load database credentials from Streamlit secrets
db_config = st.secrets["postgres"]

# Create the SQLAlchemy engine using connection string format
def init_connection():
    connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    engine = create_engine(connection_string)
    return engine.connect()

conn = init_connection()


def execute_procedure(first_name, last_name, phone_number, email, best_time, event_date, start_time, end_time, estimated_budget, event_type, event_location, guest_count, mc_service, karoake, pa_system, dancing_lights, disco_ball, uplighting, fog_machine_lights, low_fog_machine, photo_booth, photo_booth_prints, booth_location, comments, created_by):
    try:
        # Convert boolean radio button responses to True/False
        mc_service = mc_service == 'Yes'
        karoake = karoake == 'Yes'
        pa_system = pa_system == 'Yes'
        dancing_lights = dancing_lights == 'Yes'
        disco_ball = disco_ball == 'Yes'
        uplighting = uplighting == 'Yes'
        fog_machine_lights = fog_machine_lights == 'Yes'
        low_fog_machine = low_fog_machine == 'Yes'
        photo_booth = photo_booth == 'Yes'
        photo_booth_prints = photo_booth_prints == 'Yes'

        # Set empty string inputs to None
        best_time = best_time if best_time else None
        start_time = start_time if start_time else None
        end_time = end_time if end_time else None
        estimated_budget = estimated_budget if estimated_budget else None
        event_location = event_location if event_location else None
        booth_location = booth_location if booth_location else None
        comments = comments if comments else None
        created_by = created_by if created_by else None

        # Create the SQL procedure call using SQLAlchemy text()
        query = text("CALL sp_client_quote(:first_name, :last_name, :phone_number, :email " +
                     ", :best_time, :event_date, :start_time, :end_time, :estimated_budget, :event_type, :event_location " +
                     ", :guest_count, :mc_service, :karoake, :pa_system, :dancing_lights, :disco_ball, :uplighting, :fog_machine_lights " +
                     ", :low_fog_machine, :photo_booth, :photo_booth_prints, :booth_location, :comments, :created_by)")

        # Execute the procedure with the parameters as named arguments
        with conn.begin():  # Start a transaction block
            conn.execute(query, {
                "first_name": first_name, "last_name": last_name, "phone_number": phone_number, "email": email, 
                "best_time": best_time, "event_date": event_date, "start_time": start_time, "end_time": end_time, 
                "estimated_budget": estimated_budget, "event_type": event_type, "event_location": event_location, 
                "guest_count": guest_count, "mc_service": mc_service, "karoake": karoake, "pa_system": pa_system, 
                "dancing_lights": dancing_lights, "disco_ball": disco_ball, "uplighting": uplighting, "fog_machine_lights": fog_machine_lights, 
                "low_fog_machine": low_fog_machine, "photo_booth": photo_booth, "photo_booth_prints": photo_booth_prints, 
                "booth_location": booth_location, "comments": comments, "created_by": created_by
            })

        # Show success message
        st.success('Thank you! We will be in touch shortly.', icon="✅")
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")

 

# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    # Use SQLAlchemy connection and execute query
    result = conn.execute(text(query))
    # Fetch all results and load them into a pandas DataFrame
    rows = result.fetchall()
    if rows is None:
        return pd.DataFrame()  # Return an empty DataFrame instead of None
    columns = result.keys()  # Get column names
    df = pd.DataFrame(rows, columns=columns)
    # Exclude the index (reset the index to avoid displaying it)
    df = df.reset_index(drop=True)
    return df


booth_location= ""
created_by=""
with st.form("my_form"):
    first_name = st.text_input("First Name*", "")  #FirstName
    last_name = st.text_input("Last Name*", "") #LastName
    phone_number = st.text_input("Phone Number*", "") #Phone
    email = st.text_input("Email Address*", "") #Email
    event_date = st.date_input("Event Date*", value=None) 
    event_type = st.selectbox("Event Type?*", ("","Wedding", "Birthday", "Anniversary", "Corporate Function", "Engagement", "Club", "Concert", "Other"))
    best_time = st.time_input("Best Time to Contact", None) 
    start_time = st.time_input("Estimated Start Time*", None) #Start
    end_time = st.time_input("Estimated End Time*", None) #End
    estimated_budget = st.number_input("Budget Amount", 0) #Budget
    event_location = st.text_input("Venue Location", "") #Location
    guest_count = st.slider('Number of guests', 1, 600, value=50)
    service_hour_count = st.slider('Number of hours professional needed', 2, 9, value=2)
    mc_service = st.radio(
        "Do you need MC Service?",
        ('Yes', 'No'),
        index=1)
    karoake = st.radio(
        "Do you need Karoake Service?",
        ('Yes', 'No'),
        index=1)
    pa_system = st.radio(
        "Do you need PA systems?",
        ('Yes', 'No'),
        index=0)
    microphone = st.radio(
        "Do you need microphones?",
        ('Yes', 'No'),
        index=0)
    dancing_lights = st.radio(
        "Do you need dance lights?",
        ('Yes', 'No'),
        index=0)
    disco_ball = st.radio(
        "Do you need a disco ball with lighting?",
        ('Yes', 'No'),
        index=1)
    uplighting = st.radio(
        "Do you need uplighting for the venue?",
        ('Yes', 'No'),
        index=1)
    how_many_uplights = None
    if uplighting == 'Yes':
        how_many_uplights = st.slider('If yes, How many uplights', 0, 20, value=0)
    fog_machine_lights = st.radio(
        "Do you need a fog machine?",
        ('Yes', 'No'),
        index=1)
    low_fog_machine = st.radio(
        "Do you want dancing on the clouds?",
        ('Yes', 'No'),
        index=1)
    photo_booth = st.radio(
        "Do you need a photo booth?",
        ('Yes', 'No'),
        index=1)
    photo_booth_prints = st.radio(
        "If yes, do you need photo prints?",
        ('Yes', 'No'),
        index=1)
    backdrop = st.radio(
        "If yes, do you need a backdrop?",
        ('Yes', 'No'),
        index=1)
    back_drop_type = st.selectbox(
        "Select a backdrop",
        ("","White", "Shimmering Black"),
        index=0,
        placeholder=""
    )
    backdrop_props = st.radio(
        "If yes, do you need photo booth props?",
        ('Yes', 'No'),
        index=1)
    comments = st.text_area("Additional comments", "")   
    created_by = ""

    # Submit button
    submitted = st.form_submit_button("Submit")

    if submitted:
        # Check if all required fields are filled
        st.session_state["my_input"] = first_name
        if email and phone_number and first_name and event_date:
            execute_procedure(first_name, last_name, phone_number, email, best_time, event_date, start_time, end_time, estimated_budget, event_type, event_location, guest_count, mc_service, karoake, pa_system, dancing_lights, disco_ball, uplighting, fog_machine_lights, low_fog_machine, photo_booth, photo_booth_prints, booth_location, comments, created_by)
        else:
            st.error("Please fill in all required fields (Name, Phone, Email, Event Date, Est Time, Service Type).")


 

 
 
 

 