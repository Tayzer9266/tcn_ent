import streamlit as st
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client_manager import client_manager

# Page configuration
st.set_page_config(
    page_title="Client Dashboard",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# TCN Entertainment Client Dashboard"
    }
)

# Custom CSS
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
.dashboard-header {
    background: linear-gradient(135deg, #457b9d 0%, #1d3557 100%);
    color: white;
    padding: 2em;
    border-radius: 15px;
    margin-bottom: 2em;
    text-align: center;
}
.dashboard-title {
    font-size: 2.5em;
    font-weight: 700;
    margin-bottom: 0.3em;
}
.dashboard-subtitle {
    font-size: 1.2em;
    opacity: 0.9;
}
.stat-card {
    background: white;
    border-radius: 10px;
    padding: 1.5em;
    box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    text-align: center;
    transition: transform 0.2s;
}
.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 20px rgba(230,57,70,0.2);
}
.stat-number {
    font-size: 3em;
    font-weight: 700;
    color: #e63946;
    margin: 0.2em 0;
}
.stat-label {
    font-size: 1.1em;
    color: #666;
    font-weight: 500;
}
.action-card {
    background: white;
    border-radius: 10px;
    padding: 1.5em;
    box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    margin-bottom: 1em;
}
.section-title {
    font-size: 1.5em;
    font-weight: 700;
    color: #457b9d;
    margin-bottom: 1em;
    border-bottom: 3px solid #e63946;
    padding-bottom: 0.5em;
}
.event-card {
    background: linear-gradient(90deg, #f8fafc 70%, #D9D4D2 100%);
    border-radius: 10px;
    padding: 1em;
    margin-bottom: 1em;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.event-title {
    font-size: 1.2em;
    font-weight: 600;
    color: #1d3557;
    margin-bottom: 0.5em;
}
.event-detail {
    color: #666;
    margin: 0.3em 0;
}
.status-badge {
    display: inline-block;
    padding: 0.3em 0.8em;
    border-radius: 20px;
    font-size: 0.9em;
    font-weight: 600;
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
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Check if user is logged in and is a client
if not st.session_state.get('logged_in', False):
    st.error("⚠️ Please login to access the dashboard")
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
<div class="dashboard-header">
    <div class="dashboard-title">👋 Welcome, {client_data['first_name']}!</div>
    <div class="dashboard-subtitle">Manage your events, quotes, and communications</div>
</div>
""", unsafe_allow_html=True)

# Get client events and statistics
events = client_manager.get_client_events(client_id)
total_events = len(events)
pending_events = len([e for e in events if e.get('event_status') == 'pending'])
confirmed_events = len([e for e in events if e.get('event_status') == 'confirmed'])

# Calculate total quotes and messages
total_quotes = sum(e.get('quote_count', 0) for e in events)
total_messages = sum(e.get('message_count', 0) for e in events)

# Statistics Cards
st.markdown('<div class="section-title">📊 Your Overview</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Total Events</div>
        <div class="stat-number">{total_events}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Pending Events</div>
        <div class="stat-number">{pending_events}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Quotes Received</div>
        <div class="stat-number">{total_quotes}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Messages</div>
        <div class="stat-number">{total_messages}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Quick Actions
st.markdown('<div class="section-title">⚡ Quick Actions</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="action-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Request a Quote")
    st.markdown("Get quotes for DJ, Photography, or Event Coordination services")
    if st.button("Request Quote", type="primary", use_container_width=True, key="req_quote"):
        st.switch_page("pages/15_Request_Quote.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="action-card">', unsafe_allow_html=True)
    st.markdown("### 🎉 My Events")
    st.markdown("View and manage all your events and bookings")
    if st.button("View Events", type="primary", use_container_width=True, key="view_events"):
        st.switch_page("pages/16_My_Events.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="action-card">', unsafe_allow_html=True)
    st.markdown("### 💬 Messages")
    st.markdown("Chat with professionals about your events")
    if st.button("View Messages", type="primary", use_container_width=True, key="view_messages"):
        if events:
            st.switch_page("pages/17_Event_Chat.py")
        else:
            st.info("No events yet. Request a quote to get started!")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Recent Events
st.markdown('<div class="section-title">📅 Recent Events</div>', unsafe_allow_html=True)

if events:
    # Show up to 3 most recent events
    recent_events = sorted(events, key=lambda x: x.get('created_at', datetime.min), reverse=True)[:3]
    
    for event in recent_events:
        status = event.get('event_status', 'pending')
        status_class = f"status-{status}" if status in ['pending', 'confirmed', 'completed'] else "status-pending"
        
        event_date = event.get('event_date')
        if event_date:
            if isinstance(event_date, str):
                event_date = datetime.fromisoformat(event_date.replace('Z', '+00:00'))
            formatted_date = event_date.strftime('%B %d, %Y')
        else:
            formatted_date = "Date TBD"
        
        st.markdown(f"""
        <div class="event-card">
            <div class="event-title">{event.get('event_name', 'Untitled Event')}</div>
            <div class="event-detail">📍 {event.get('event_location', 'Location TBD')}</div>
            <div class="event-detail">📅 {formatted_date}</div>
            <div class="event-detail">🎭 {event.get('event_type', 'General Event')}</div>
            <div class="event-detail">
                <span class="status-badge {status_class}">{status.upper()}</span>
                &nbsp;&nbsp;
                💬 {event.get('message_count', 0)} messages
                &nbsp;&nbsp;
                💰 {event.get('quote_count', 0)} quotes
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(f"View Details", key=f"details_{event['event_id']}", use_container_width=True):
                st.session_state.selected_event_id = event['event_id']
                st.switch_page("pages/17_Event_Chat.py")
        with col2:
            if event.get('quote_count', 0) > 0:
                if st.button(f"View Quotes ({event.get('quote_count', 0)})", key=f"quotes_{event['event_id']}", use_container_width=True):
                    st.session_state.selected_event_id = event['event_id']
                    st.switch_page("pages/16_My_Events.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if len(events) > 3:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("View All Events", type="secondary", use_container_width=True):
                st.switch_page("pages/16_My_Events.py")
else:
    st.info("🎉 No events yet! Click 'Request Quote' above to get started with your first event.")
    st.markdown("""
    ### Getting Started
    
    1. **Request a Quote** - Tell us about your event and what services you need
    2. **Receive Quotes** - Our professionals will send you customized quotes
    3. **Chat & Coordinate** - Communicate directly with professionals about your event
    4. **Book & Enjoy** - Accept a quote and let us make your event amazing!
    """)

# Account Information
st.markdown("---")
st.markdown('<div class="section-title">👤 Account Information</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    **Name:** {client_name}  
    **Email:** {client_data['email']}  
    **Phone:** {client_data.get('phone_number', 'Not provided')}
    """)

with col2:
    if st.button("Logout", type="secondary", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.session_state.user_data = None
        st.session_state.user_profile_type = None
        st.session_state.user_type = None
        st.success("Logged out successfully!")
        st.switch_page("pages/1_Login.py")
