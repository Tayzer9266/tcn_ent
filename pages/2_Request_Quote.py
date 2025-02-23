import streamlit as st  
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import base64
from PIL import Image



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

# # HTML content
# html_content = """
# <a href="https://www.gigsalad.com/tcn_entertainment_dallas"><img src="https://cress.gigsalad.com/images/svg/standalone/promokit-links/book-securely/book-securely--dark.svg" alt="Hire me on GigSalad" height="100" width="300"></a>
# """
# # Display the HTML content
# components.html(html_content, height=100)

################################################## DATABASE CONNECTION ############################################################################

# Load database credentials from Streamlit secrets
db_config = st.secrets["postgres"]

# Create the SQLAlchemy engine using connection string format
def init_connection():
    connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    engine = create_engine(connection_string)
    return engine.connect()

conn = init_connection()

def execute_procedure(first_name, last_name, phone_number, email, best_time, event_date, start_time,
                      estimated_budget, event_type, event_location, guest_count, pa_system, dancing_lights, disco_ball,
                      uplighting, fog_machine, low_fog_machine, photo_booth, photo_booth_prints, booth_location,
                      comments, created_by, uplight_ct, backdrop_props, back_drop_type, service_hours, service_types):
    try:
        # Convert boolean radio button responses to True/False
        pa_system = pa_system == 'Yes'
        dancing_lights = dancing_lights == 'Yes'
        disco_ball = disco_ball == 'Yes'
        uplighting = uplighting == 'Yes'
        fog_machine = fog_machine == 'Yes'
        low_fog_machine = low_fog_machine == 'Yes'
        photo_booth = photo_booth == 'Yes'
        photo_booth_prints = photo_booth_prints == 'Yes'

        # Set empty string inputs to None
        best_time = best_time if best_time else None
        start_time = start_time if start_time else None
        estimated_budget = estimated_budget if estimated_budget else None
        event_location = event_location if event_location else None
        booth_location = booth_location if booth_location else None
        comments = comments if comments else None
        created_by = created_by if created_by else None

        # Create the SQL procedure call using SQLAlchemy text()
        query = text("CALL sp_client_quote(:first_name, :last_name, :phone_number, :email, " +
                     ":best_time, :event_date, :start_time, " +
                     ":estimated_budget, :event_type, :event_location, :guest_count, :pa_system, " +
                     ":dancing_lights, :disco_ball, :uplighting, :fog_machine, " +
                     ":low_fog_machine, :photo_booth, :photo_booth_prints, :booth_location, " +
                     ":comments, :created_by, :uplight_ct, :backdrop_props, :back_drop_type, " +
                     ":service_hours, :service_types)")

        # Execute the procedure with the parameters as named arguments
        with conn.begin():  # Start a transaction block
            conn.execute(query, {
                "first_name": first_name, "last_name": last_name, "phone_number": phone_number, "email": email,
                "best_time": best_time, "event_date": event_date, "start_time": start_time,
                "estimated_budget": estimated_budget, "event_type": event_type, "event_location": event_location,
                "guest_count": guest_count, "pa_system": pa_system, "dancing_lights": dancing_lights, "disco_ball": disco_ball,
                "uplighting": uplighting, "fog_machine": fog_machine, "low_fog_machine": low_fog_machine, "photo_booth": photo_booth,
                "photo_booth_prints": photo_booth_prints, "booth_location": booth_location, "comments": comments,
                "created_by": created_by, "uplight_ct": uplight_ct, "backdrop_props": backdrop_props,
                "back_drop_type": back_drop_type, "service_hours": service_hours, "service_types": service_types
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
    #df = df.reset_index(drop=True)
    return df



def main():
    # Ask the user if they want a new quote
    # Create a drop-down menu for new quote or preview existing quotes
    global selected_bookings
    selected_bookings = []
    if 'selected_bookings' not in st.session_state:
        st.session_state.selected_bookings = []
    photo_booth_options = ['Yes', 'No']
    booth_location= ""
    created_by=""
    option = st.selectbox("Select a quote", ("", "New", "Current"))
    if option == "New": 
        with st.form("my_form"):
            service_types = st.multiselect("Service Type?*", ("","DJ","MC", "Karaoke"))
            first_name = st.text_input("First Name*", "")  #FirstName
            last_name = st.text_input("Last Name*", "") #LastName
            phone_number = st.text_input("Phone Number*", "") #Phone
            email = st.text_input("Email Address*", "") #Email
            event_date = st.date_input("Event Date*", value=None) 
            event_type = st.selectbox("Event Type?*", ("","Wedding", "Birthday", "Anniversary", "Corporate Function", "Engagement", "Club", "Concert", "Other"))
            best_time = st.time_input("Best Time to Contact", None) 
            service_hours = st.slider('Number of hours professional needed', 2, 24, value=2)
            start_time = st.time_input("Estimated Start Time*", None) #Start
            estimated_budget = st.number_input("Budget Amount", 0) #Budget
            event_location = st.text_input("Venue Location", "") #Location
            guest_count = st.slider('Number of guests', 1, 600, value=50)
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
                "Do you need a disco ball?",
                ('Yes', 'No'),
                index=1)
            uplighting = st.radio(
                "Do you need uplighting?",
                ('Yes', 'No'),
                index=1)
            uplight_ct = st.slider('If yes, How many uplights', 0, 20, value=0)
            fog_machine = st.radio(
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
                    index=1
                )
            backdrop = st.radio(
                    "If yes, do you need a backdrop?",
                    ('Yes', 'No'),
                    index=1
                )
            back_drop_type = st.selectbox(
                    "Select a backdrop",
                    ("", "White", "Shimmering Black"),
                    index=0,
                    placeholder=""
                )
            backdrop_props = st.radio(
                    "If yes, do you need photo booth props?",
                    ('Yes', 'No'),
                    index=1
                )
            comments = st.text_area("Additional comments", "")   
            created_by = ""

            # Submit button
            submitted = st.form_submit_button("Submit")
            if submitted:
                # Check if all required fields are filled
                st.session_state["my_input"] = first_name
                if email and phone_number and first_name and event_date and service_hours and event_type:
                    execute_procedure(first_name, last_name, phone_number, email, best_time, event_date, start_time, estimated_budget, event_type, event_location, guest_count, pa_system, dancing_lights, disco_ball, uplighting, fog_machine, low_fog_machine, photo_booth, photo_booth_prints, booth_location, comments, created_by, uplight_ct, back_drop_type, backdrop_props, service_hours, service_types)
                else:
                    st.error("Please fill in all required fields (Name, Phone, Email, Event Date, Service Hours, Event Type).")
 
 

    elif option == "Current":
        # Add your logic to preview existing quotes here
        email = st.text_input("Email Address*", "") 
        # Add a submit button
        #if st.button('View') and email:
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
                    last_name
                FROM f_get_bookings('{email}')
            """
        rows = run_query(query)
    
        if rows.empty:
                if email:
                    st.write("Loading...")
        else:
                st.write("Booking ID | Event State  |   Event Date   |   Event Type |")
                options = []
                for index, row in rows.iterrows():
                    option_text = f"{row['booking_id']} - {row['event_status']} - {row['event_date']} - {row['event_type']}"
                    options.append(option_text)

                selected_option = st.radio("", options)

                if selected_option:
                    for index, row in rows.iterrows():
                        if selected_option == f"{row['booking_id']} - {row['event_status']} - {row['event_date']} - {row['event_type']}":
                            selected_bookings.append(row['booking_id'])

                    for booking in selected_bookings:
                        st.write(booking)

if __name__ == "__main__":
    main()
 
 
 

 