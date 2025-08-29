import streamlit as st

def render():
    st.header("🎊 General Party Questionnaire")
    st.write("Please provide details about your celebration to help us create the perfect experience.")
    
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
    
    # Event Details
    st.subheader("🎉 Event Details")
    occasion = st.text_input("Occasion/Reason for celebration*")
    guest_of_honor = st.text_input("Guest of honor (if applicable)")
    party_theme = st.text_input("Party theme or style")
    
    # Celebration Type
    st.subheader("🎭 Celebration Type")
    celebration_type = st.selectbox("Type of celebration", [
        "Corporate event",
        "Retirement party", 
        "Anniversary celebration",
        "Graduation party",
        "Holiday party",
        "Reunion",
        "Other"
    ])
    
    if celebration_type == "Other":
        other_type = st.text_input("Please specify other celebration type")
    
    # Specific Needs
    st.subheader("🎯 Specific Needs")
    col1, col2 = st.columns(2)
    with col1:
        professional_atmosphere = st.radio("Professional atmosphere required?", ["Yes", "No"], horizontal=True)
        family_friendly = st.radio("Family-friendly content only?", ["Yes", "No"], horizontal=True)
    with col2:
        age_range = st.text_input("Age range of attendees")
        cultural_considerations = st.text_area("Cultural considerations")
    
    # Special Elements
    st.subheader("✨ Special Elements")
    recognition_ceremony = st.radio("Recognition/awards ceremony?", ["Yes", "No"], horizontal=True)
    if recognition_ceremony == "Yes":
        ceremony_details = st.text_area("Ceremony details")
    
    speeches = st.radio("Speeches or presentations?", ["Yes", "No"], horizontal=True)
    if speeches == "Yes":
        speech_details = st.text_area("Speech details")
    
    special_announcements = st.text_area("Special announcements")
    group_activities = st.text_area("Group activities")
    
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
    
    # Music Considerations
    st.subheader("🎵 Music Considerations")
    volume_levels = st.selectbox("Appropriate volume levels for venue type", [
        "Background Music", "Conversation Level", "Moderate Dancing", "Energetic Dancing"
    ])
    music_ratio = st.slider("Background music vs. dance music ratio", 0, 100, 50)
    genre_restrictions = st.text_area("Specific genre restrictions")
    clean_versions = st.radio("Clean versions only?", ["Yes", "No"], horizontal=True)
    
    # Line Dances
    st.subheader("💃 Line Dances")
    st.write("Line dance preferences:")
    if celebration_type in ["Corporate event", "Professional event"]:
        st.info("Professional events may skip line dances entirely")
        include_line_dances = st.radio("Include line dances?", ["No", "Yes - Limited", "Yes - Full Selection"], horizontal=True)
    else:
        line_dance_preference = st.selectbox("Line dance preference", [
            "None", "Limited Selection", "Full Selection", "Custom Selection"
        ])
    
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
