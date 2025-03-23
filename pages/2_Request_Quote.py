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
    initial_sidebar_state="collapsed",
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
                      comments, created_by, uplight_ct, backdrop_props, back_drop_type, service_hours, service_types, cold_sparks, microphone, monogram,
                      discount_code):
    try:
        # Convert boolean radio button responses to True/False
        pa_system = pa_system == 'Yes'
        dancing_lights = dancing_lights == 'Yes'
        disco_ball = disco_ball == 'Yes'
        uplighting = uplighting == 'Yes'
        fog_machine = fog_machine == 'Yes'
        backdrop_props = backdrop_props == 'Yes'
        low_fog_machine = low_fog_machine == 'Yes'
        #photo_booth = photo_booth == 'Yes'
        monogram = monogram == 'Yes'
        photo_booth_prints = photo_booth_prints == 'Yes'
        cold_sparks = cold_sparks == 'Yes'
        microphone = microphone == 'Yes'
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
                     ":service_hours, :service_types, :cold_sparks, :microphone, :monogram, :discount_code)")

        # Execute the procedure with the parameters as named arguments
        with conn.begin() as transaction:  # Start a transaction block
            try:
                conn.execute(query, {
                    "first_name": first_name, "last_name": last_name, "phone_number": phone_number, "email": email,
                    "best_time": best_time, "event_date": event_date, "start_time": start_time,
                    "estimated_budget": estimated_budget, "event_type": event_type, "event_location": event_location,
                    "guest_count": guest_count, "pa_system": pa_system, "dancing_lights": dancing_lights, "disco_ball": disco_ball,
                    "uplighting": uplighting, "fog_machine": fog_machine, "low_fog_machine": low_fog_machine, "photo_booth": photo_booth,
                    "photo_booth_prints": photo_booth_prints, "booth_location": booth_location, "comments": comments,
                    "created_by": created_by, "uplight_ct": uplight_ct, "backdrop_props": backdrop_props,
                    "back_drop_type": back_drop_type, "service_hours": service_hours, "service_types": service_types, "cold_sparks": cold_sparks, "microphone": microphone, 
                    "monogram": monogram, "discount_code": discount_code
                })
                transaction.commit()  # Explicitly commit the transaction
                conn.close()
                st.success('Thank you! We will be in touch shortly.', icon="✅")
            except Exception as e:
                transaction.rollback()  # Rollback the transaction if an error occurs
                raise e
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")


def execute_procedure_update(booking_id, event_status, first_name, last_name, phone_number, email, best_time, event_date, start_time,
                      estimated_budget, event_type, event_location, guest_count, pa_system, dancing_lights, disco_ball,
                      uplighting, fog_machine, low_fog_machine, photo_booth, photo_booth_prints, booth_location,
                      comments, created_by, uplight_ct, backdrop_props, back_drop_type, service_hours, service_types, cold_sparks, microphone, monogram, 
                      price_override, discount_code):
    try:
        # Convert boolean radio button responses to True/False
        pa_system = pa_system == 'Yes'
        dancing_lights = dancing_lights == 'Yes'
        disco_ball = disco_ball == 'Yes'
        uplighting = uplighting == 'Yes'
        fog_machine = fog_machine == 'Yes'
        low_fog_machine = low_fog_machine == 'Yes'
        backdrop_props = backdrop_props == 'Yes'
       # photo_booth = photo_booth == 'Yes'
        monogram = monogram == 'Yes'
        microphone = microphone == 'Yes'
        photo_booth_prints = photo_booth_prints == 'Yes'
        cold_sparks = cold_sparks == 'Yes'
        microphone = microphone == 'Yes'

        # Set empty string inputs to None
        best_time = best_time if best_time else None
        start_time = start_time if start_time else None
        estimated_budget = estimated_budget if estimated_budget else None
        event_location = event_location if event_location else None
        booth_location = booth_location if booth_location else None
        comments = comments if comments else None
        created_by = created_by if created_by else None
 
        # Create the SQL procedure call using SQLAlchemy text()
        query = text("CALL sp_client_quote_update(:booking_id, :event_status, :first_name, :last_name, :phone_number, :email, " +
                     ":best_time, :event_date, :start_time, " +
                     ":estimated_budget, :event_type, :event_location, :guest_count, :pa_system, " +
                     ":dancing_lights, :disco_ball, :uplighting, :fog_machine, " +
                     ":low_fog_machine, :photo_booth, :photo_booth_prints, :booth_location, " +
                     ":comments, :created_by, :uplight_ct, :backdrop_props, :back_drop_type, " +
                     ":service_hours, :service_types, :cold_sparks, :microphone, :monogram, :price_override, :discount_code)")

        # Execute the procedure with the parameters as named arguments
        conn = init_connection()
        with conn.begin():  # Start a transaction block
            transaction = conn.begin()
            try:
                conn.execute(query, {
                    "booking_id": booking_id, "event_status": event_status, "first_name": first_name, "last_name": last_name, "phone_number": phone_number, "email": email,
                    "best_time": best_time, "event_date": event_date, "start_time": start_time,
                    "estimated_budget": estimated_budget, "event_type": event_type, "event_location": event_location,
                    "guest_count": guest_count, "pa_system": pa_system, "dancing_lights": dancing_lights, "disco_ball": disco_ball,
                    "uplighting": uplighting, "fog_machine": fog_machine, "low_fog_machine": low_fog_machine, "photo_booth": photo_booth,
                    "photo_booth_prints": photo_booth_prints, "booth_location": booth_location, "comments": comments,
                    "created_by": created_by, "uplight_ct": uplight_ct, "backdrop_props": backdrop_props,
                    "back_drop_type": back_drop_type, "service_hours": service_hours, "service_types": service_types, "cold_sparks": cold_sparks, "microphone": microphone, "monogram": monogram,
                    "price_override": price_override, "discount_code": discount_code
                })
                transaction.commit()  # Explicitly commit the transaction
                conn.close()
                st.success('Your event has been updated', icon="✅")
            except Exception as e:
                transaction.rollback()  # Rollback if there's an error
                raise e
 
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")


 

# Uses st.cache_data to only rerun when the query changes or after 10 min.
#@st.cache_data.clear()
@st.cache_data(ttl=10)

# def run_query(query):
#     #try:
#         # Use SQLAlchemy connection and execute query
#         result = conn.execute(text(query))
#         # Fetch all results and load them into a pandas DataFrame
#         rows = result.fetchall()
#         if rows is None:
#             return pd.DataFrame()  # Return an empty DataFrame instead of None
#         columns = result.keys()  # Get column names
#         df = pd.DataFrame(rows, columns=columns)
#         # Exclude the index (reset the index to avoid displaying it)
#         #df = df.reset_index(drop=True)
    
#         return df
#     # finally:
#     #     conn.close()  # Ensure the connection is closed
def run_query(query):
    try:
        # Begin a transaction
        with conn.begin() as transaction:
            # Execute the query
            result = conn.execute(text(query))
            
            # Fetch all results and load them into a pandas DataFrame
            rows = result.fetchall()
            if not rows:
                return pd.DataFrame()  # Return an empty DataFrame if no rows
            
            columns = result.keys()  # Get column names
            df = pd.DataFrame(rows, columns=columns)
            df = df.reset_index(drop=True)  # Reset index to avoid displaying it
            
            # If no exception occurred, the transaction will auto-commit
            return df
    except Exception as e:
        # Rollback the transaction on error
        transaction.rollback()
        raise RuntimeError(f"Error executing query: {e}")
    
 

@st.cache_data(ttl=600)
def run_query_as_text(query):
    # Use SQLAlchemy connection and execute query
    result = conn.execute(text(query))
    rows = result.fetchall()  # Fetch all results

    if not rows:  # Check if rows are empty
        return "No data was returned for the given query."

    # Get column names
    columns = result.keys()

    # Format rows as text
    text_output = "Query Results:\n"
    text_output += "\t".join(columns) + "\n"  # Add column headers
    text_output += "-" * 40 + "\n"  # Add a separator
    for row in rows:
        text_output += "\t".join(map(str, row)) + "\n"  # Add each row of data

    return text_output

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
                "Select a quote",
                ('New', 'Current'),
                index=0)
 
    if option == "New": 
        with st.form("my_form"):
            service_types = st.multiselect("Service Type?*", ("","DJ","MC", "Karaoke"))
            first_name = st.text_input("First Name*", "")  #FirstName
            last_name = st.text_input("Last Name*", "") #LastName
            phone_number = st.text_input("Phone Number*", "") #Phone
            email = st.text_input("Email Address*", "") #Email
            discount_code = st.text_input("Discount Code", "") #Phone
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
            monogram = st.radio(
                "Do you want a projecting monogram?",
                ('Yes', 'No'),
                index=1)
            cold_sparks = st.radio(
                "Do you need cold sparks?",
                ('Yes', 'No'),
                index=1)
            photo_booth = st.selectbox(
                    "Select a photo booth",
                    ("", "DSLR Photo Booth", "IPad Photo Booth"),
                    index=0,
                    placeholder=""
                )
       
            photo_booth_prints = st.radio(
                    "If yes, do you need photo prints?",
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
                try:
                    if email and phone_number and first_name and event_date and service_hours and event_type:
                        conn = init_connection()
                        execute_procedure(first_name, last_name, phone_number, email, best_time, event_date, start_time, estimated_budget, event_type,
                                        event_location, guest_count, pa_system, dancing_lights, disco_ball, uplighting, fog_machine, low_fog_machine, 
                                        photo_booth, photo_booth_prints, booth_location, comments, created_by, uplight_ct, backdrop_props, back_drop_type,  
                                        service_hours, service_types, cold_sparks, microphone, monogram, discount_code)
                    else:
                        st.error("Please fill in all required fields (Name, Phone, Email, Event Date, Service Hours, Event Type).")
                finally:
                    conn.close()
 
 

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
        
        try:
            conn = init_connection()     
            rows = run_query(query)
        finally:
            conn.close()
        if rows.empty:
                if email:
                    st.write("Loading...")
        else:
                
                options = []
                st.write("Booking ID | Event State  |   Event Date   |   Event Type ")
                for index, row in rows.iterrows():
                    option_text = f"{row['booking_id']} - {row['event_status']} - {row['event_date']} - {row['event_type']}"
                    options.append(option_text)

                selected_option = st.radio("", options)

                if selected_option:
                    
                    for index, row in rows.iterrows():
                        if selected_option == f"{row['booking_id']} - {row['event_status']} - {row['event_date']} - {row['event_type']}":
                            selected_bookings.append(row['booking_id'])

                    #booking = selected_bookings[0]
                    for booking in selected_bookings:
                      

                        # query = f"""
                        # SELECT a.product as items,
                        #     a.units,
                        #     a.market_total AS market_price,
                        #     a.savings as  savings, 
                        #     a.amount AS total
                        # FROM f_service_product_total('{booking}') as a
                        # """


                        # # Execute the query and create a DataFrame
                        # df = run_query(query)

                        # # Display the DataFrame
                        # if not df.empty:
                        #     st.write('*This is just an estimate. We are ready to match or beat any offer—reach out to us today!')
                        #     st.write(df) # Display the first few rows for verification
                            
                        # else:
                        #     st.write("No data was returned for the given query.")
                             

                        # Define your query
                        query = f"""
                        SELECT 
                        booking_id,
                        first_name,
                        last_name,
                        phone_number,
                        email,
                        best_time,
                        event_date,
                        start_time,
                        estimated_budget,
                        event_type,
                        event_location,
                        guest_count,
                        pa_system,
                        dancing_lights,
                        disco_ball,
                        uplighting,
                        fog_machine,
                        low_fog_machine,
                        photo_booth,
                        photo_booth_prints,
                        photo_booth_props,
                        comments,
                        created_by,
                        uplight_ct,
                        backdrop_props,
                        back_drop_type,
                        service_hours,
                        service_types,
                        event_status,
                        billing_status,
                        payment_due_date,
                        actual_cost ,
                        cold_sparks,
                        microphone,
                        monogram,
                        price_override,
                        discount_code
                        FROM f_get_booking_details('{booking}')
                        """
                        try:
                            conn = init_connection()
                        # Run the query and store the results in a DataFrame
                            df = run_query(query)
                            # Convert boolean columns to integers (0 for True, 1 for False)
                        finally:
                            conn.close()
                        df = df.applymap(lambda x: 0 if x is True else 1 if x is False else x)
                        default_service_types = df['service_types'][0]
                        billing_status = df['billing_status'][0]
                        payment_due_date = df['payment_due_date'][0]
                        actual_cost = df['actual_cost'][0]
                  
                        back_drop_needed = 1 if not df['back_drop_type'][0] else 0
                        booking_id = booking
                        if df['event_status'][0] != 'Scheduled' or email == "5003":
                            with st.form("my_form"):
                                st.subheader("Booking# " + str(booking_id))

                                if email == "5003":
                                    event_status = st.selectbox("Booking Status", (df['event_status'][0], "Ongoing","Canceled","Scheduled")) 
                                else:
                                    event_status = st.selectbox("Booking Status", (df['event_status'][0],"Ongoing","Canceled")) 

                                service_types = st.multiselect(
                                    "Service Type?*",
                                    options=["", "DJ", "MC", "Karaoke"],
                                    default=default_service_types
                                )
                                if email == "5003":
                                    price_override = st.text_input("Override Price", df['price_override'][0])

                                discount_code  = st.text_input("Discount Code", df['discount_code'][0]) 
           
                                first_name = st.text_input("First Name*", df['first_name'][0])  #FirstName
                                last_name = st.text_input("Last Name*", df['last_name'][0]) #LastName
                                phone_number = st.text_input("Phone Number*", df['phone_number'][0]) #Phone
                                email = st.text_input("Email Address*", df['email'][0]) #Email
                                event_date = st.date_input("Event Date*", df['event_date'][0]) 
                                event_type = st.selectbox("Event Type?*", (df['event_type'][0],"Wedding", "Birthday", "Anniversary", "Corporate Function", "Engagement", "Club", "Concert", "Other"))
                                best_time = st.time_input("Best Time to Contact", df['best_time'][0]) 
                                service_hours = st.slider('Number of hours professional needed', 2, 24, value=df['service_hours'][0])
                                start_time = st.time_input("Estimated Start Time*", df['start_time'][0]) #Start
                                estimated_budget = st.number_input("Budget Amount", ) #Budget
                                event_location = st.text_input("Venue Location", df['event_location'][0]) #Location
                                guest_count = st.slider('Number of guests', 1, 600, value=df['guest_count'][0])
                        
                                pa_system = st.radio(
                                    "Do you need PA systems?",
                                    ('Yes', 'No'),
                                    index=int(df['pa_system'][0]))
                                microphone = st.radio(
                                    "Do you need microphones?",
                                    ('Yes', 'No'),
                                    index=int(df['microphone'][0]))
                                cold_sparks = st.radio(
                                    "Do you need cold sparks?",
                                    ('Yes', 'No'),
                                    index=int(df['cold_sparks'][0]))
                                dancing_lights = st.radio(
                                    "Do you need dance lights?",
                                    ('Yes', 'No'),
                                    index=int(df['dancing_lights'][0]))
                                disco_ball = st.radio(
                                    "Do you need a disco ball?",
                                    ('Yes', 'No'),
                                    index=int(df['disco_ball'][0])
                                    )
                                monogram = st.radio(
                                    "Do you want a projecting monogram?",
                                    ('Yes', 'No'),
                                    index=int(df['monogram'][0])
                                    )
                                uplighting = st.radio(
                                    "Do you need uplighting?",
                                    ('Yes', 'No'),
                                    index=int(df['uplighting'][0])
                                    )
                                uplight_ct = st.slider('If yes, How many uplights', 0, 20, value=df['uplight_ct'][0])
                                fog_machine = st.radio(
                                    "Do you need a fog machine?",
                                    ('Yes', 'No'),
                                    index=int(df['fog_machine'][0]))
                                low_fog_machine = st.radio(
                                    "Do you want dancing on the clouds?",
                                    ('Yes', 'No'),
                                    index=int(df['low_fog_machine'][0]))
                                photo_booth = st.selectbox(
                                            "Select a photo booth",
                                            (str(df['photo_booth'][0]), "", "DSLR Photo Booth", "IPad Photo Booth"),
                                            index=0
                                        )
                                photo_booth_prints = st.radio(
                                        "If yes, do you need photo prints?",
                                        ('Yes', 'No'),
                                        index=int(df['photo_booth_prints'][0])
                                    )
                                back_drop_type = st.selectbox(
                                    "Select a backdrop",
                                    (str(df['back_drop_type'][0]), "White", "Shimmering Black"),
                                    index=0
                                )

                                backdrop_props = st.radio(
                                        "If yes, do you need photo booth props?",
                                        ('Yes', 'No'),
                                        index=int(df['photo_booth_props'][0])
                                    )
                                comments = st.text_area("Additional comments", df['comments'][0])   
                                created_by = ""

                                # Submit button
                                submitted = st.form_submit_button("Update")
                                if submitted:
                                    # Check if all required fields are filled
                                    st.session_state["my_input"] = first_name
                                    try: 
                                        if email and phone_number and first_name and event_date and service_hours and event_type:
                                            booking_id = next(iter(booking_id)) if isinstance(booking_id, set) else booking_id
                                            execute_procedure_update(booking_id, event_status, first_name, last_name, phone_number, email, best_time, event_date, start_time, 
                                                                    estimated_budget, event_type, event_location, guest_count, pa_system, dancing_lights, disco_ball, uplighting, 
                                                                    fog_machine, low_fog_machine, photo_booth, photo_booth_prints, booth_location, comments, created_by, uplight_ct, 
                                                                    backdrop_props, back_drop_type,  service_hours, service_types, cold_sparks, microphone, monogram, price_override, discount_code)
                                        else:
                                            st.error("Please fill in all required fields (Name, Phone, Email, Event Date, Service Hours, Event Type).")
                                    finally:
                                        conn.close()

 

if __name__ == "__main__":
    main()
 
 
 

 