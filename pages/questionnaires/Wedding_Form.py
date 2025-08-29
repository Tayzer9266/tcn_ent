import streamlit as st

def render():
    st.header("💍 Wedding Questionnaire")
    st.write("Please provide details about your wedding celebration to help us create the perfect experience.")
    
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
    
    # Couple Information
    st.subheader("👰‍♀️🤵‍♂️ Couple Information")
    col1, col2 = st.columns(2)
    with col1:
        bride_name = st.text_input("Bride's Name*")
    with col2:
        groom_name = st.text_input("Groom's Name*")
    
    # Ceremony Details
    st.subheader("⛪ Ceremony Details")
    ceremony_venue = st.text_input("Wedding Ceremony Facility Name (Optional)")
    ceremony_address = st.text_input("Ceremony Address")
    ceremony_phone = st.text_input("Ceremony Phone")
    has_ceremony = st.radio("Ceremony Music?", ["Yes", "No"], horizontal=True)
    ceremony_time = st.time_input("Ceremony Start Time") if has_ceremony == "Yes" else None
    
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
    
    # Special Wedding Moments
    st.subheader("💫 Special Wedding Moments")
    col1, col2 = st.columns(2)
    with col1:
        first_dance = st.text_input("First dance song")
        first_dance_time = st.time_input("First dance time")
        father_dance = st.text_input("Father-bride dance song")
        father_name = st.text_input("Father's name")
        father_dance_time = st.time_input("Father-bride dance time")
    with col2:
        bridal_dance = st.text_input("Bridal party dance song")
        mother_dance = st.text_input("Mother-groom dance song")
        mother_name = st.text_input("Mother's name")
        mother_dance_time = st.time_input("Mother-groom dance time")
    
    anniversary_dance = st.radio("Anniversary dance?", ["Yes", "No"], horizontal=True)
    cake_song = st.text_input("Cake cutting song")
    cake_time = st.time_input("Cake cutting time")
    
    # Wedding Ceremonies
    st.subheader("🎭 Wedding Ceremonies")
    garter_removal = st.text_input("Garter removal ceremony song")
    garter_removal_time = st.time_input("Garter removal time")
    garter_toss = st.text_input("Garter toss song")
    garter_toss_time = st.time_input("Garter toss time")
    bouquet_toss = st.text_input("Bouquet toss song")
    bouquet_toss_time = st.time_input("Bouquet toss time")
    
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
    private_dance = st.text_input("Private couple dance song")
    memory_book = st.radio("Memory book?", ["Yes", "No"], horizontal=True)
    additional_notes = st.text_area("Any additional notes or special requests")
    
    st.info("💡 All fields marked with * are required. Your information helps us create the perfect celebration!")
