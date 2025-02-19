import streamlit as st  
import io
from PIL import Image
import base64
import pandas as pd
import mysql.connector
#from st_aggrid import AgGrid, GridOptionsBuilder
#import psycopg2

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

################################################## Email Form ############################################################################    
# Uses st.cache_resource to only run once.
# @st.cache_resource
# def init_connection():

#     return psycopg2.connect(**st.secrets["postgres"])

# conn = init_connection()
#@st.experimental_singleton
#def init_connection():
#    return mysql.connector.connect(**st.secrets["postgres"])

#conn = init_connection()
conn = st.connection("postgresql", type="sql")
#conn = st.experimental_connection('tcn_ent', type='sql')

# Function to execute the stored procedure
def execute_procedure(email, song, artist, first_name):
    with conn.cursor() as cur:
        try:
            cur.execute("CALL sp_song_request(%s, %s, %s, %s);", (email, song, artist, first_name))
            conn.commit()
            st.success("Your song is added successfully! (It may take a few mins to show up in the queue)")
        except Exception as e:
            conn.rollback()
            st.error(f"Error: {e}")


# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

 

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
query = "select  s.Song_Order, c.first_name  as Request_By, s.song_name as Song_Name , s.artist_name as Artist_Name from song_requests s left join clients c on c.client_id = s.created_by order by s.song_order"
rows = run_query(query)

# Convert the query results to a pandas DataFrame
data = pd.DataFrame(rows, columns=['Song_Order', 'Request_By', 'Song_Name', 'Artist_Name'])

#Display the results in a DataGrid
# st.subheader("Song Queue List")
# if data.empty:
#     st.write("Currently No Song Request")
# else:
#     gb = GridOptionsBuilder.from_dataframe(data)
#     gb.configure_pagination(paginationAutoPageSize=True)
#     gridOptions = gb.build()
#     AgGrid(data, gridOptions=gridOptions, height=200, width='100%')


 
