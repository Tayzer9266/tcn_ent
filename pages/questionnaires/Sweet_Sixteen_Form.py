import streamlit as st

def render():
    st.header("🎂 Sweet Sixteen Questionnaire")
    st.write("Please provide details about your Sweet Sixteen celebration to help us create the perfect experience.")
    
    # Basic Event Information
    st.subheader("📋 Basic Event Information")
    col1, col2 = st.columns(2)
    with col1:
        event_date = st.date_input("Event Date*")
        host_name = st.text_input("Host/Organizer Name*")
        host_phone = st.text_input("Host Phone Number*")
    with col2:
        host_email = st.text_input("Host Email Address*", value=st.session_state.get('user_email', ''))
        start_time = st.time_input("Event Start Time*")
        if start_time:
            st.write(f"Selected: {start_time.strftime('%I:%M %p')}")
        end_time = st.time_input("Event End Time*")
        if end_time:
            st.write(f"Selected: {end_time.strftime('%I:%M %p')}")
    num_guests = st.number_input("Number of Guests*", min_value=1, step=1)
    
    # Venue Information
    st.subheader("🏛️ Venue Information")
    venue_name = st.text_input("Reception/Main Venue Name*")
    venue_address = st.text_input("Reception Address (Street, City, State, Zip)*")
    venue_phone = st.text_input("Venue Phone Number")
    
    # Birthday Person Information
    st.subheader("🎂 Birthday Person Information")
    col1, col2 = st.columns(2)
    with col1:
        birthday_name = st.text_input("Birthday Person's Name*")
    with col2:
        actual_birthday = st.date_input("Actual birthday date*")
    
    # Party Theme
    st.subheader("🎨 Party Theme")
    party_theme = st.text_input("Party theme/colors")
    special_decorations = st.text_area("Special decorations")
    
    # Sweet Sixteen Traditions
    st.subheader("✨ Sweet Sixteen Traditions")
    col1, col2, col3 = st.columns(3)
    with col1:
        candle_ceremony = st.radio("Candle lighting ceremony?", ["Yes", "No"], horizontal=True)
        if candle_ceremony == "Yes":
            num_candles = st.number_input("Number of candles (16 + 1 for luck)", min_value=17, max_value=20, value=17)
            candle_song = st.text_input("Candle lighting song")
            candle_dedications = st.text_area("Special dedications for each candle")
    with col2:
        keys_ceremony = st.radio("Keys ceremony? (receiving car keys)", ["Yes", "No"], horizontal=True)
        tiara_ceremony = st.radio("Tiara/crown ceremony?", ["Yes", "No"], horizontal=True)
    with col3:
        grand_entrance = st.radio("Grand entrance?", ["Yes", "No"], horizontal=True)
        if grand_entrance == "Yes":
            entrance_song = st.text_input("Introduction song")
    
    # Equipment & Services
    st.subheader("🎛️ Equipment & Services")
    col1, col2, col3 = st.columns(3)
    with col1:
        uplighting = st.radio("Up-Lighting?", ["Yes", "No"], horizontal=True)
        if uplighting == "Yes":
            uplighting_count = st.number_input("How many?", min_value=1, step=1)
            uplighting_color = st.text_input("What color?")
    with col2:
        projection = st.radio("Projection Screen?", ["Yes", "No"], horizontal=True)
    with col3:
        photobooth = st.radio("Photo Booth?", ["Yes", "No"], horizontal=True)
        if photobooth == "Yes":
            photobooth_template = st.selectbox("Template selection", ["Standard", "Custom"])
            photobooth_images = st.number_input("Number of images", min_value=1, step=1)
            photobooth_props = st.radio("Props?", ["Yes", "No"], horizontal=True)
            photobooth_backdrop = st.selectbox("Backdrop color", ["White", "Shimmering", "Black", "Other"])
    
    # Music Programming
    st.subheader("🎵 Music Programming")
    cocktail_music = st.multiselect("Cocktail Hour Music Style:", [
        "Big Band", "Soft Rock", "Current Top 40", "Alternative",
        "Motown", "R&B", "Smooth Jazz", "Country", 
        "Vitamin String Quartet", "Afrobeats"
    ])
    dinner_music = st.multiselect("Dinner Music Style:", [
        "Big Band", "Soft Rock", "Current Top 40", "Alternative",
        "Motown", "R&B", "Smooth Jazz", "Country", 
        "Vitamin String Quartet", "Afrobeats"
    ])
    dinner_time = st.time_input("Dinner Time")
    if dinner_time:
        st.write(f"Selected: {dinner_time.strftime('%I:%M %p')}")
    dinner_style = st.selectbox("Dinner Style", ["Plated", "Buffet", "Family Style"])
    
    # General Music Preferences
    st.subheader("🎶 General Music Preferences")
    music_genres = st.multiselect("Music genres to include:", [
        "Oldies", "Motown", "Sock Hip", "Rock", "Emo", "Top 40", 
        "70's Disco", "80's", "90's", "Hip-Hop", "Country", "R&B", 
        "Afrobeats", "Techno", "Alternative", "House", "Afro-House", "Remixes"
    ])
    custom_playlist = st.text_input("Custom genres or playlist URLs")
    must_play = st.text_area("Must-play songs (up to 20)", placeholder="Enter one song per line")
    do_not_play = st.text_area("Do not play songs", placeholder="Enter one song per line")
    guest_requests = st.radio("Allow guest song requests?", ["Yes", "No"], horizontal=True)
    fade_songs = st.radio("Can DJ fade out songs that aren't working?", ["Yes", "No"], horizontal=True)
    
    # Age-Appropriate Music
    st.subheader("🎵 Age-Appropriate Music")
    current_hits = st.text_area("Current Top 40 hits")
    teen_artists = st.text_area("Teen-popular artists")
    age_classics = st.text_area("Age-appropriate classics")
    tiktok_songs = st.text_area("TikTok trending songs")
    
    # Special Moments
    st.subheader("💫 Special Moments")
    parent_speeches = st.radio("Parent speeches?", ["Yes", "No"], horizontal=True)
    birthday_toast = st.radio("Birthday toast?", ["Yes", "No"], horizontal=True)
    
    # Activities
    st.subheader("🎯 Activities")
    special_dances = st.text_area("Special dances or performances")
    group_photo_times = st.text_input("Group photo times")
    social_media_moments = st.text_area("Social media moments")
    
    # Line Dances
    st.subheader("💃 Line Dances")
    st.write("Select appropriate dances for the celebration:")
    col1, col2 = st.columns(2)
    with col1:
        trending_dances = st.radio("Current trending dances", ["Yes", "No"], horizontal=True)
        age_appropriate = st.radio("Age-appropriate line dances", ["Yes", "No"], horizontal=True, value="Yes")
    with col2:
        social_media_dances = st.radio("Social media popular dances", ["Yes", "No"], horizontal=True)
    
    # Event Coordination
    st.subheader("🤝 Event Coordination")
    banquet_manager = st.text_input("Banquet Manager Name & Contact")
    photographer = st.text_input("Photographer Name & Contact")
    videographer = st.text_input("Videographer Name & Contact")
    other_vendors = st.text_area("Other vendor contacts")
    
    # Announcements
    st.subheader("📢 Announcements")
    col1, col2 = st.columns(2)
    with col1:
        announce_requests = st.radio("Announce that guests can request songs?", ["Yes", "No"], horizontal=True)
        announce_photobooth = st.radio("Announce photo booth?", ["Yes", "No"], horizontal=True)
        announce_guestbook = st.radio("Announce guest book signing?", ["Yes", "No"], horizontal=True)
    with col2:
        snack_time = st.time_input("Late night snack announcement time")
        if snack_time:
            st.write(f"Selected: {snack_time.strftime('%I:%M %p')}")
        last_call = st.time_input("Last call for alcohol time")
        if last_call:
            st.write(f"Selected: {last_call.strftime('%I:%M %p')}")
        photobooth_warning = st.radio("15-minute photo booth warning?", ["Yes", "No"], horizontal=True)
    
    # Final Notes
    st.subheader("📝 Final Notes")
    last_song = st.text_input("Last song of the night")
    additional_notes = st.text_area("Any additional notes or special requests")
    
    st.info("💡 All fields marked with * are required. Your information helps us create the perfect celebration!")
