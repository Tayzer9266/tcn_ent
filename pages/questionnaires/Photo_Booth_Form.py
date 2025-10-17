import streamlit as st
from utils.pdf_generator import generate_photo_booth_questionnaire_pdf
from datetime import datetime

def render():
    st.header("📸 Photo Booth Questionnaire")
    st.write("Please provide details about your photo booth event to help us create the perfect experience.")
    
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
    
    # Photo Booth Details
    st.subheader("📸 Photo Booth Details")
    col1, col2 = st.columns(2)
    with col1:
        photobooth_template = st.selectbox("Template selection", ["Standard", "Custom"])
        photobooth_images = st.number_input("Number of Images per Session", min_value=1, step=1, value=4)
        photobooth_props = st.radio("Props?", ["Yes", "No"], horizontal=True)
    with col2:
        photobooth_backdrop = st.selectbox("Backdrop Color", ["White", "Shimmering", "Black", "Other"])
        photobooth_duration = st.number_input("Photo Booth Duration (hours)", min_value=1, step=1, value=4)
        photobooth_location = st.text_input("Photo Booth Location within Venue")

    # Photo Template Details
    st.subheader("🖼️ Photo Template Details")
    col1, col2 = st.columns(2)
    with col1:
        photo_template_size = st.selectbox("Photo Template Size", ["2x6", "4x6"])
        photos_per_template = st.number_input("Number of Photos per Template", min_value=1, max_value=5, step=1, value=1)
    with col2:
        template_description = st.text_area("Template Description (e.g., balloons, colors, themes)", height=100)

    # Photo Booth Special Features
    st.subheader("✨ Photo Booth Special Features")
    col1, col2 = st.columns(2)
    with col1:
        green_screen = st.radio("Green Screen Effects?", ["Yes", "No"], horizontal=True)
        instant_printing = st.radio("Instant Printing?", ["Yes", "No"], horizontal=True)
        digital_gallery = st.radio("Digital Gallery?", ["Yes", "No"], horizontal=True)
    with col2:
        custom_overlays = st.radio("Custom Overlays?", ["Yes", "No"], horizontal=True)
        social_media_sharing = st.radio("Social Media Sharing?", ["Yes", "No"], horizontal=True)
        video_booth = st.radio("Video Booth Option?", ["Yes", "No"], horizontal=True)

    # Event Coordination
    st.subheader("🤝 Event Coordination")
    banquet_manager = st.text_input("Banquet Manager Name & Contact")
    photographer = st.text_input("Photographer Name & Contact")
    videographer = st.text_input("Videographer Name & Contact")
    other_vendors = st.text_area("Other vendor contacts")

    # Final Notes
    st.subheader("📝 Final Notes")
    additional_notes = st.text_area("Any additional notes or special requests")
    
    st.info("💡 All fields marked with * are required. Your information helps us create the perfect celebration!")
    
    # PDF Download Button
    st.markdown("---")
    st.subheader("📄 Download Blank Questionnaire")
    st.write("Download a printable PDF version of this questionnaire to fill out offline.")
    
    if st.button("📥 Download Photo Booth Questionnaire PDF", use_container_width=True, key="download_photo_booth_pdf_btn"):
        try:
            # Generate blank questionnaire PDF
            pdf_bytes = generate_photo_booth_questionnaire_pdf()
            
            # Create download button
            st.download_button(
                label="⬇️ Download PDF Now",
                data=pdf_bytes,
                file_name=f"Photo_Booth_Questionnaire_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                key="photo_booth_questionnaire_pdf"
            )
            st.success("✅ PDF generated successfully! Click the download button above to save the questionnaire.")
            
        except Exception as e:
            st.error(f"❌ Error generating PDF: {str(e)}")
            st.info("Please try again or contact support if the issue persists.")
