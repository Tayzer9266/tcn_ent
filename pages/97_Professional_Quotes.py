import streamlit as st
import os
import sys
from datetime import datetime, date, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client_manager import client_manager
from auth_utils import require_professional_auth

# Require professional authentication
require_professional_auth()

# Page configuration
st.set_page_config(
    page_title="Quote Requests",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# Manage Quote Requests"
    }
)

# Custom CSS
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
.page-header {
    background: linear-gradient(135deg, #457b9d 0%, #1d3557 100%);
    color: white;
    padding: 2em;
    border-radius: 15px;
    margin-bottom: 2em;
    text-align: center;
}
.page-title {
    font-size: 2.5em;
    font-weight: 700;
    margin-bottom: 0.3em;
}
.request-card {
    background: white;
    border-radius: 15px;
    padding: 1.5em;
    margin-bottom: 1.5em;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.request-header {
    border-bottom: 2px solid #e63946;
    padding-bottom: 0.8em;
    margin-bottom: 1em;
}
.request-title {
    font-size: 1.5em;
    font-weight: 700;
    color: #1d3557;
}
.client-info {
    background: #f8f9fa;
    border-radius: 10px;
    padding: 1em;
    margin: 1em 0;
}
.info-label {
    font-weight: 600;
    color: #457b9d;
}
.status-badge {
    display: inline-block;
    padding: 0.4em 1em;
    border-radius: 20px;
    font-size: 0.9em;
    font-weight: 600;
}
.status-pending {
    background: #ffd60a;
    color: #003566;
}
.status-sent {
    background: #06d6a0;
    color: #003566;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Check if user is logged in and is a professional
if not st.session_state.get('logged_in', False):
    st.error("⚠️ Please login to access quote requests")
    if st.button("Go to Login"):
        st.switch_page("pages/90_Login.py")
    st.stop()

if st.session_state.get('user_type') != 'professional':
    st.error("⚠️ This page is for professionals only")
    st.stop()

# Get professional data
professional_data = st.session_state.user_data
professional_id = professional_data.get('profile_id')
professional_name = professional_data.get('name')
professional_type = st.session_state.user_profile_type  # 'photographers', 'djs', 'event_coordinators'

# Map table name to professional type
type_map = {
    'photographers': 'photographer',
    'djs': 'dj',
    'event_coordinators': 'event_coordinator'
}
prof_type = type_map.get(professional_type, 'professional')

# Header
st.markdown(f"""
<div class="page-header">
    <div class="page-title">💼 Quote Requests</div>
    <div style="font-size: 1.2em; opacity: 0.9;">Manage client requests and send quotes</div>
</div>
""", unsafe_allow_html=True)

# Tabs for different views
tab1, tab2 = st.tabs(["📋 New Requests", "📤 My Quotes"])

with tab1:
    st.markdown("### 📋 Client Quote Requests")
    
    # Get all quote requests
    all_requests = client_manager.get_all_quote_requests()
    
    # Filter out past events
    if all_requests:
        today = date.today()
        active_requests = []
        past_count = 0
        
        for request in all_requests:
            event_date = request.get('event_date')
            include_event = False
            
            if event_date:
                # Convert to date if it's a datetime or string
                if isinstance(event_date, str):
                    try:
                        event_date = datetime.fromisoformat(event_date.replace('Z', '+00:00')).date()
                    except:
                        # If parsing fails, include the event
                        include_event = True
                elif isinstance(event_date, datetime):
                    event_date = event_date.date()
                elif isinstance(event_date, date):
                    # Already a date object
                    pass
                else:
                    # Unknown type, include the event
                    include_event = True
                
                # Only include events that haven't passed
                if not include_event:
                    if event_date >= today:
                        include_event = True
                    else:
                        past_count += 1
            else:
                # Include events without a date (TBD)
                include_event = True
            
            if include_event:
                active_requests.append(request)
        
        all_requests = active_requests
        
        # Sort by event date (earliest first - most recent upcoming event)
        def get_sort_date(request):
            event_date = request.get('event_date')
            if event_date:
                if isinstance(event_date, str):
                    try:
                        return datetime.fromisoformat(event_date.replace('Z', '+00:00'))
                    except:
                        return datetime.max
                elif isinstance(event_date, date) and not isinstance(event_date, datetime):
                    return datetime.combine(event_date, datetime.min.time())
                elif isinstance(event_date, datetime):
                    return event_date
            return datetime.max
        
        all_requests.sort(key=get_sort_date)
        
        # Show info about filtered events
        if past_count > 0:
            st.info(f"📊 Found {len(all_requests)} active quote requests ({past_count} past events hidden)")
        else:
            st.info(f"📊 Found {len(all_requests)} active quote requests")
    else:
        st.info("📭 No quote requests found in the database")
    
    if all_requests:
        for request in all_requests:
            event_id = request['event_id']
            
            # Check if this professional has already sent a quote
            existing_quotes = client_manager.get_event_quotes(event_id)
            has_quoted = any(q.get('professional_id') == professional_id for q in existing_quotes)
            
            st.markdown('<div class="request-card">', unsafe_allow_html=True)
            
            # Request header with event status
            event_status = request.get('event_status', 'pending')
            status_color = {
                'pending': '#ffd60a',
                'confirmed': '#06d6a0',
                'completed': '#457b9d',
                'cancelled': '#e63946'
            }.get(event_status.lower(), '#666')
            
            st.markdown(f"""
            <div class="request-header">
                <div class="request-title">{request.get('event_name', 'Untitled Event')} 
                    <span style="background: {status_color}; color: white; padding: 0.2em 0.8em; border-radius: 15px; font-size: 0.7em; margin-left: 0.5em;">{event_status.upper()}</span>
                </div>
                <div style="color: #666; font-size: 0.9em;">Event ID: {event_id} | Requested: {request.get('created_at', 'Unknown').strftime('%b %d, %Y') if isinstance(request.get('created_at'), datetime) else 'Unknown'}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Client information
            st.markdown('<div class="client-info">', unsafe_allow_html=True)
            st.markdown(f"**👤 Client:** {request.get('first_name')} {request.get('last_name')}")
            st.markdown(f"**📧 Email:** {request.get('email')}")
            st.markdown(f"**📞 Phone:** {request.get('phone_number', 'Not provided')}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Event details
            col1, col2, col3 = st.columns(3)
            
            with col1:
                event_date = request.get('event_date')
                if event_date:
                    if isinstance(event_date, str):
                        event_date = datetime.fromisoformat(event_date.replace('Z', '+00:00'))
                    formatted_date = event_date.strftime('%B %d, %Y')
                else:
                    formatted_date = "Date TBD"
                
                st.markdown(f"""
                <span class="info-label">📅 Date:</span> {formatted_date}<br>
                <span class="info-label">📍 Location:</span> {request.get('event_location', 'TBD')}<br>
                <span class="info-label">🎭 Type:</span> {request.get('event_type', 'General')}
                """, unsafe_allow_html=True)
            
            with col2:
                # Safely format budget
                budget = request.get('estimated_budget', 0)
                try:
                    budget_formatted = f"${float(budget):,.2f}" if budget else "TBD"
                except (ValueError, TypeError):
                    budget_formatted = "TBD"
                
                st.markdown(f"""
                <span class="info-label">👥 Guests:</span> {request.get('estimated_guest', 'TBD')}<br>
                <span class="info-label">⏱️ Hours:</span> {request.get('service_hours', 'TBD')}<br>
                <span class="info-label">💰 Budget:</span> {budget_formatted}
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <span class="info-label">🎵 Services:</span> {request.get('requested_services', 'Not specified')}<br>
                <span class="info-label">💬 Messages:</span> {request.get('message_count', 0)}<br>
                <span class="info-label">💰 Quotes:</span> {request.get('quote_count', 0)}
                """, unsafe_allow_html=True)
            
            # Description and requirements
            if request.get('description'):
                with st.expander("📝 Event Description"):
                    st.write(request.get('description'))
            
            if request.get('special_requirements'):
                with st.expander("⭐ Special Requirements"):
                    st.write(request.get('special_requirements'))
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Actions
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if has_quoted:
                    st.success("✅ You've already sent a quote for this event")
                else:
                    if st.button(f"💰 Send Quote", key=f"quote_{event_id}", use_container_width=True, type="primary"):
                        st.session_state.selected_event_for_quote = event_id
                        st.session_state.show_quote_form = True
                        st.rerun()
            
            with col2:
                if st.button(f"💬 Chat with Client", key=f"chat_{event_id}", use_container_width=True):
                    st.session_state.selected_event_id = event_id
                    st.session_state.professional_chat_mode = True
                    # Create a professional chat page or redirect
                    st.info("Chat feature: Navigate to event chat")
            
            with col3:
                if st.button(f"📋 View Details", key=f"details_{event_id}", use_container_width=True):
                    with st.expander(f"Full Event Details - {request.get('event_name')}", expanded=True):
                        st.json(request)
            
            st.markdown("---")
        
        # Quote form modal
        if st.session_state.get('show_quote_form', False):
            event_id = st.session_state.get('selected_event_for_quote')
            event = client_manager.get_event_by_id(event_id)
            
            if event:
                st.markdown("---")
                st.markdown(f"### 💰 Send Quote for: {event.get('event_name')}")
                
                with st.form(f"quote_form_{event_id}"):
                    st.markdown(f"**Client:** {event.get('first_name')} {event.get('last_name')}")
                    st.markdown(f"**Event:** {event.get('event_name')} on {event.get('event_date')}")
                    
                    quote_amount = st.number_input(
                        "Quote Amount ($) *",
                        min_value=0.0,
                        max_value=100000.0,
                        value=float(event.get('estimated_budget', 1000)),
                        step=50.0,
                        help="Enter your quote amount"
                    )
                    
                    quote_details = st.text_area(
                        "Quote Details *",
                        placeholder="Describe what's included in your quote...",
                        help="Provide details about services, equipment, hours, etc.",
                        height=150
                    )
                    
                    valid_until = st.date_input(
                        "Valid Until",
                        value=date.today() + timedelta(days=30),
                        min_value=date.today(),
                        help="How long is this quote valid?"
                    )
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        submit_quote = st.form_submit_button("📤 Send Quote", type="primary", use_container_width=True)
                    
                    with col2:
                        cancel_quote = st.form_submit_button("Cancel", use_container_width=True)
                    
                    if submit_quote:
                        if not quote_details:
                            st.error("Please provide quote details")
                        else:
                            quote_data = {
                                'quote_amount': quote_amount,
                                'quote_details': quote_details,
                                'valid_until': datetime.combine(valid_until, datetime.min.time())
                            }
                            
                            success, quote_id = client_manager.create_quote(
                                event_id=event_id,
                                professional_id=professional_id,
                                professional_type=prof_type,
                                professional_name=professional_name,
                                quote_data=quote_data
                            )
                            
                            if success:
                                st.success(f"✅ Quote sent successfully! Quote ID: {quote_id}")
                                st.balloons()
                                st.session_state.show_quote_form = False
                                st.session_state.selected_event_for_quote = None
                                st.rerun()
                            else:
                                st.error("❌ Failed to send quote. Please try again.")
                    
                    if cancel_quote:
                        st.session_state.show_quote_form = False
                        st.session_state.selected_event_for_quote = None
                        st.rerun()
    else:
        st.info("📭 No quote requests available at the moment")

with tab2:
    st.markdown("### 📤 My Sent Quotes")
    
    # Get quotes sent by this professional
    my_quotes = client_manager.get_professional_quotes(professional_id, prof_type)
    
    if my_quotes:
        st.success(f"📊 You've sent {len(my_quotes)} quotes")
        
        # Group by status
        pending_quotes = [q for q in my_quotes if q.get('quote_status') == 'sent']
        accepted_quotes = [q for q in my_quotes if q.get('quote_status') == 'accepted']
        rejected_quotes = [q for q in my_quotes if q.get('quote_status') == 'rejected']
        
        # Display statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Pending", len(pending_quotes))
        with col2:
            st.metric("Accepted", len(accepted_quotes))
        with col3:
            st.metric("Rejected", len(rejected_quotes))
        
        st.markdown("---")
        
        # Display quotes
        for quote in my_quotes:
            status = quote.get('quote_status', 'sent')
            status_class = f"status-{status}"
            
            st.markdown('<div class="request-card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Event:** {quote.get('event_name')}")
                st.markdown(f"**Client:** {quote.get('first_name')} {quote.get('last_name')}")
                st.markdown(f"**Amount:** ${quote.get('quote_amount', 0):,.2f}")
            
            with col2:
                st.markdown(f'<span class="status-badge {status_class}">{status.upper()}</span>', unsafe_allow_html=True)
            
            with st.expander("View Quote Details"):
                st.markdown(f"**Quote ID:** {quote.get('quote_id')}")
                st.markdown(f"**Event Date:** {quote.get('event_date')}")
                st.markdown(f"**Location:** {quote.get('event_location')}")
                st.markdown(f"**Client Email:** {quote.get('email')}")
                st.markdown(f"**Client Phone:** {quote.get('phone_number')}")
                st.markdown(f"**Sent:** {quote.get('created_at')}")
                st.markdown(f"**Valid Until:** {quote.get('valid_until')}")
                st.markdown(f"**Details:** {quote.get('quote_details')}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("📭 You haven't sent any quotes yet")

# Back button
st.markdown("---")
if st.button("← Back to Profile Management"):
    st.switch_page("pages/92_Profile_Management.py")
