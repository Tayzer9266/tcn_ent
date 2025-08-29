import streamlit as st
from utils.pdf_generator import generate_wedding_pdf_response
from datetime import datetime

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
    has_ceremony = st.radio("Ceremony Music?", ["Yes", "No"], horizontal=True, index=1)
    ceremony_time = st.time_input("Ceremony Start Time") if has_ceremony == "Yes" else None
    if has_ceremony == "Yes" and ceremony_time:
        st.write(f"Selected: {ceremony_time.strftime('%I:%M %p')}")
    
    # Equipment & Services
    st.subheader("🎛️ Equipment & Services")
    col1, col2, col3 = st.columns(3)
    with col1:
        uplighting = st.radio("Up-Lighting?", ["Yes", "No"], horizontal=True, index=1)
        if uplighting == "Yes":
            uplighting_count = st.number_input("How many?", min_value=1, step=1)
            uplighting_color = st.text_input("What color?")
    with col2:
        projection = st.radio("Projection Screen?", ["Yes", "No"], horizontal=True, index=1)
    with col3:
        photobooth = st.radio("Photo Booth?", ["Yes", "No"], horizontal=True, index=1)
        if photobooth == "Yes":
            photobooth_template = st.selectbox("Template selection", ["Standard", "Custom"])
            photobooth_images = st.number_input("Number of images", min_value=1, step=1)
            photobooth_props = st.radio("Props?", ["Yes", "No"], horizontal=True, index=1)
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
    guest_requests = st.radio("Allow guest song requests?", ["Yes", "No"], horizontal=True, index=1)
    fade_songs = st.radio("Can DJ fade out songs that aren't working?", ["Yes", "No"], horizontal=True, index=1)
    
    # Special Wedding Moments
    st.subheader("💫 Special Wedding Moments")
    col1, col2 = st.columns(2)
    with col1:
        first_dance = st.text_input("First dance song")
        first_dance_time = st.time_input("First dance time")
        if first_dance_time:
            st.write(f"Selected: {first_dance_time.strftime('%I:%M %p')}")
        father_dance = st.text_input("Father-bride dance song")
        father_name = st.text_input("Father's name")
        father_dance_time = st.time_input("Father-bride dance time")
        if father_dance_time:
            st.write(f"Selected: {father_dance_time.strftime('%I:%M %p')}")
    with col2:
        bridal_dance = st.text_input("Bridal party dance song")
        mother_dance = st.text_input("Mother-groom dance song")
        mother_name = st.text_input("Mother's name")
        mother_dance_time = st.time_input("Mother-groom dance time")
        if mother_dance_time:
            st.write(f"Selected: {mother_dance_time.strftime('%I:%M %p')}")
    
    anniversary_dance = st.radio("Anniversary dance?", ["Yes", "No"], horizontal=True)
    cake_song = st.text_input("Cake cutting song")
    cake_time = st.time_input("Cake cutting time")
    if cake_time:
        st.write(f"Selected: {cake_time.strftime('%I:%M %p')}")
    
    # Wedding Ceremonies
    st.subheader("🎭 Wedding Ceremonies")
    garter_removal = st.text_input("Garter removal ceremony song")
    garter_removal_time = st.time_input("Garter removal time")
    if garter_removal_time:
        st.write(f"Selected: {garter_removal_time.strftime('%I:%M %p')}")
    garter_toss = st.text_input("Garter toss song")
    garter_toss_time = st.time_input("Garter toss time")
    if garter_toss_time:
        st.write(f"Selected: {garter_toss_time.strftime('%I:%M %p')}")
    bouquet_toss = st.text_input("Bouquet toss song")
    bouquet_toss_time = st.time_input("Bouquet toss time")
    if bouquet_toss_time:
        st.write(f"Selected: {bouquet_toss_time.strftime('%I:%M %p')}")
    
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
        announce_requests = st.radio("Announce that guests can request songs?", ["Yes", "No"], horizontal=True, index=1)
        announce_photobooth = st.radio("Announce photo booth?", ["Yes", "No"], horizontal=True, index=1)
        announce_guestbook = st.radio("Announce guest book signing?", ["Yes", "No"], horizontal=True, index=1)
    with col2:
        snack_time = st.time_input("Late night snack announcement time")
        if snack_time:
            st.write(f"Selected: {snack_time.strftime('%I:%M %p')}")
        last_call = st.time_input("Last call for alcohol time")
        if last_call:
            st.write(f"Selected: {last_call.strftime('%I:%M %p')}")
        photobooth_warning = st.radio("15-minute photo booth warning?", ["Yes", "No"], horizontal=True, index=1)
    
    # Final Notes
    st.subheader("📝 Final Notes")
    last_song = st.text_input("Last song of the night")
    private_dance = st.text_input("Private couple dance song")
    memory_book = st.radio("Memory book?", ["Yes", "No"], horizontal=True)
    additional_notes = st.text_area("Any additional notes or special requests")
    
    st.info("💡 All fields marked with * are required. Your information helps us create the perfect celebration!")
    
    # PDF Download Button
    st.markdown("---")
    st.subheader("📄 Download Your Responses")
    
    if st.button("📥 Download Responses as PDF", use_container_width=True, key="download_pdf_btn"):
        # Collect all form data
        form_data = {
            'event_date': str(event_date) if event_date else None,
            'host_name': host_name,
            'host_phone': host_phone,
            'host_email': host_email,
            'start_time': str(start_time) if start_time else None,
            'end_time': str(end_time) if end_time else None,
            'num_guests': num_guests,
            'venue_name': venue_name,
            'venue_address': venue_address,
            'venue_phone': venue_phone,
            'bride_name': bride_name,
            'groom_name': groom_name,
            'ceremony_venue': ceremony_venue,
            'ceremony_address': ceremony_address,
            'ceremony_phone': ceremony_phone,
            'has_ceremony': has_ceremony,
            'ceremony_time': str(ceremony_time) if ceremony_time else None,
            'uplighting': uplighting,
            'uplighting_count': uplighting_count if uplighting == "Yes" else None,
            'uplighting_color': uplighting_color if uplighting == "Yes" else None,
            'projection': projection,
            'photobooth': photobooth,
            'photobooth_template': photobooth_template if photobooth == "Yes" else None,
            'photobooth_images': photobooth_images if photobooth == "Yes" else None,
            'photobooth_props': photobooth_props if photobooth == "Yes" else None,
            'photobooth_backdrop': photobooth_backdrop if photobooth == "Yes" else None,
            'cocktail_music': cocktail_music,
            'dinner_music': dinner_music,
            'dinner_time': str(dinner_time) if dinner_time else None,
            'dinner_style': dinner_style,
            'music_genres': music_genres,
            'custom_playlist': custom_playlist,
            'must_play': must_play,
            'do_not_play': do_not_play,
            'guest_requests': guest_requests,
            'fade_songs': fade_songs,
            'first_dance': first_dance,
            'first_dance_time': str(first_dance_time) if first_dance_time else None,
            'father_dance': father_dance,
            'father_name': father_name,
            'father_dance_time': str(father_dance_time) if father_dance_time else None,
            'bridal_dance': bridal_dance,
            'mother_dance': mother_dance,
            'mother_name': mother_name,
            'mother_dance_time': str(mother_dance_time) if mother_dance_time else None,
            'anniversary_dance': anniversary_dance,
            'cake_song': cake_song,
            'cake_time': str(cake_time) if cake_time else None,
            'garter_removal': garter_removal,
            'garter_removal_time': str(garter_removal_time) if garter_removal_time else None,
            'garter_toss': garter_toss,
            'garter_toss_time': str(garter_toss_time) if garter_toss_time else None,
            'bouquet_toss': bouquet_toss,
            'bouquet_toss_time': str(bouquet_toss_time) if bouquet_toss_time else None,
            'banquet_manager': banquet_manager,
            'photographer': photographer,
            'videographer': videographer,
            'other_vendors': other_vendors,
            'announce_requests': announce_requests,
            'announce_photobooth': announce_photobooth,
            'announce_guestbook': announce_guestbook,
            'snack_time': str(snack_time) if snack_time else None,
            'last_call': str(last_call) if last_call else None,
            'photobooth_warning': photobooth_warning,
            'last_song': last_song,
            'private_dance': private_dance,
            'memory_book': memory_book,
            'additional_notes': additional_notes
        }
        
        try:
            # Generate PDF
            pdf_bytes = generate_wedding_pdf_response(form_data)
            
            # Create download button
            st.download_button(
                label="⬇️ Download PDF Now",
                data=pdf_bytes,
                file_name=f"Wedding_Questionnaire_Responses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                key="wedding_responses_pdf"
            )
            st.success("✅ PDF generated successfully! Click the download button above to save your responses.")
            
        except Exception as e:
            st.error(f"❌ Error generating PDF: {str(e)}")
            st.info("Please try again or contact support if the issue persists.")
