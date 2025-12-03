import streamlit as st
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client_manager import client_manager

# Page configuration
st.set_page_config(
    page_title="My Events",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# Manage Your Events"
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
.page-subtitle {
    font-size: 1.2em;
    opacity: 0.9;
}
.event-card {
    background: white;
    border-radius: 15px;
    padding: 1.5em;
    margin-bottom: 1.5em;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}
.event-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 25px rgba(230,57,70,0.2);
}
.event-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1em;
    padding-bottom: 0.8em;
    border-bottom: 2px solid #e63946;
}
.event-title {
    font-size: 1.5em;
    font-weight: 700;
    color: #1d3557;
}
.event-id {
    font-size: 0.9em;
    color: #666;
    font-weight: 500;
}
.event-detail {
    margin: 0.5em 0;
    color: #333;
}
.event-detail-label {
    font-weight: 600;
    color: #457b9d;
}
.status-badge {
    display: inline-block;
    padding: 0.4em 1em;
    border-radius: 20px;
    font-size: 0.9em;
    font-weight: 600;
    text-transform: uppercase;
}
.status-pending {
    background: #ffd60a;
    color: #003566;
}
.status-confirmed {
    background: #06d6a0;
    color: #003566;
}
.status-completed {
    background: #457b9d;
    color: white;
}
.status-cancelled {
    background: #e63946;
    color: white;
}
.filter-section {
    background: white;
    border-radius: 10px;
    padding: 1em;
    margin-bottom: 2em;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}
.no-events {
    text-align: center;
    padding: 3em;
    background: white;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Check if user is logged in and is a client
if not st.session_state.get('logged_in', False):
    st.error("⚠️ Please login to view your events")
    if st.button("Go to Login"):
        st.switch_page("pages/1_Login.py")
    st.stop()

if st.session_state.get('user_type') != 'client':
    st.error("⚠️ This page is for clients only")
    st.stop()

# Get client data
client_data = st.session_state.user_data
client_id = client_data['client_id']
client_name = f"{client_data['first_name']} {client_data['last_name']}"

# Header
st.markdown(f"""
<div class="page-header">
    <div class="page-title">🎉 My Events</div>
    <div class="page-subtitle">View and manage all your event bookings</div>
</div>
""", unsafe_allow_html=True)

# Get all events
all_events = client_manager.get_client_events(client_id)

# Filter section
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

with col1:
    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Pending", "Confirmed", "Completed", "Cancelled"],
        key="status_filter"
    )

with col2:
    sort_order = st.selectbox(
        "Sort by Date",
        ["Newest First", "Oldest First", "Event Date (Upcoming)", "Event Date (Past)"],
        key="sort_order"
    )

with col3:
    search_term = st.text_input("Search Events", placeholder="Search by name or location", key="search")

with col4:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Filter events
filtered_events = all_events

# Apply status filter
if status_filter != "All":
    filtered_events = [e for e in filtered_events if e.get('event_status', '').lower() == status_filter.lower()]

# Apply search filter
if search_term:
    search_lower = search_term.lower()
    filtered_events = [e for e in filtered_events 
                      if search_lower in e.get('event_name', '').lower() 
                      or search_lower in e.get('event_location', '').lower()]

# Apply sorting
if sort_order == "Newest First":
    filtered_events = sorted(filtered_events, key=lambda x: x.get('created_at', datetime.min), reverse=True)
elif sort_order == "Oldest First":
    filtered_events = sorted(filtered_events, key=lambda x: x.get('created_at', datetime.min))
elif sort_order == "Event Date (Upcoming)":
    filtered_events = sorted(filtered_events, key=lambda x: x.get('event_date', datetime.max))
elif sort_order == "Event Date (Past)":
    filtered_events = sorted(filtered_events, key=lambda x: x.get('event_date', datetime.max), reverse=True)

# Display events
if filtered_events:
    st.markdown(f"### Found {len(filtered_events)} event(s)")
    
    for event in filtered_events:
        status = event.get('event_status', 'pending')
        status_class = f"status-{status}" if status in ['pending', 'confirmed', 'completed', 'cancelled'] else "status-pending"
        
        # Format event date
        event_date = event.get('event_date')
        if event_date:
            if isinstance(event_date, str):
                event_date = datetime.fromisoformat(event_date.replace('Z', '+00:00'))
            formatted_date = event_date.strftime('%B %d, %Y at %I:%M %p')
            date_display = formatted_date
        else:
            date_display = "Date TBD"
        
        # Format times
        start_time = event.get('start_time')
        end_time = event.get('end_time')
        if start_time and end_time:
            time_display = f"{start_time} - {end_time}"
        else:
            time_display = "Time TBD"
        
        st.markdown(f"""
        <div class="event-card">
            <div class="event-header">
                <div>
                    <div class="event-title">{event.get('event_name', 'Untitled Event')}</div>
                    <div class="event-id">Event ID: {event.get('event_id')}</div>
                </div>
                <span class="status-badge {status_class}">{status}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Event details in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="event-detail">
                <span class="event-detail-label">📅 Date:</span> {date_display}
            </div>
            <div class="event-detail">
                <span class="event-detail-label">⏰ Time:</span> {time_display}
            </div>
            <div class="event-detail">
                <span class="event-detail-label">📍 Location:</span> {event.get('event_location', 'Location TBD')}
            </div>
            """, unsafe_allow_html=True)
            
            if event.get('venue'):
                st.markdown(f"""
                <div class="event-detail">
                    <span class="event-detail-label">🏛️ Venue:</span> {event.get('venue')}
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="event-detail">
                <span class="event-detail-label">🎭 Type:</span> {event.get('event_type', 'General Event')}
            </div>
            <div class="event-detail">
                <span class="event-detail-label">👥 Guests:</span> {event.get('estimated_guest', 'TBD')}
            </div>
            <div class="event-detail">
                <span class="event-detail-label">⏱️ Duration:</span> {event.get('service_hours', 'TBD')} hours
            </div>
            <div class="event-detail">
                <span class="event-detail-label">💰 Budget:</span> ${event.get('estimated_budget', 0):,.2f}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Event statistics and actions
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💬 Messages", event.get('message_count', 0))
        
        with col2:
            st.metric("💰 Quotes", event.get('quote_count', 0))
        
        with col3:
            if st.button("📋 View Details", key=f"details_{event['event_id']}", use_container_width=True):
                st.session_state.selected_event_id = event['event_id']
                # Show event details in expander
                with st.expander(f"Event Details - {event.get('event_name')}", expanded=True):
                    if event.get('description'):
                        st.markdown(f"**Description:**\n{event.get('description')}")
                    if event.get('special_requirements'):
                        st.markdown(f"**Special Requirements:**\n{event.get('special_requirements')}")
                    
                    # Get quotes for this event
                    quotes = client_manager.get_event_quotes(event['event_id'])
                    if quotes:
                        st.markdown("### 💰 Quotes Received")
                        for quote in quotes:
                            st.markdown(f"""
                            **{quote.get('professional_name', 'Professional')}** ({quote.get('professional_type', 'Service')})  
                            Amount: ${quote.get('quote_amount', 0):,.2f}  
                            Status: {quote.get('quote_status', 'pending')}  
                            Details: {quote.get('quote_details', 'No details provided')}
                            """)
                    else:
                        st.info("No quotes received yet")
        
        with col4:
            if st.button("💬 Chat", key=f"chat_{event['event_id']}", use_container_width=True):
                st.session_state.selected_event_id = event['event_id']
                st.switch_page("pages/17_Event_Chat.py")
        
        st.markdown("---")

else:
    # No events found
    st.markdown("""
    <div class="no-events">
        <h2>📭 No Events Found</h2>
        <p>You don't have any events matching your filters.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if status_filter != "All" or search_term:
        if st.button("Clear Filters"):
            st.session_state.status_filter = "All"
            st.session_state.search = ""
            st.rerun()

# Action buttons
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("← Back to Dashboard", use_container_width=True):
        st.switch_page("pages/14_Client_Dashboard.py")

with col2:
    if st.button("📋 Request New Quote", type="primary", use_container_width=True):
        st.switch_page("pages/15_Request_Quote.py")

with col3:
    if st.button("🔄 Refresh Events", use_container_width=True):
        st.rerun()

# Summary statistics
if all_events:
    st.markdown("---")
    st.markdown("### 📊 Event Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Events", len(all_events))
    
    with col2:
        pending = len([e for e in all_events if e.get('event_status') == 'pending'])
        st.metric("Pending", pending)
    
    with col3:
        confirmed = len([e for e in all_events if e.get('event_status') == 'confirmed'])
        st.metric("Confirmed", confirmed)
    
    with col4:
        total_budget = sum(e.get('estimated_budget', 0) for e in all_events)
        st.metric("Total Budget", f"${total_budget:,.2f}")
