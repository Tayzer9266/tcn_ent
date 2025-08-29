import streamlit as st

def render():
    st.header("👑 Quinceañera Questionnaire")
    st.write("Please provide details about your Quinceañera celebration to help us create the perfect experience.")
    
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
    
    # Quinceañera Information
    st.subheader("👑 Quinceañera Information")
    col1, col2 = st.columns(2)
    with col1:
        quinceanera_name = st.text_input("Quinceañera's Name*")
    with col2:
        birthday_date = st.date_input("Turning 15 date*")
    
    # Religious Ceremony
    st.subheader("⛪ Religious Ceremony")
    church_name = st.text_input("Church Name (if applicable)")
    mass_time = st.time_input("Mass time")
    if mass_time:
        st.write(f"Selected: {mass_time.strftime('%I:%M %p')}")
    priest_contact = st.text_input("Priest/Pastor contact")
    
    # Court of Honor
    st.subheader("👑 Court of Honor")
    court_intro = st.radio("Court introduction?", ["Yes", "No"], horizontal=True)
    if court_intro == "Yes":
        court_members = st.number_input("Number of court members (damas and chambelanes)", min_value=1, max_value=20, step=1)
        court_names = st.text_area("Court member names", placeholder="Enter one name per line")
        court_song = st.text_input("Court entrance song")
    
    # Traditional Ceremonies
    st.subheader("🎭 Traditional Ceremonies")
    col1, col2, col3 = st.columns(3)
    with col1:
        shoe_ceremony = st.radio("Changing of shoes ceremony?", ["Yes", "No"], horizontal=True)
        if shoe_ceremony == "Yes":
            shoe_changer = st.text_input("Who will change the shoes (father/male relative)")
            shoe_song = st.text_input("Changing of shoes song")
    with col2:
        crown_ceremony = st.radio("Crown/tiara ceremony?", ["Yes", "No"], horizontal=True)
    with col3:
        doll_ceremony = st.radio("Last doll ceremony?", ["Yes", "No"], horizontal=True)
    
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
    
    # Cultural Music
    st.subheader("🎵 Cultural Music")
    traditional_mexican = st.text_area("Traditional Mexican music requests")
    mariachi_requests = st.text_area("Mariachi requests")
    regional_music = st.multiselect("Regional music preferences", ["Norteño", "Banda", "Other"])
    latin_hits = st.text_area("Contemporary Latin hits")
    
    # Special Dances
    st.subheader("💃 Special Dances")
    col1, col2 = st.columns(2)
    with col1:
        waltz_song = st.text_input("Waltz song (traditional first dance)*")
        father_dance = st.text_input("Father-daughter dance song")
        surprise_dance = st.text_input("Surprise dance song")
    with col2:
        court_waltz = st.text_input("Court waltz (group dance)")
    
    # Reception Elements
    st.subheader("🥂 Reception Elements")
    parent_toast = st.radio("Toast by parents?", ["Yes", "No"], horizontal=True)
    padrinos_toast = st.radio("Toast by padrinos (godparents)?", ["Yes", "No"], horizontal=True)
    brindis = st.radio("Brindis (official toast)?", ["Yes", "No"], horizontal=True)
    
    # Cultural Announcements
    st.subheader("📢 Cultural Announcements")
    presentation = st.radio("Presentation of the quinceañera?", ["Yes", "No"], horizontal=True)
    tradition_explanation = st.radio("Explanation of traditions for non-Latino guests?", ["Yes", "No"], horizontal=True)
    
    # Line Dances
    st.subheader("💃 Line Dances")
    st.write("Select appropriate dances for the celebration:")
    col1, col2 = st.columns(2)
    with col1:
        mexican_dances = st.radio("Traditional Mexican group dances", ["Yes", "No"], horizontal=True)
        latin_dances = st.radio("Latin dance styles", ["Yes", "No"], horizontal=True)
    with col2:
        standard_dances = st.radio("Standard line dances", ["Yes", "No"], horizontal=True)
        cultural_circle = st.radio("Cultural circle dances", ["Yes", "No"], horizontal=True)
    
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
