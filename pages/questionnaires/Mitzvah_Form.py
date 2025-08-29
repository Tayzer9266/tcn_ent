import streamlit as st

def render():
    st.header("🎭 Mitzvah Questionnaire")
    st.write("Please provide details about your Bar/Bat Mitzvah celebration to help us create the perfect experience.")
    
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
        end_time = st.time_input("Event End Time*")
    num_guests = st.number_input("Number of Guests*", min_value=1, step=1)
    
    # Venue Information
    st.subheader("🏛️ Venue Information")
    venue_name = st.text_input("Reception/Main Venue Name*")
    venue_address = st.text_input("Reception Address (Street, City, State, Zip)*")
    venue_phone = st.text_input("Venue Phone Number")
    
    # Child Information
    st.subheader("👦👧 Child Information")
    col1, col2 = st.columns(2)
    with col1:
        child_name = st.text_input("Child's Name*")
        child_age = st.number_input("Child's Age*", min_value=12, max_value=14, step=1)
    with col2:
        hebrew_name = st.text_input("Hebrew Name (optional)")
    
    # Religious Ceremony
    st.subheader("🕍 Religious Ceremony")
    temple_name = st.text_input("Temple/Synagogue Name*")
    ceremony_address = st.text_input("Ceremony Address*")
    ceremony_time = st.time_input("Ceremony Start Time*")
    rabbi_name = st.text_input("Rabbi/Cantor Name & Contact")
    
    # Jewish Traditions
    st.subheader("✡️ Jewish Traditions")
    col1, col2, col3 = st.columns(3)
    with col1:
        hora_dance = st.radio("Hora dance?", ["Yes", "No"], horizontal=True)
        chair_dance = st.radio("Chair dance (lifting the child)?", ["Yes", "No"], horizontal=True)
    with col2:
        candle_ceremony = st.radio("Candle lighting ceremony?", ["Yes", "No"], horizontal=True)
        if candle_ceremony == "Yes":
            num_candles = st.number_input("Number of candles", min_value=1, max_value=20, value=13)
            candle_song = st.text_input("Candle lighting song")
    with col3:
        special_dedications = st.text_area("Special candle dedications")
    
    # Service Elements
    st.subheader("📖 Service Elements")
    torah_music = st.text_input("Torah reading music")
    haftorah_music = st.text_input("Haftorah reading music")
    special_prayers = st.text_area("Special prayers or songs")
    
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
    
    # Cultural Music
    st.subheader("🎵 Cultural Music")
    traditional_jewish = st.text_area("Traditional Jewish music requests")
    israeli_folk = st.text_area("Israeli folk songs")
    contemporary_jewish = st.text_area("Contemporary Jewish artists")
    
    # Party Introduction
    st.subheader("🎤 Party Introduction")
    child_intro = st.radio("Child introduction?", ["Yes", "No"], horizontal=True)
    if child_intro == "Yes":
        intro_song = st.text_input("Introduction song")
        family_recognition = st.text_area("Special recognition of family members")
    
    # Special Moments
    st.subheader("💫 Special Moments")
    col1, col2 = st.columns(2)
    with col1:
        motzi = st.radio("Motzi (blessing over bread)?", ["Yes", "No"], horizontal=True)
        kiddush = st.radio("Kiddush (blessing over wine)?", ["Yes", "No"], horizontal=True)
    with col2:
        parent_speeches = st.radio("Parent speeches?", ["Yes", "No"], horizontal=True)
        sibling_participation = st.radio("Sibling participation?", ["Yes", "No"], horizontal=True)
    
    # Line Dances
    st.subheader("💃 Line Dances")
    st.write("Select appropriate line dances for the celebration:")
    col1, col2 = st.columns(2)
    with col1:
        hava_nagila = st.radio("Hava Nagila", ["Yes", "No"], horizontal=True)
        traditional_circle = st.radio("Traditional Jewish circle dances", ["Yes", "No"], horizontal=True)
    with col2:
        standard_line = st.radio("Standard party line dances", ["Yes", "No"], horizontal=True)
        no_mature_content = st.radio("No overly mature content", ["Yes", "No"], horizontal=True, value="Yes")
    
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
        last_call = st.time_input("Last call for alcohol time")
        photobooth_warning = st.radio("15-minute photo booth warning?", ["Yes", "No"], horizontal=True)
    
    # Final Notes
    st.subheader("📝 Final Notes")
    last_song = st.text_input("Last song of the night")
    additional_notes = st.text_area("Any additional notes or special requests")
    
    st.info("💡 All fields marked with * are required. Your information helps us create the perfect celebration!")
