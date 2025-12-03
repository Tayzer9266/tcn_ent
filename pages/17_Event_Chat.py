import streamlit as st
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client_manager import client_manager

# Page configuration
st.set_page_config(
    page_title="Event Chat",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# Chat with Professionals"
    }
)

# Custom CSS
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f1ecec;
}
.chat-header {
    background: linear-gradient(135deg, #457b9d 0%, #1d3557 100%);
    color: white;
    padding: 1.5em;
    border-radius: 15px;
    margin-bottom: 1.5em;
}
.chat-title {
    font-size: 2em;
    font-weight: 700;
    margin-bottom: 0.3em;
}
.chat-subtitle {
    font-size: 1em;
    opacity: 0.9;
}
.event-info-card {
    background: white;
    border-radius: 10px;
    padding: 1.5em;
    margin-bottom: 1.5em;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}
.chat-container {
    background: white;
    border-radius: 15px;
    padding: 1.5em;
    margin-bottom: 1.5em;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    max-height: 600px;
    overflow-y: auto;
}
.message {
    margin-bottom: 1em;
    padding: 1em;
    border-radius: 10px;
    max-width: 70%;
}
.message-client {
    background: linear-gradient(135deg, #457b9d 0%, #1d3557 100%);
    color: white;
    margin-left: auto;
    text-align: right;
}
.message-professional {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    color: #333;
    margin-right: auto;
}
.message-sender {
    font-weight: 600;
    font-size: 0.9em;
    margin-bottom: 0.3em;
}
.message-text {
    font-size: 1em;
    line-height: 1.5;
}
.message-time {
    font-size: 0.8em;
    opacity: 0.7;
    margin-top: 0.3em;
}
.message-input-container {
    background: white;
    border-radius: 10px;
    padding: 1.5em;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}
.no-messages {
    text-align: center;
    padding: 3em;
    color: #666;
}
.info-label {
    font-weight: 600;
    color: #457b9d;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Check if user is logged in
if not st.session_state.get('logged_in', False):
    st.error("⚠️ Please login to access chat")
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

# Get selected event ID from session state or show event selector
selected_event_id = st.session_state.get('selected_event_id')

# Get all client events
events = client_manager.get_client_events(client_id)

if not events:
    st.warning("📭 You don't have any events yet. Request a quote to get started!")
    if st.button("Request Quote", type="primary"):
        st.switch_page("pages/15_Request_Quote.py")
    st.stop()

# Event selector
st.markdown('<div class="chat-header">', unsafe_allow_html=True)
st.markdown('<div class="chat-title">💬 Event Chat</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-subtitle">Communicate with professionals about your event</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Event selection
event_options = {f"{e['event_name']} (ID: {e['event_id']})": e['event_id'] for e in events}
selected_event_name = st.selectbox(
    "Select Event",
    options=list(event_options.keys()),
    index=0 if not selected_event_id else list(event_options.values()).index(selected_event_id) if selected_event_id in event_options.values() else 0
)

selected_event_id = event_options[selected_event_name]
st.session_state.selected_event_id = selected_event_id

# Get event details
event = next((e for e in events if e['event_id'] == selected_event_id), None)

if not event:
    st.error("Event not found")
    st.stop()

# Display event information
st.markdown('<div class="event-info-card">', unsafe_allow_html=True)
st.markdown(f"### 🎉 {event['event_name']}")

col1, col2, col3 = st.columns(3)

with col1:
    event_date = event.get('event_date')
    if event_date:
        if isinstance(event_date, str):
            event_date = datetime.fromisoformat(event_date.replace('Z', '+00:00'))
        formatted_date = event_date.strftime('%B %d, %Y')
    else:
        formatted_date = "Date TBD"
    
    st.markdown(f"""
    <span class="info-label">📅 Date:</span> {formatted_date}<br>
    <span class="info-label">📍 Location:</span> {event.get('event_location', 'TBD')}<br>
    <span class="info-label">🎭 Type:</span> {event.get('event_type', 'General')}
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <span class="info-label">👥 Guests:</span> {event.get('estimated_guest', 'TBD')}<br>
    <span class="info-label">⏱️ Duration:</span> {event.get('service_hours', 'TBD')} hours<br>
    <span class="info-label">💰 Budget:</span> ${event.get('estimated_budget', 0):,.2f}
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <span class="info-label">📊 Status:</span> {event.get('event_status', 'pending').upper()}<br>
    <span class="info-label">💬 Messages:</span> {event.get('message_count', 0)}<br>
    <span class="info-label">💰 Quotes:</span> {event.get('quote_count', 0)}
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Get messages for this event
messages = client_manager.get_event_messages(selected_event_id)

# Mark messages as read for client
client_manager.mark_messages_as_read(selected_event_id, 'client')

# Display messages
st.markdown("### 💬 Conversation")

if messages:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for msg in messages:
        sender_type = msg.get('sender_type', 'client')
        sender_name = msg.get('sender_name', 'Unknown')
        message_text = msg.get('message_text', '')
        created_at = msg.get('created_at')
        
        if created_at:
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            time_str = created_at.strftime('%b %d, %Y at %I:%M %p')
        else:
            time_str = "Unknown time"
        
        message_class = f"message-{sender_type}"
        
        st.markdown(f"""
        <div class="message {message_class}">
            <div class="message-sender">{sender_name}</div>
            <div class="message-text">{message_text}</div>
            <div class="message-time">{time_str}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="no-messages">
        <h3>📭 No messages yet</h3>
        <p>Start the conversation by sending a message below!</p>
    </div>
    """, unsafe_allow_html=True)

# Message input
st.markdown('<div class="message-input-container">', unsafe_allow_html=True)
st.markdown("### ✍️ Send a Message")

with st.form("message_form", clear_on_submit=True):
    message_text = st.text_area(
        "Your Message",
        placeholder="Type your message here...",
        height=100,
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        send_button = st.form_submit_button("📤 Send Message", type="primary", use_container_width=True)
    
    with col2:
        refresh_button = st.form_submit_button("🔄 Refresh", use_container_width=True)
    
    with col3:
        back_button = st.form_submit_button("← Back", use_container_width=True)
    
    if send_button:
        if message_text.strip():
            success, message_id = client_manager.send_message(
                event_id=selected_event_id,
                sender_id=client_id,
                sender_type='client',
                sender_name=client_name,
                message_text=message_text.strip()
            )
            
            if success:
                st.success("✅ Message sent!")
                st.rerun()
            else:
                st.error("❌ Failed to send message. Please try again.")
        else:
            st.warning("⚠️ Please enter a message")
    
    if refresh_button:
        st.rerun()
    
    if back_button:
        st.switch_page("pages/16_My_Events.py")

st.markdown('</div>', unsafe_allow_html=True)

# Additional actions
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 View Event Details", use_container_width=True):
        st.switch_page("pages/16_My_Events.py")

with col2:
    if st.button("💰 View Quotes", use_container_width=True):
        quotes = client_manager.get_event_quotes(selected_event_id)
        if quotes:
            with st.expander("💰 Quotes for this Event", expanded=True):
                for quote in quotes:
                    st.markdown(f"""
                    ---
                    **Professional:** {quote.get('professional_name', 'Unknown')}  
                    **Type:** {quote.get('professional_type', 'Service')}  
                    **Amount:** ${quote.get('quote_amount', 0):,.2f}  
                    **Status:** {quote.get('quote_status', 'pending').upper()}  
                    **Details:** {quote.get('quote_details', 'No details provided')}  
                    **Valid Until:** {quote.get('valid_until', 'Not specified')}
                    """)
        else:
            st.info("No quotes received yet for this event")

with col3:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/14_Client_Dashboard.py")

# Tips section
with st.expander("💡 Chat Tips"):
    st.markdown("""
    **How to use the chat:**
    - Send messages to communicate with professionals about your event
    - Ask questions about services, pricing, availability, etc.
    - Discuss event details and special requirements
    - Professionals will respond to your messages
    - Check back regularly for responses
    
    **Best Practices:**
    - Be clear and specific in your messages
    - Provide all relevant details about your event
    - Respond promptly to professional inquiries
    - Keep the conversation professional and courteous
    """)
