 import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import base64
from PIL import Image
from datetime import datetime
from utils.pdf_generator import PDFGenerator, generate_dj_contract_pdf_response


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
 
with st.container():
    st.write("---")
    
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("3 Easy Steps")
        st.write( """Get the party started without the hassle! Request your free, no-obligation DJ quote tailored to your event's needs—fast and easy! We're committed to offering unbeatable prices and will match or beat any competitor's offer. Plus, see how our rates compare to the average market price.""")
        st.write( """Follow these simple steps to secure your DJ services in no time:""")
        st.write( """1. Complete our quick and user-friendly request form below""")
        st.write( """2. Click on "Your Bookings".""")
        st.write( """3. Provide your email address to instantly access automated pricing results.""")
        st.write( """We will personally contact you to address any questions or concerns you may have. Once you're satisfied, you can lock in the date with a small $60 deposit.""")
 
        

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
                      discount_code,lasers, moving_head_ct, co2_cannon, cold_spark_ct, projector, confetti_cannon, venue):
    try:
        # Convert boolean radio button responses to True/False
        pa_system = pa_system == 'Yes';
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
        projector = projector == 'Yes'
        confetti_cannon = confetti_cannon == 'Yes'
        lasers = lasers == 'Yes'
        co2_cannon = co2_cannon == 'Yes'
        microphone = microphone == 'Yes'
        # Set empty string inputs to None
        best_time = best_time if best_time else None
        start_time = start_time if start_time else None
        estimated_budget = estimated_budget if estimated_budget else None
        event_location = event_location if event_location else None
        venue = venue if venue else None
        booth_location = booth_location if booth_location else None
        comments = comments if comments else None
        created_by = created_by if created_by else None

        # Create the SQL function call using SQLAlchemy text()
        query = text("SELECT * FROM f_client_quote(:first_name, :last_name, :phone_number, :email, " +
                     ":best_time, :event_date, :start_time, " +
                     ":estimated_budget, :event_type, :event_location, :guest_count, :pa_system, " +
                     ":dancing_lights, :disco_ball, :uplighting, :fog_machine, " +
                     ":low_fog_machine, :photo_booth, :photo_booth_prints, :booth_location, " +
                     ":comments, :created_by, :uplight_ct, :backdrop_props, :back_drop_type, " +
                     ":service_hours, :service_types, :cold_sparks, :microphone, :monogram, :discount_code, " +
                     ":lasers, :moving_head_ct,:co2_cannon,:cold_spark_ct, :projector, :confetti_cannon, :venue)")

        # Execute the function with the parameters as named arguments

        with conn.begin() as transaction:  # Start a transaction block
            try:
                result = conn.execute(query, {
                    "first_name": first_name, "last_name": last_name, "phone_number": phone_number, "email": email,
                    "best_time": best_time, "event_date": event_date, "start_time": start_time,
                    "estimated_budget": estimated_budget, "event_type": event_type, "event_location": event_location,
                    "guest_count": guest_count, "pa_system": pa_system, "dancing_lights": dancing_lights, "disco_ball": disco_ball,
                    "uplighting": uplighting, "fog_machine": fog_machine, "low_fog_machine": low_fog_machine, "photo_booth": photo_booth,
                    "photo_booth_prints": photo_booth_prints, "booth_location": booth_location, "comments": comments,
                    "created_by": created_by, "uplight_ct": uplight_ct, "backdrop_props": backdrop_props,
                    "back_drop_type": back_drop_type, "service_hours": service_hours, "service_types": service_types, "cold_sparks": cold_sparks, "microphone": microphone,
                    "monogram": monogram, "discount_code": discount_code, "lasers": lasers, "moving_head_ct": moving_head_ct, "co2_cannon": co2_cannon, "cold_spark_ct": cold_spark_ct, 
                    "projector": projector, "confetti_cannon": confetti_cannon
                })
                row = result.fetchone()
                if row:
                    savings = row[0]
                    total = row[1]
                    return savings, total
                else:
                    return None, None

                #conn.close()

            except Exception as e:
                transaction.rollback()  # Rollback the transaction if an error occurs
                raise e
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")


def execute_procedure_update(booking_id, event_status, first_name, last_name, phone_number, email, best_time, event_date, start_time,
                      estimated_budget, event_type, event_location, guest_count, pa_system, dancing_lights, disco_ball,
                      uplighting, fog_machine, low_fog_machine, photo_booth, photo_booth_prints, booth_location,
                      comments, created_by, uplight_ct, backdrop_props, back_drop_type, service_hours, service_types, cold_sparks, microphone, monogram, 
                      price_override, discount_code,lasers, moving_head_ct, co2_cannon, cold_spark_ct, projector,confetti_cannon, venue):
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

        lasers = lasers == 'Yes'
        co2_cannon = co2_cannon == 'Yes' 
        projector = projector == 'Yes'
        confetti_cannon = confetti_cannon == 'Yes'
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
                     ":service_hours, :service_types, :cold_sparks, :microphone, :monogram, :price_override, :discount_code," +
                     ":lasers, :moving_head_ct, :co2_cannon, :cold_spark_ct, :projector, :confetti_cannon, :venue)")

        # Execute the procedure with the parameters as named arguments
 
        with conn.begin() as transaction:
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
                    "price_override": price_override, "discount_code": discount_code, 
                    "lasers":lasers, "moving_head_ct": moving_head_ct, "co2_cannon":co2_cannon, "cold_spark_ct": cold_spark_ct, "projector": projector, "confetti_cannon": confetti_cannon, "venue":venue
                })
 
                #conn.close()
                
            except Exception as e:
                transaction.rollback()  # Rollback if there's an error
                raise e
        st.success('Your event has been updated', icon="✅")
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
 # Ensure the connection is closed
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
                        "Select a quote",
                        ('New', 'Your Bookings'),
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
                    event_type = st.selectbox("Event Type?*", ("","Wedding", "Birthday", "Anniversary", "Corporate Function", "Engagement", "Club", "Concert", "Fundraiser","Other"))
                    best_time = st.time_input("Best Time to Contact", None)
                    if best_time:
                        st.write(f"Central Time: {best_time.strftime('%I:%M %p')}")
                    service_hours = st.slider('Number of hours professional needed', 2, 24, value=2)
                    start_time = st.time_input("Estimated Start Time*", None) #Start
                    if start_time:
                        st.write(f"Central Time: {start_time.strftime('%I:%M %p')}")
                    estimated_budget = st.number_input("Budget Amount", 0) #Budget
                    event_location = st.text_input("Venue Location", "") #Location
                    venue = st.text_input("Venue", "")
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
                    moving_head_ct = st.slider('How many moving heads do you need?', 0, 4, value=0)
                    disco_ball = st.radio(
                        "Do you need a disco ball?",
                        ('Yes', 'No'),
                        index=1)
                    #uplighting = "No"
                    # uplighting = st.radio(
                    #     "Do you need uplighting?",
                    #     ('Yes', 'No'),
                    #     index=1)
                    uplight_ct = st.slider('How many uplights do you need?', 0, 20, value=0)
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
                    cold_spark_ct = st.slider('How many cold sparks do you need?', 0, 6, value=0)
                    projector = st.radio(
                        "Do you need a projector?",
                        ('Yes', 'No'),
                        index=1
                                            )
                    confetti_cannon = st.radio(
                        "Do you need a confetti cannon?",
                        ('Yes', 'No'),
                        index=1
                                            )
                    lasers = st.radio(
                        "Do you need lasers?",
                        ('Yes', 'No'),
                        index=1
                                            )
                    co2_cannon = st.radio(
                        "Do you need a CO2 Cannon?",
                        ('Yes', 'No'),
                        index=1
                    )

                    photo_booth = st.selectbox(
                            "Select a photo booth",
                            ("", "DSLR Photo Booth", "IPad Photo Booth"),
                            index=0,
                            placeholder=""
                        )
            
                    photo_booth_prints = st.radio(
                            "Do you need photo prints?",
                            ('Yes', 'No'),
                            index=1
                        )
        
                    back_drop_type = st.selectbox(
                            "Select a backdrop",
                            ("", "White Backdrop", "Shimmering Black Backdrop"),
                            index=0,
                            placeholder=""
                        )
                    backdrop_props = st.radio(
                            "Do you need photo booth props?",
                            ('Yes', 'No'),
                            index=1
                        )
                    comments = st.text_area("Additional comments", "")   
                    created_by = ""

                    # Submit button
                    submitted = st.form_submit_button("Submit")

                    if submitted:
                        try:
                            # Check if all required fields are filled
                            st.session_state["my_input"] = first_name

                            if email and phone_number and first_name and event_date and service_hours and event_type:
                                # Attempt to execute the function and get the quote price
                                savings, total = execute_procedure(
                                    first_name, last_name, phone_number, email, best_time, event_date, start_time,
                                    estimated_budget, event_type, event_location, guest_count, pa_system, dancing_lights, disco_ball,
                                    uplighting, fog_machine, low_fog_machine, photo_booth, photo_booth_prints, booth_location,
                                    comments, created_by, uplight_ct, backdrop_props, back_drop_type, service_hours, service_types,
                                    cold_sparks, microphone, monogram, discount_code,lasers,moving_head_ct, co2_cannon,cold_spark_ct, projector,confetti_cannon, venue
                                )
                                if savings is not None and total is not None:
                                    #st.success("Your quote has been submitted successfully!")
                                    st.write(f"Total Savings: ${savings:.2f}")
                                    st.write(f"Grand Total: ${total:.2f}")
                                    st.write("If you want to review the itemization of costs and savings, scroll to the top of the form and select 'Your Bookings'.")

                                    # Prepare form data for PDF
                                    form_data = {
                                        'service_types': service_types,
                                        'first_name': first_name,
                                        'last_name': last_name,
                                        'phone_number': phone_number,
                                        'email': email,
                                        'discount_code': discount_code,
                                        'event_date': event_date,
                                        'event_type': event_type,
                                        'best_time': best_time,
                                        'service_hours': service_hours,
                                        'start_time': start_time,
                                        'estimated_budget': estimated_budget,
                                        'event_location': event_location,
                                        'guest_count': guest_count,
                                        'pa_system': pa_system,
                                        'microphone': microphone,
                                        'dancing_lights': dancing_lights,
                                        'disco_ball': disco_ball,
                                        'uplighting': uplighting,
                                        'uplight_ct': uplight_ct,
                                        'fog_machine': fog_machine,
                                        'low_fog_machine': low_fog_machine,
                                        'monogram': monogram,
                                        'cold_sparks': cold_sparks,
                                        'photo_booth': photo_booth,
                                        'photo_booth_prints': photo_booth_prints,
                                        'back_drop_type': back_drop_type,
                                        'backdrop_props': backdrop_props,
                                        'comments': comments,
                                        'lasers': lasers,
                                        'moving_head_ct': moving_head_ct,
                                        'co2_cannon': co2_cannon,
                                        'cold_spark_ct': cold_spark_ct,
                                        'projector': projector,
                                        'confetti_cannon': confetti_cannon,
                                        'venue': venue
                                    }
                                    st.session_state['pdf_data'] = form_data
                                    st.session_state['show_links'] = True
                                else:
                                    st.write("If you want to review the itemization of costs and savings, scroll to the top of the form and select 'Your Bookings'.")
                            else:
                                # Display an error if required fields are missing
                                st.error("Please fill in all required fields: Name, Phone, Email, Event Date, Service Hours, and Event Type.")
                        except Exception as e:
                            # Handle any unexpected errors
                            st.error(f"An error occurred while submitting your quote: {e}")
                    
                
        
        

            elif option == "Your Bookings":
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

        

                            if not df.empty:
                                st.subheader("Event Estimate:")
                                st.warning("We are ready to match or beat any offer—reach out to us today!")

                                # Ensure the first column remains as a string
                                first_column = df.iloc[:, 0]  # Extract the first column

                                # Convert the rest of the columns to numeric and round them to two decimal places
                                numeric_columns = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce').round(2)

                                # Recombine the first column and numeric columns
                                updated_df = pd.concat([first_column, numeric_columns], axis=1)

                                # Apply styles: Bold header and first column
                                styled_df = updated_df.style.format("{:.2f}", subset=updated_df.columns[1:]).set_table_styles([
                                    {'selector': 'th', 'props': [('font-weight', 'bold')]},  # Bold headers
                                    {'selector': 'td:first-child', 'props': [('font-weight', 'bold')]}  # Bold the first column
                                ])

                                # Display the styled DataFrame
                                st.dataframe(styled_df)

                                              
        
                            else:
                                    st.write("No data was returned for the given query.")
                                    

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
                                discount_code,
                                event_date_ct,
                                venue,
                                co2_cannon, 
                                lasers, 
                                confetti_cannon, 
                                projector, 
                                cold_spark_ct,
                                moving_head_ct
                                FROM f_get_booking_details('{booking}')
                                """

                            df = run_query(query)
        
                            df = df.applymap(lambda x: 0 if x is True else 1 if x is False else x)
                            default_service_types = df['service_types'][0]
                            billing_status = df['billing_status'][0]
                            payment_due_date = df['payment_due_date'][0]
                            actual_cost = df['actual_cost'][0]
                            event_date_ct = df['event_date_ct'][0]

                            # Prepare booking data for contract PDF
                            if not contract_df.empty:
                                booking_data = {
                                    'dj_name': contract_df['professional'][0] or 'Tay Nguyen',
                                    'client_name': f"{contract_df['first_name'][0] or ''} {contract_df['last_name'][0] or ''}".strip() or 'Client Name',
                                    'contract_date': contract_df['today'][0].strftime('%m/%d/%Y') if contract_df['today'][0] and isinstance(contract_df['today'][0], datetime) else datetime.now().strftime('%m/%d/%Y'),
                                    'event_date': contract_df['event_date'][0].strftime('%m/%d/%Y') if contract_df['event_date'][0] and isinstance(contract_df['event_date'][0], datetime) else 'Not provided',
                                    'start_time': contract_df['start_time'][0].strftime('%I:%M %p') if contract_df['start_time'][0] and hasattr(contract_df['start_time'][0], 'strftime') else 'Not provided',
                                    'end_time': contract_df['end_time'][0].strftime('%I:%M %p') if contract_df['end_time'][0] and hasattr(contract_df['end_time'][0], 'strftime') else 'Not provided',
                                    'venue': contract_df['venue'][0] or 'Not provided',
                                    'event_location': contract_df['event_location'][0] or 'Not provided',
                                    'total_fee': f"{contract_df['grand_total'][0]:.2f}" if contract_df['grand_total'][0] else '0.00',
                                    'deposit': '60.00',
                                    'event_type': contract_df['event_type'][0] or 'Not provided',
                                    'equipment_list': contract_df['products'][0] or 'MC/DJ performance\nPremium PA Sound System\nWireless Microphones\nComplimentary Dance Lights'
                                }
                            else:
                                booking_data = {
                                    'dj_name': 'Tay Nguyen',
                                    'client_name': 'Client Name',
                                    'contract_date': datetime.now().strftime('%m/%d/%Y'),
                                    'event_date': 'Not provided',
                                    'start_time': 'Not provided',
                                    'end_time': 'Not provided',
                                    'event_location': 'Not provided',
                                    'total_fee': '0.00',
                                    'deposit': '60.00',
                                    'event_type': 'Not provided',
                                    'equipment_list': 'MC/DJ performance\nPremium PA Sound System\nWireless Microphones\nDance Lights'
                                }

                            # Generate contract PDF and add download button only if status is Scheduled
                            if df['event_status'][0] == 'Scheduled':
                                generator = PDFGenerator()
                                contract_pdf_bytes = generator.generate_dj_contract_pdf(booking_data)

                                # Add download button for contract
                                last_name = contract_df['last_name'][0] if not contract_df.empty and contract_df['last_name'][0] else 'Unknown'
                                booking_id = contract_df['booking_id'][0] if not contract_df.empty and contract_df['booking_id'][0] else 'Unknown'
                                file_name = f"dj_contract_{last_name}_{booking_id}.pdf"
                                st.download_button(
                                    label="Download Booking Contract",
                                    data=contract_pdf_bytes,
                                    file_name=file_name,
                                    mime="application/pdf",
                                    key="contract_pdf_download_bookings"
                                )
 
                     
                            price_override2 = df['price_override'][0]
                            back_drop_needed = 1 if not df['back_drop_type'][0] else 0
                            booking_id = booking
                        
 
 

                                ############################################
                            if event_date_ct > 1:
                                 st.warning("This date has several bookings. Kindly reach out to us to confirm availability.")   
                   

                            if df['event_status'][0] != 'Scheduled' or email == "5003":
                                    
                                    with st.form("my_form"):
                                        st.subheader("Booking# " + str(booking_id))

                                        if event_date_ct > 1:
                                            event_status = st.selectbox("Booking Status", ("Conflict","Canceled"))  
                                        elif email == "5003":
                                            event_status = st.selectbox("Booking Status", (df['event_status'][0], "Ongoing","Canceled","Scheduled","Proposal")) 
                                        else:
                                            event_status = st.selectbox("Booking Status", (df['event_status'][0],"Ongoing","Canceled")) 

                                        service_types = st.multiselect(
                                            "Service Type?*",
                                            options=["", "DJ", "MC", "Karaoke"],
                                            default=default_service_types
                                        )
                                        # Default value for price_override
                                        price_override = df['price_override'][0]

                                        # Conditional assignment if email matches "5003"
                                        if email == "5003":
                                            price_override = st.text_input("Override Price", df['price_override'][0])
 
                                        discount_code  = st.text_input("Discount Code", df['discount_code'][0]) 
                                        first_name = st.text_input("First Name*", df['first_name'][0])  #FirstName
                                        last_name = st.text_input("Last Name*", df['last_name'][0]) #LastName
                                        phone_number = st.text_input("Phone Number*", df['phone_number'][0]) #Phone
                                        email = st.text_input("Email Address*", df['email'][0]) #Email
                                        event_date = st.date_input("Event Date*", df['event_date'][0]) 
                                        event_type = st.selectbox("Event Type?*", (df['event_type'][0],"Wedding", "Birthday", "Anniversary", "Corporate Function", "Engagement", "Club", "Concert", "Fundraiser","Graduation","Other"))
                                        best_time = st.time_input("Best Time to Contact", df['best_time'][0])
                                        if best_time:
                                            st.write(f"Central Time: {best_time.strftime('%I:%M %p')}")
                                        service_hours = st.slider('Number of hours professional needed', 2, 24, value=df['service_hours'][0])
                                        start_time = st.time_input("Estimated Start Time*", df['start_time'][0]) #Start
                                        if start_time:
                                            st.write(f"Central Time: {start_time.strftime('%I:%M %p')}")
                                        estimated_budget = st.number_input("Budget Amount", df['estimated_budget'][0]) #Budget

                                        venue = st.text_input("Venue", df['venue'][0]) #Location


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
                                        dancing_lights = st.radio(
                                            "Do you need dance lights?",
                                            ('Yes', 'No'),
                                            index=int(df['dancing_lights'][0]))
                                        moving_head_ct = st.slider('How many moving heads do you need?', 0, 4, value=df['moving_head_ct'][0])
                                        cold_sparks = st.radio(
                                            "Do you need cold sparks?",
                                            ('Yes', 'No'),
                                            index=int(df['cold_sparks'][0]))
                                        cold_spark_ct = st.slider('How many cold sparks do you need?', 0, 6, value=0)
                                        disco_ball = st.radio(
                                            "Do you need a disco ball?",
                                            ('Yes', 'No'),
                                            index=int(df['disco_ball'][0])
                                            )
                                        projector = st.radio(
                                                "Do you need a projector?",
                                                ('Yes', 'No'),
                                                index=1
                                            )
                                        confetti_cannon = st.radio(
                                                "Do you need a confetti cannon?",
                                                ('Yes', 'No'),
                                                index=1
                                            )
                                        lasers = st.radio(
                                                "Do you need lasers?",
                                                ('Yes', 'No'),
                                                index=1
                                            )
                                        co2_cannon = st.radio(
                                            "Do you need a CO2 Cannon?",
                                            ('Yes', 'No'),
                                            index=1
                                        )

                                        uplighting = "No"
                                        uplight_ct = st.slider('How many uplights do you need?', 0, 20, value=df['uplight_ct'][0])
                                        fog_machine = st.radio(
                                            "Do you need a fog machine?",
                                            ('Yes', 'No'),
                                            index=int(df['fog_machine'][0]))
                                        low_fog_machine = st.radio(
                                            "Do you want dancing on the clouds?",
                                            ('Yes', 'No'),
                                            index=int(df['low_fog_machine'][0]))
                                        monogram = st.radio(
                                            "Do you want a projecting monogram?",
                                            ('Yes', 'No'),
                                            index=int(df['monogram'][0]))
                                        photo_booth = st.selectbox(
                                                    "Select a photo booth",
                                                    (str(df['photo_booth'][0]), "", "DSLR Photo Booth", "IPad Photo Booth"),
                                                    index=0
                                                )
                                        photo_booth_prints = st.radio(
                                                "Do you need photo prints?",
                                                ('Yes', 'No'),
                                                index=int(df['photo_booth_prints'][0])
                                            )
                                        back_drop_type = st.selectbox(
                                            "Select a backdrop",
                                            (str(df['back_drop_type'][0]), "", "White Backdrop", "Shimmering Black Backdrop"),
                                            index=0
                                        )

                                        backdrop_props = st.radio(
                                                "Do you need photo booth props?",
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

                                            if email and phone_number and first_name and event_date and service_hours and event_type:
                                                    booking_id = next(iter(booking_id)) if isinstance(booking_id, set) else booking_id
                                                    execute_procedure_update(booking_id, event_status, first_name, last_name, phone_number, email, best_time, event_date, start_time,
                                                                            estimated_budget, event_type, event_location, guest_count, pa_system, dancing_lights, disco_ball, uplighting,
                                                                            fog_machine, low_fog_machine, photo_booth, photo_booth_prints, booth_location, comments, created_by, uplight_ct,
                                                                            backdrop_props, back_drop_type,  service_hours, service_types, cold_sparks, microphone, monogram, price_override, discount_code,
                                                                            lasers, moving_head_ct, co2_cannon, cold_spark_ct, projector,confetti_cannon, venue)
                                                    # , event_date_ct integer, projector boolean, confetti_cannon boolean, lasers boolean, co2_cannon boolean, venue text)

                                                    # Prepare form data for PDF after successful update
                                                    form_data = {
                                                        'service_types': service_types,
                                                        'first_name': first_name,
                                                        'last_name': last_name,
                                                        'phone_number': phone_number,
                                                        'email': email,
                                                        'discount_code': discount_code,
                                                        'event_date': event_date,
                                                        'event_type': event_type,
                                                        'best_time': best_time,
                                                        'service_hours': service_hours,

                                                        'projector': projector,
                                                        'venue': venue,
                                                        'co2_cannon': co2_cannon,
                                                        'moving_head_ct': moving_head_ct,
                                                        'lasers': lasers,
                                                        'confetti_cannon': confetti_cannon,
                                                        'cold_spark_ct': cold_spark_ct,

                                                        'start_time': start_time,
                                                        'estimated_budget': estimated_budget,
                                                        'event_location': event_location,
                                                        'guest_count': guest_count,
                                                        'pa_system': pa_system,
                                                        'microphone': microphone,
                                                        'dancing_lights': dancing_lights,
                                                        'disco_ball': disco_ball,
                                                        'uplighting': uplighting,
                                                        'uplight_ct': uplight_ct,
                                                        'fog_machine': fog_machine,
                                                        'low_fog_machine': low_fog_machine,
                                                        'monogram': monogram,
                                                        'cold_sparks': cold_sparks,
                                                        'photo_booth': photo_booth,
                                                        'photo_booth_prints': photo_booth_prints,
                                                        'back_drop_type': back_drop_type,
                                                        'backdrop_props': backdrop_props,
                                                        'comments': comments
                                                    }
                                                    st.session_state['pdf_data'] = form_data
                                                    st.session_state['show_links'] = True
                                            else:
                                                    st.error("Please fill in all required fields (Name, Phone, Email, Event Date, Service Hours, Event Type).")
        

        

        if __name__ == "__main__":
            main()

        # Display links after successful submission or update
        if 'show_links' in st.session_state and st.session_state['show_links']:
            st.write("[Pay the deposit to lock in your date](https://buy.stripe.com/cN29BFc2F7gqgBGdQQ)")
        