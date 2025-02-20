import streamlit as st  
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import base64
from PIL import Image

################################################## SET PAGE ############################################################################  
st.set_page_config(
    page_title="Song Requests",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# Make your dream a reality!"
    }
)

# Use local CSS
with open("pages/style/style.css") as source_style:
    st.markdown(f"<style>{source_style.read()}</style>", unsafe_allow_html=True)

st.image("pages/images/song_request.png", width=1750)  

# Inject CSS for background color
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Load the images
youtube_img = base64.b64encode(open("pages/images/youtube.png", "rb").read()).decode()
instagram_img = base64.b64encode(open("pages/images/instagram.png", "rb").read()).decode()

# Create columns in the sidebar with less spacing
col1, col2, col3, col4, col5, col6 = st.sidebar.columns([1, 1, 1, 1, 1, 1])

with col1:
    st.markdown(
        f"""<a href="https://www.youtube.com/@djtayzer">
        <img src="data:image/png;base64,{youtube_img}" width="30">
        </a>""",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""<a href="https://www.instagram.com/tayzer/">
        <img src="data:image/png;base64,{instagram_img}" width="30">
        </a>""",
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

# Function to execute the stored procedure
def execute_procedure(email, song, artist, first_name):
    try:
        # Create the SQL procedure call using SQLAlchemy text()
        query = text("CALL sp_song_request(:email, :song, :artist, :first_name)")

        # Execute the procedure with the parameters as named arguments
        with conn.begin():  # Start a transaction block
            conn.execute(query, {"email": email, "song": song, "artist": artist, "first_name": first_name})

        # Show success message
        st.success("Your song is added successfully! (It may take a few mins to show up in the queue)")

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
    return pd.DataFrame(rows, columns=columns)


# Input fields
st.subheader("Song Request Form")
my_email_address = st.text_input("Email Address*", "")  # Email
my_first_name = st.text_input("First Name", "")  # First
my_song = st.text_input("Song Name*", "")  # Song
my_artist = st.text_input("Artist Name*", "")  # Artist

# Submit button
if st.button("Submit"):
    # Check if all required fields are filled
    if my_email_address and my_song and my_artist:
        execute_procedure(my_email_address, my_song, my_artist, my_first_name)
    else:
        st.error("Please fill in all required fields.")

# Run the query to fetch song requests
query = """
    SELECT s.Song_Order, c.first_name AS Request_By, s.song_name AS Song_Name, s.artist_name AS Artist_Name
    FROM song_requests s
    LEFT JOIN clients c ON c.client_id = s.created_by
    where s.deleted_at is null
    ORDER BY s.song_order
"""
rows = run_query(query)

# Display the results
st.subheader("Song Queue List")
if rows.empty:
    st.write("Currently No Song Request")
else:
    st.write(rows)
 
