import streamlit as st
import base64
import streamlit.components.v1 as components
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import os
# Page Tab
st.set_page_config(
    page_title="Home",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",  #expanded
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
 
# Background for page
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


# Load database credentials from Streamlit secrets
db_config = st.secrets["postgres"]

#Create the SQLAlchemy engine using connection string format
def init_connection():
    connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    engine = create_engine(connection_string)
    return engine.connect()

conn = init_connection()

 

@st.cache_data(ttl=10)
 #Ensure the connection is closed
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


# Initialize the current index in session state
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

# List that contains paths to images or YouTube video links
media_paths = [
    "https://www.youtube.com/watch?v=baTq72zAc-U",  # Example YouTube video link
    "pages/images/featured_pro.png",
    "pages/images/reception.jpg",
    "pages/images/kids.jpg",
    "pages/images/work_fund.png",
    "pages/images/work_karaoke.png",
    "pages/images/work_night.jpg",
    "pages/images/work_siepe.jpg"
]

# Adjust the column width ratios: column 2 is 5 times larger than columns 1 and 3
col1, col2, col3 = st.columns([1, 10, 1])  # Relative column widths

# Display the main media (image or video) in the larger column (column 2)
with col2:
    current_media = media_paths[st.session_state.current_index]
    if current_media.endswith((".jpg", ".png", ".jpeg", ".gif")):  # Check for image extensions
        st.image(current_media, width=1750)
    elif "youtube.com" in current_media or "youtu.be" in current_media:  # Check for YouTube links
        st.video(current_media)

# Style for larger buttons
button_style = """
    <style>
        .button {
            font-size: 30px;
            font-family: Arial, sans-serif; /* Change font type to Arial */
            font-weight: bold;      /* Make the font bold */
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background-color: #f1ecec;
            cursor: pointer;
        }
        .button:hover {
            background-color: #ddd;
        }
    </style>
"""
st.markdown(button_style, unsafe_allow_html=True)


coll1, coll2, coll3, coll4 = st.columns([10, 1, 1, 10])  # Relative column widths

 # Previous button in column 1
with coll2:
    if st.button("⬅️", key="previous", use_container_width=True):
        st.session_state.current_index = (st.session_state.current_index - 1) % len(media_paths)
 

# Next button in column 3
with coll3:
    if st.button("➡️", key="next", use_container_width=True):
        st.session_state.current_index = (st.session_state.current_index + 1) % len(media_paths)
 

######################################################################################
# ---- HEADER SECTION ----
with st.container():
    st.title("Overview")
    st.write(
        """Welcome to TCN Entertainment, where the beats meet the streets and the fun never skips a track! I am your ultimate DJ professional with the top-tier sound and lighting. 
        I'm here to turn your event into an epic celebration that'll have everyone talking long after the music fades. 
        But I'm more than just a DJ, I will work closely with you to understand your vision, preferences, and must-play tracks. 
        I'm here to listen, collaborate, and bring your party dreams to life, one beat drop at a time. So, if you're ready to take 
        your event to the next level, let me help you and be your soundtrack to success!"""
    )
    st.write("---")
    st.subheader("Exceptional DJ Services for Unforgettable Events")
    st.write(
        """As a dedicated and professional DJ based in Dallas, TX, I specialize in delivering the perfect soundtrack to bring every celebration to life. Whether you're planning a once-in-a-lifetime wedding, a private party, a corporate event, or any other special occasion, I create customized playlists that match your vision and keep your guests engaged from start to finish. Here's a closer look at the services I offer:"""
    )
    st.subheader("Weddings")
    st.write("""Your wedding day should be as unique as your love story, and the right music can make every moment unforgettable. With expertise in setting the perfect tone, I ensure the soundtrack flows seamlessly—from your grand entrance to the final dance. I know how to read the crowd, adapt to the energy in the room, and create an atmosphere filled with magic and joy.""")
    st.subheader("Private Parties")
    st.write("""From milestone birthdays to intimate anniversary celebrations, your private party deserves a personal touch. I work closely with you to design a playlist that matches the vibe of your event, whether it’s a high-energy dance party or a relaxed gathering with family and friends. Together, we'll create a musical experience that keeps your guests entertained all night long.""")
    st.subheader("Corporate Events")
    st.write("""Professional events call for an expert approach to music. Whether it's a networking event, holiday party, or company celebration, I balance sophistication and entertainment to ensure your gathering is both enjoyable and memorable. I’ll work with you to set the perfect tone, ensuring your event runs smoothly and leaves a lasting impression.""")
    st.subheader("School Dances")
    st.write("""When it comes to school events like prom or homecoming, it's all about bringing the energy! I craft age-appropriate playlists that keep students on their feet and create an electric atmosphere. From slow dances to chart-topping hits, I’ll make sure the night is unforgettable for everyone.""")
    st.subheader("Fundraisers")
    st.write("""Fundraising events thrive on an inviting and upbeat atmosphere. With music that energizes your guests and complements your cause, I help create a positive environment that encourages participation and generosity. Together, we’ll make your fundraiser a success.""")
    st.subheader("Bar and Bat Mitzvahs")
    st.write("""Milestone events like bar and bat mitzvahs deserve the perfect blend of tradition and celebration. I specialize in creating playlists that honor the cultural significance of the day while bringing energy and excitement to the dance floor. Let's make it a day to remember for everyone involved.""")
    st.subheader("Personalized DJ Services for Any Occasion")
    st.write("""Every event is unique, and I'm committed to bringing your vision to life. Whether you're planning an elegant wedding, a spirited private party, or a milestone celebration, I tailor my services to suit your needs. With a keen ability to read the room and curate the perfect playlist, I’ll ensure your guests are entertained from the first note to the last.
        Let’s make your event extraordinary. Together, we'll create an unforgettable experience filled with great music, good vibes, and lasting memories.""")
    st.write("[Get a Quote>](Request_Quote)")  



# Sumamry Section
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Services")
        st.write(
            """
 
            Music Genres

            - Top 40 / Pop
            - EDM / House / Techno
            - Hip-Hop / R&B / Afrobeats
            - Classic Rock / 80s / 90s Hits
            - Latin / Reggaeton
            - Jazz / Chillout
            - Custom Playlist Creation

            Event Services

            - Event Coordination with Venue & Planner
            - On-Site Setup & Breakdown
            - Full Sound & Lighting Packages
            - Visual Effects (LED, Projection Mapping)
            - Live Remixing & Mashups
            - Karaoke Setup

            Additional Features

            - Photo Booth Rentals (DSLR, IPAD)
            - Custom Music Production
            - Virtual/Live Streaming DJ Sets
            - Wireless Microphones & PA Systems
            - Interactive Crowd Engagement (Games, Requests)

            """
        )
        st.write("[Learn More >](Services)")

# # Sumamry Section
# with st.container():
#     st.write("---")
#     left_column, right_column = st.columns(2)
#     with left_column:
#         st.header("Live Song Requests")
#         st.write("##")
#         st.write(
#             """
#             We want to make sure your event has the perfect soundtrack! Our song request form allows you to share your favorite tunes, and let us know any specific songs or genres you'd like to hear. Whether you have a list of must-play tracks or just want to guide us with a vibe, we’ve got you covered. Fill out the form below to submit your requests, and we'll make sure to incorporate them into the mix to keep the party going all night long!
#             """
#         )
#         st.write("[Learn More >](/Song_Requests)")
 
# ---- SONG REQUESTS SECTION ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns([2, 1])
    with left_column:
        st.markdown('<div class="section-title">📝 Live Song Requests</div>', unsafe_allow_html=True)
        st.write(
            "Share your favorite songs and genres! Fill out our request form and we'll keep the party going all night long."
        )
        st.markdown('<a href="/Song_Requests" style="font-weight:700;color:#e63946;">Request a Song &gt;</a>', unsafe_allow_html=True)
    with right_column:
        st.image("pages/images/work_karaoke.png", caption="Your playlist. Your party.", use_column_width=True)

# ---- REVIEWS SECTION ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns([2, 1])
    with left_column:
        st.markdown('<div class="section-title">🌟 Reviews</div>', unsafe_allow_html=True)
        st.write("See what clients are saying about TCN Entertainment!")
        st.markdown(
            """
            <a href="https://www.gigsalad.com/tcn_entertainment_dallas" target="_blank">
                <img src="https://cress.gigsalad.com/images/svg/standalone/promokit-links/top-performer/top-performer--blue.svg" height="64">
            </a>
            <a href="https://www.gigsalad.com/tcn_entertainment_dallas" target="_blank">
                <img src="https://cress.gigsalad.com/images/svg/standalone/promokit-links/read-reviews/read-reviews--dark.svg" height="40">
            </a>
            """,
            unsafe_allow_html=True
        )
    with right_column:
        st.image("pages/images/reception.jpg", caption="Real events. Real memories.", use_column_width=True)



# # Sumamry Section
# with st.container():
#     st.write("---")
#     left_column, right_column = st.columns(2)
#     with left_column:
#         st.header("Reviews")
#         st.write("##")
    

# html_content2 = """
# <div style="display: flex; align-items: center;">
#     <a href="https://www.gigsalad.com/tcn_entertainment_dallas" style="margin-right: 20px;">
#         <img src="https://cress.gigsalad.com/images/svg/standalone/promokit-links/top-performer/top-performer--blue.svg" alt="Top Performer on GigSalad" height="128" width="116">
#     </a>
#     <a href="https://www.gigsalad.com/tcn_entertainment_dallas">
#         <img src="https://cress.gigsalad.com/images/svg/standalone/promokit-links/read-reviews/read-reviews--dark.svg" alt="Read My Reviews on GigSalad" height="100" width="300">
#     </a>
# </div>
# """

# # Display the HTML content
# #components.html(html_content2, height=150)

# # HTML content
# html_content = """
# <div id="gigsalad-reviews-widget"></div><script>var gsReviewWidget;(function(d,t){var s=d.createElement(t),options={path:'254761',maxWidth:600,count:4};s.src='https://www.gigsalad.com/js/gigsalad-reviews-widget.min.js';s.onload=s.onreadystatechange=function(){var rs=this.readyState;if(rs)if(rs!='complete')if(rs!='loaded')return;try{gsReviewWidget=new GsReviewsWidget(options);gsReviewWidget.display();}catch(e){}};var scr=d.getElementsByTagName(t)[0];var par=scr.parentNode;par.insertBefore(s,scr);})(document,'script');</script>
# """

# # Display the HTML content
# components.html(html_content, height=900)
# st.write("[Get an instant quote>](Request_Quote)")

# ---- UPCOMING EVENTS SECTION ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns([2, 1])
    with left_column:
        st.markdown(
            """
            <style>
            .section-title {
                font-size: 1.5em;
                font-weight: 700;
                color: #457b9d;
                margin-top: 1.2em;
                margin-bottom: 0.5em;
            }
            .event-card {
                background: linear-gradient(90deg, #f8fafc 70%, #e63946 100%);
                border-radius: 10px;
                padding: 0.7em 1.2em;
                margin-bottom: 0.7em;
                box-shadow: 0 2px 12px rgba(230,57,70,0.08);
                font-size: 1.1em;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown('<div class="section-title">📅 Upcoming Events</div>', unsafe_allow_html=True)
        query = """
            select event_date::date  as event_date
            , a.event_name 
            , a.event_status
            from events a
            where event_status in ('Scheduled','Ongoing')
            and a.deleted_at is null 
            and event_date >= now()::date
            order by event_date 
        """
        df = run_query(query)
        if not df.empty:
            for index, row in df.iterrows():
                st.markdown(
                    f"<div class='event-card'><b>{row['event_date']}</b> &mdash; <span style='color:#e63946;'>{row['event_status']}</span> &mdash; {row['event_name']}</div>",
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                "<div class='event-card'>No scheduled events found.</div>",
                unsafe_allow_html=True
            )
    # with right_column:
    #     st.image("pages/images/work_fund.png", caption="See you on the dance floor!", use_column_width=True)

# ---- CALL TO ACTION ----
with st.container():
    st.write("---")
    st.markdown(
        """
        <div style="text-align:center;">
            <a href="Request_Quote" style="background:#e63946;color:#fff;padding:1em 2em;border-radius:8px;font-size:1.3em;font-weight:700;text-decoration:none;box-shadow:0 2px 8px rgba(230,57,70,0.12);transition:background 0.2s;">
                Get an Instant Quote &gt;
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

# Sumamry Section
# with st.container():
#     st.write("---")
#     left_column, right_column = st.columns(2)
#     with left_column:
#         st.header("Upcoming Events")
#         st.write("##")

#         query = """
#             select event_date::date  as event_date
#             , a.event_name 
#             , a.event_status
#             from events a
#             where event_status in ('Scheduled','Ongoing')
#             and a.deleted_at is null 
#             and event_date >= now()::date
#             order by event_date 
#         """
        
#         # Execute the query and create a DataFrame
#         df = run_query(query)
#         # Display the query results as text rows
#         if not df.empty:
#             for index, row in df.iterrows():
#                 st.text(f" {row['event_date']} - {row['event_status']} - {row['event_name']} ")
#         else:
#             st.text("No scheduled events found.")

  

  
  

# try:
#     # Execute your query
#     result = conn.execute("SELECT * FROM your_table")
#     # Process the results here
#     for row in result:
#         print(row)
# finally:
#     # Ensure the connection is closed
#     conn.close()

 

# # Define the path for the main hover image
# image_path = "https://universemagazine.com/wp-content/uploads/2022/08/zm4nfgq29yi91-1536x1536-1.jpg"  # Main hover image

# # Define CSS for hover effect with "info" text as the trigger
# hover_style = """
# <style>
# .hover-container {
#     position: relative;
#     display: inline-block;
#     cursor: pointer;
# }
# .hover-text {
#     font-size: 16px;
#     font-weight: bold;
#     color: #007BFF; /* Blue color for the text */
#     text-decoration: underline;
# }
# .hover-image {
#     display: none;
#     position: absolute; /* Position the pop-up relative to the container */
#     top: 0; /* Align vertically with the text */
#     left: 120%; /* Position the pop-up to the right of the text */
#     z-index: 999;
#     background: #fff;
#     border: 1px solid #ddd;
#     box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
#     width: 100px; /* Set the pop-up image width */
#     height: 100px; /* Set the pop-up image height */
#     object-fit: cover; /* Ensure the image fills the defined dimensions */
# }
# .hover-container:hover .hover-image {
#     display: block;
# }
# </style>
# """
 
# st.markdown(hover_style, unsafe_allow_html=True)

# # App layout
# st.title("Image Pop-up Triggered by Text")

# # Use "info" text as the hover trigger
# st.markdown(f"""
# <div class="hover-container">
#     <div>
#         <span class="hover-text">info</span> <!-- Text trigger -->
#     </div>
#     <img src="{image_path}" class="hover-image" alt="popup image" />
# </div>
# """, unsafe_allow_html=True)
