import streamlit as st
from utils.pdf_generator import generate_birthday_party_questionnaire_pdf
from datetime import datetime

def render():
    st.header("🎉 Birthday Party Questionnaire")
    st.write("Please provide details about your birthday celebration to help us create the perfect experience.")
    
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
        birthday_age = st.number_input("Age turning*", min_value=1, max_value=100, step=1)
    with col2:
        actual_birthday = st.date_input("Actual birthday date*")
    
    # Party Style
    st.subheader("🎨 Party Style")
    milestone = st.selectbox("Milestone birthday?", ["Not a milestone", "18th", "21st", "30th", "40th", "50th", "60th", "70th", "80th", "90th", "100th"])
    party_theme = st.text_input("Party theme")
    atmosphere = st.selectbox("Formal or casual atmosphere", ["Casual", "Semi-Formal", "Formal"])
    
    # Age-Specific Elements
    st.subheader("👶👦👩👴 Age-Specific Elements")
    
    age_group = st.selectbox("Primary age group of attendees", [
        "Children (Under 13)",
        "Teens (13-17)", 
        "Young Adults (18-25)",
        "Adults (26-45)",
        "Middle Age (46-65)",
        "Seniors (65+)"
    ])
    
    if age_group == "Children (Under 13)":
        st.write("🎈 Children's Birthday Settings")
        kid_friendly = st.radio("Kid-friendly music only?", ["Yes", "No"], horizontal=True, value="Yes")
        interactive_games = st.text_area("Interactive games music")
        character_songs = st.text_area("Character theme songs")
        action_songs = st.multiselect("Action songs", ["Freeze Dance", "Musical Chairs", "Hokey Pokey", "Chicken Dance"])
        
    elif age_group == "Teens (13-17)":
        st.write("🎵 Teen Birthday Settings")
        current_hits = st.radio("Current hits and trending songs?", ["Yes", "No"], horizontal=True, value="Yes")
        age_appropriate = st.radio("Age-appropriate content only?", ["Yes", "No"], horizontal=True, value="Yes")
        social_media = st.text_area("Social media friendly moments")
        
    else:
        st.write("🎊 Adult Birthday Settings")
        era_music = st.multiselect("Music from their era/decade", [
            "50s", "60s", "70s", "80s", "90s", "2000s", "2010s", "Current"
        ])
        nostalgic_hits = st.text_area("Nostalgic hits from their youth")
        sophisticated = st.radio("Sophisticated party atmosphere?", ["Yes", "No"], horizontal=True)
    
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
    must_play = st.text_area("Must-play songs (up to 20)")
    do_not_play = st.text_area("Do not play songs")
    guest_requests = st.radio("Allow guest song requests?", ["Yes", "No"], horizontal=True)
    fade_songs = st.radio("Can DJ fade out songs that aren't working?", ["Yes", "No"], horizontal=True)
    
    # Special Moments
    st.subheader("💫 Special Moments")
    birthday_intro = st.radio("Birthday person introduction?", ["Yes", "No"], horizontal=True)
    cake_presentation = st.text_input("Cake presentation song")
    birthday_toast = st.radio("Birthday toast/speech?", ["Yes", "No"], horizontal=True)
    family_recognition = st.text_area("Special recognition of family/friends")
    
    # Activities Based on Age
    st.subheader("🎯 Activities Based on Age")
    dancing_level = st.selectbox("Dancing level appropriate for age group", [
        "None", "Light", "Moderate", "Energetic", "Very Active"
    ])
    interactive_elements = st.text_area("Interactive elements")
    group_participation = st.text_area("Group participation songs")
    
    # Order of Events and Time
    st.subheader("📅 Order of Events and Time")
    st.write("Please list the order of events for your celebration with their scheduled times:")

    # Common Birthday events
    default_events = [
        "Guest Arrival",
        "Birthday Person Introduction",
        "Cocktail Hour",
        "Dinner Service",
        "Cake Cutting",
        "Birthday Toast/Speech",
        "Special Recognition",
        "Open Dancing",
        "Group Participation",
        "Interactive Elements",
        "Last Dance"
    ]

    st.info("💡 Tip: You can modify, remove, or add events based on your preferences. Use the fields below to plan your timeline.")

    # Create a dynamic list for events
    num_events = st.number_input("How many events do you want to schedule?", min_value=1, max_value=25, value=10, step=1)

    event_schedule = []
    for i in range(num_events):
        col1, col2 = st.columns([3, 2])
        with col1:
            event_name = st.text_input(
                f"Event {i+1} Name",
                value=default_events[i] if i < len(default_events) else "",
                key=f"event_name_{i}"
            )
        with col2:
            event_time = st.time_input(f"Event {i+1} Time", key=f"event_time_{i}")
            if event_time:
                st.write(f"Selected: {event_time.strftime('%I:%M %p')}")

        if event_name:
            event_schedule.append({
                "order": i + 1,
                "name": event_name,
                "time": event_time.strftime('%I:%M %p') if event_time else ""
            })

    # Line Dances
    st.subheader("💃 Line Dances")
    st.write("Select appropriate dances for the celebration:")
    if age_group == "Children (Under 13)":
        st.write("Children's action songs and simple dances")
    elif age_group == "Teens (13-17)":
        st.write("Current trending dances and age-appropriate line dances")
    else:
        st.write("Classic line dances and era-appropriate dances")
    
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

    # PDF Download Button
    st.markdown("---")
    st.subheader("📄 Download Blank Questionnaire")
    st.write("Download a printable PDF version of this questionnaire to fill out offline.")

    if st.button("📥 Download Birthday Party Questionnaire PDF", use_container_width=True, key="download_birthday_party_pdf_btn"):
        try:
            # Generate blank questionnaire PDF
            pdf_bytes = generate_birthday_party_questionnaire_pdf()

            # Create download button
            st.download_button(
                label="⬇️ Download PDF Now",
                data=pdf_bytes,
                file_name=f"Birthday_Party_Questionnaire_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                key="birthday_party_questionnaire_pdf"
            )
            st.success("✅ PDF generated successfully! Click the download button above to save the questionnaire.")

        except Exception as e:
            st.error(f"❌ Error generating PDF: {str(e)}")
            st.info("Please try again or contact support if the issue persists.")
