import streamlit as st
import os
import sys
from datetime import datetime, date, time, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client_manager import client_manager
from auth_utils import require_client_auth

# Require client authentication
require_client_auth()

# Page configuration
st.set_page_config(
    page_title="Request Quote",
    page_icon="pages/images/TCN logo black.jpg",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# Request a Quote for Your Event"
    }
)

# Custom CSS
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
.quote-container {
    background: white;
    border-radius: 15px;
    padding: 2em;
    box-shadow: 0 4px 20px rgba(230,57,70,0.15);
    max-width: 800px;
    margin: 2em auto;
}
.quote-title {
    font-size: 2.5em;
    font-weight: 700;
    color: #457b9d;
    text-align: center;
    margin-bottom: 0.5em;
}
.quote-subtitle {
    font-size: 1.1em;
    color: #666;
    text-align: center;
    margin-bottom: 2em;
}
.section-header {
    font-size: 1.3em;
    font-weight: 600;
    color: #457b9d;
    margin-top: 1.5em;
    margin-bottom: 0.8em;
    border-bottom: 2px solid #e63946;
    padding-bottom: 0.3em;
}
.service-card {
    background: linear-gradient(135deg, #f8fafc 0%, #e8f4f8 100%);
    border: 2px solid #457b9d;
    border-radius: 10px;
    padding: 1em;
    margin: 0.5em 0;
    cursor: pointer;
    transition: all 0.3s;
}
.service-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 15px rgba(69, 123, 157, 0.3);
}
.service-card.selected {
    background: linear-gradient(135deg, #457b9d 0%, #1d3557 100%);
    color: white;
    border-color: #e63946;
}
.info-box {
    background: #e8f4f8;
    border-left: 4px solid #457b9d;
    padding: 1em;
    margin: 1em 0;
    border-radius: 5px;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Check if user is logged in and is a client
if not st.session_state.get('logged_in', False):
    st.error("⚠️ Please login to request a quote")
    if st.button("Go to Login"):
        st.switch_page("pages/1_Login.py")
    st.stop()

if st.session_state.get('user_type') != 'client':
    st.error("⚠️ This page is for clients only")
    st.stop()

# Get client data
client_data = st.session_state.user_data
client_id = client_data['client_id']

# Get all available services
services = client_manager.get_all_services()

# Service type mapping
service_type_map = {
    'DJ Services': 'dj',
    'Photography Services': 'photographer',
    'Event Coordination': 'event_coordinator'
}

# Header
st.markdown('<div class="quote-container">', unsafe_allow_html=True)
st.markdown('<div class="quote-title">📋 Request a Quote</div>', unsafe_allow_html=True)
st.markdown('<div class="quote-subtitle">Tell us about your event and we\'ll connect you with the perfect professionals</div>', unsafe_allow_html=True)

# Quote request form
with st.form("quote_request_form"):
    
    # Service Selection
    st.markdown('<div class="section-header">🎵 Select Services</div>', unsafe_allow_html=True)
    st.markdown("Choose the services you need for your event:")
    
    selected_services = []
    
    # Create service selection checkboxes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        dj_service = st.checkbox("🎧 DJ Services", help="Professional DJ with music and MC services")
        if dj_service:
            selected_services.append('DJ Services')
    
    with col2:
        photo_service = st.checkbox("📸 Photography", help="Professional event photography")
        if photo_service:
            selected_services.append('Photography Services')
    
    with col3:
        coord_service = st.checkbox("🎉 Event Coordination", help="Complete event planning and coordination")
        if coord_service:
            selected_services.append('Event Coordination')
    
    # Additional services
    st.markdown("**Additional Services:**")
    col1, col2 = st.columns(2)
    
    with col1:
        lighting_service = st.checkbox("💡 Lighting & Effects", help="Professional lighting and special effects")
        if lighting_service:
            selected_services.append('Lighting & Effects')
    
    with col2:
        photobooth_service = st.checkbox("📷 Photo Booth", help="Fun photo booth with props")
        if photobooth_service:
            selected_services.append('Photo Booth')
    
    # Event Details
    st.markdown('<div class="section-header">🎊 Event Details</div>', unsafe_allow_html=True)
    
    event_name = st.text_input("Event Name *", placeholder="e.g., Sarah's Wedding Reception")
    
    event_type = st.selectbox(
        "Event Type *",
        ["", "Wedding", "Birthday Party", "Sweet Sixteen", "Quinceañera", "Bar/Bat Mitzvah", 
         "Corporate Event", "Fundraiser", "School Event", "Private Party", "Other"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        event_date = st.date_input(
            "Event Date *",
            min_value=date.today(),
            help="Select the date of your event"
        )
    
    with col2:
        estimated_guests = st.number_input(
            "Number of Guests *",
            min_value=1,
            max_value=10000,
            value=50,
            step=10,
            help="Approximate number of attendees"
        )
    
    # Location Details
    st.markdown('<div class="section-header">📍 Location Details</div>', unsafe_allow_html=True)
    
    venue = st.text_input("Venue Name", placeholder="e.g., Grand Ballroom at Hilton Hotel")
    
    event_location = st.text_input(
        "Event Address *",
        placeholder="e.g., 123 Main St, Dallas, TX 75201"
    )
    
    # Time Details
    st.markdown('<div class="section-header">⏰ Time Details</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        start_time = st.time_input(
            "Start Time *",
            value=time(18, 0),
            help="When does your event start?"
        )
    
    with col2:
        end_time = st.time_input(
            "End Time *",
            value=time(23, 0),
            help="When does your event end?"
        )
    
    with col3:
        # Calculate service hours
        if start_time and end_time:
            start_datetime = datetime.combine(date.today(), start_time)
            end_datetime = datetime.combine(date.today(), end_time)
            if end_datetime < start_datetime:
                end_datetime = datetime.combine(date.today() + timedelta(days=1), end_time)
            duration = (end_datetime - start_datetime).total_seconds() / 3600
            st.metric("Service Hours", f"{duration:.1f} hrs")
            service_hours = duration
        else:
            service_hours = 5.0
    
    # Budget
    st.markdown('<div class="section-header">💰 Budget</div>', unsafe_allow_html=True)
    
    budget_range = st.select_slider(
        "Estimated Budget *",
        options=["Under $500", "$500-$1,000", "$1,000-$2,000", "$2,000-$3,000", 
                 "$3,000-$5,000", "$5,000-$10,000", "Over $10,000"],
        value="$1,000-$2,000",
        help="Select your approximate budget range"
    )
    
    # Convert budget range to numeric value for database
    budget_map = {
        "Under $500": 500,
        "$500-$1,000": 1000,
        "$1,000-$2,000": 2000,
        "$2,000-$3,000": 3000,
        "$3,000-$5,000": 5000,
        "$5,000-$10,000": 10000,
        "Over $10,000": 15000
    }
    estimated_budget = budget_map.get(budget_range, 2000)
    
    # Additional Information
    st.markdown('<div class="section-header">📝 Additional Information</div>', unsafe_allow_html=True)
    
    description = st.text_area(
        "Event Description",
        placeholder="Tell us more about your event...",
        help="Provide any additional details about your event"
    )
    
    special_requirements = st.text_area(
        "Special Requirements",
        placeholder="Any special requests, themes, or requirements?",
        help="Let us know if you have any specific needs or preferences"
    )
    
    # Info box
    st.markdown("""
    <div class="info-box">
        <strong>💡 What happens next?</strong><br>
        1. We'll create your event request<br>
        2. Our professionals will review your requirements<br>
        3. You'll receive customized quotes within 24-48 hours<br>
        4. You can chat with professionals and accept the best quote
    </div>
    """, unsafe_allow_html=True)
    
    # Submit buttons
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        submit = st.form_submit_button("Submit Quote Request", type="primary", use_container_width=True)
    
    with col2:
        cancel = st.form_submit_button("Cancel", use_container_width=True)
    
    if cancel:
        st.switch_page("pages/14_Client_Dashboard.py")
    
    if submit:
        # Validation
        errors = []
        
        if not selected_services:
            errors.append("Please select at least one service")
        if not event_name:
            errors.append("Event name is required")
        if not event_type:
            errors.append("Event type is required")
        if not event_location:
            errors.append("Event address is required")
        if not event_date:
            errors.append("Event date is required")
        if end_time <= start_time:
            errors.append("End time must be after start time")
        
        # Display errors or proceed
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
        else:
            # Create event
            event_data = {
                'event_name': event_name,
                'event_type': event_type,
                'event_date': datetime.combine(event_date, start_time),
                'event_location': event_location,
                'start_time': start_time,
                'end_time': end_time,
                'service_hours': service_hours,
                'venue': venue if venue else None,
                'estimated_guest': estimated_guests,
                'estimated_budget': estimated_budget,
                'description': description if description else None,
                'special_requirements': special_requirements if special_requirements else None
            }
            
            success, event_id = client_manager.create_event(client_id, event_data)
            
            if success:
                # Link selected services to event
                service_ids = []
                for service_name in selected_services:
                    matching_service = next((s for s in services if s['service_name'] == service_name), None)
                    if matching_service:
                        service_ids.append(matching_service['service_id'])
                        client_manager.add_service_to_event(event_id, matching_service['service_id'])
                
                st.success("✅ Quote request submitted successfully!")
                st.balloons()
                
                st.info(f"""
                **Event Created:** {event_name}  
                **Event ID:** {event_id}  
                **Services Requested:** {', '.join(selected_services)}  
                **Date:** {event_date.strftime('%B %d, %Y')}  
                **Location:** {event_location}
                """)
                
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("View My Events", type="primary", use_container_width=True):
                        st.switch_page("pages/16_My_Events.py")
                
                with col2:
                    if st.button("Back to Dashboard", use_container_width=True):
                        st.switch_page("pages/14_Client_Dashboard.py")
            else:
                st.error("❌ Failed to create event. Please try again.")

st.markdown('</div>', unsafe_allow_html=True)

# Back button
if st.button("← Back to Dashboard"):
    st.switch_page("pages/14_Client_Dashboard.py")
