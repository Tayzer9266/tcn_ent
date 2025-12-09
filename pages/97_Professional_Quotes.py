import streamlit as st
import os
import sys
from datetime import datetime, date, timedelta

# Page configuration - MUST be first
st.set_page_config(
    page_title="Quote Requests",
    page_icon="pages/images/TCN logo black.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "# Manage Quote Requests"
    }
)

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client_manager import client_manager
from auth_utils import require_professional_auth

# Require professional authentication
require_professional_auth()

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
user_role = professional_data.get('role', 'user')
is_admin = (user_role == 'admin')

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
    
    # Debug: Show total count before filtering
    if is_admin:
        if all_requests:
            st.info(f"🔍 Admin Debug: Found {len(all_requests)} total events in database before filtering")
        else:
            st.warning(f"🔍 Admin Debug: No events found in database. The events table may be empty.")
    
    # Filter by professional assignment (non-admin only)
    if not is_admin and all_requests:
        filtered_by_assignment = []
        
        # Get the professional's database ID from their profile_id
        # We need to look up their actual database ID
        professional_db_id = professional_data.get('id')  # This is the database ID
        
        # DEBUG: Show professional info
        st.warning(f"🔍 DEBUG - Professional Info: ID={professional_db_id}, Name={professional_name}, Type={professional_type}")
        st.warning(f"🔍 DEBUG - Professional Data: {professional_data}")
        
        # Map professional type to field name in events table
        assignment_field_map = {
            'djs': 'dj_id',
            'photographers': 'photographer_id',
            'event_coordinators': 'event_coordinator_id'
        }
        
        assignment_field = assignment_field_map.get(professional_type)
        
        # DEBUG: Show first few events with assignment info
        st.warning(f"🔍 DEBUG - Checking field: {assignment_field}")
        for idx, request in enumerate(all_requests[:3]):  # Show first 3 events
            assigned_id = request.get(assignment_field)
            st.warning(f"🔍 DEBUG - Event {idx+1}: event_id={request.get('event_id')}, {assignment_field}={assigned_id}, Match={assigned_id == professional_db_id}")
        
        for request in all_requests:
            assigned_id = request.get(assignment_field)
            
            # Include if:
            # 1. Not assigned to anyone (assigned_id is None or 0)
            # 2. Assigned to this specific professional
            if assigned_id is None or assigned_id == 0 or assigned_id == professional_db_id:
                filtered_by_assignment.append(request)
        
        all_requests = filtered_by_assignment
        
        # Show filtering info
        if filtered_by_assignment:
            assigned_to_me = [r for r in filtered_by_assignment if r.get(assignment_field) == professional_db_id]
            unassigned = [r for r in filtered_by_assignment if not r.get(assignment_field) or r.get(assignment_field) == 0]
            st.info(f"📊 Showing {len(filtered_by_assignment)} events: {len(assigned_to_me)} assigned to you, {len(unassigned)} unassigned")
        else:
            st.error(f"❌ No events found matching your ID ({professional_db_id}). This could mean no events are assigned to you or unassigned.")
    
    # Filter out past events FIRST (but admins can see all events)
    active_requests = []
    past_count = 0
    
    if all_requests:
        today = date.today()
        
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
                
                # Admins see all events, others only see future events
                if not include_event:
                    if is_admin or event_date >= today:
                        include_event = True
                    else:
                        past_count += 1
            else:
                # Include events without a date (TBD)
                include_event = True
            
            if include_event:
                active_requests.append(request)
    
    # Calculate status statistics AFTER filtering past events
    status_counts = {}
    if active_requests:
        for request in active_requests:
            status = request.get('event_status', 'pending').lower()
            status_counts[status] = status_counts.get(status, 0) + 1
    
    # Display status statistics
    if status_counts:
        st.markdown("### 📊 Event Status Statistics (Active Events)")
        stat_cols = st.columns(len(status_counts))
        for idx, (status, count) in enumerate(sorted(status_counts.items())):
            with stat_cols[idx]:
                status_color = {
                    'pending': '#ffd60a',
                    'confirmed': '#06d6a0',
                    'completed': '#457b9d',
                    'cancelled': '#e63946'
                }.get(status, '#666')
                st.markdown(f"""
                <div style="background: {status_color}; color: white; padding: 1em; border-radius: 10px; text-align: center;">
                    <div style="font-size: 2em; font-weight: 700;">{count}</div>
                    <div style="font-size: 0.9em; text-transform: uppercase;">{status}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Status filter
        st.markdown("### 🔍 Filter by Status")
        filter_col1, filter_col2 = st.columns([3, 1])
        
        # Initialize filter state if not exists
        if 'status_filter' not in st.session_state:
            st.session_state.status_filter = 'All'
        
        with filter_col1:
            status_options = ['All'] + [s.title() for s in sorted(status_counts.keys())]
            selected_status = st.selectbox(
                "Select Status to Display",
                options=status_options,
                index=status_options.index(st.session_state.status_filter) if st.session_state.status_filter in status_options else 0,
                key="status_selectbox",
                help="Filter events by their status"
            )
            # Update session state
            st.session_state.status_filter = selected_status
        
        with filter_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Reset Filter", use_container_width=True, key="reset_filter_btn"):
                st.session_state.status_filter = 'All'
                st.rerun()
        
        st.markdown("---")
    
    # Apply status filter if selected
    filtered_requests = active_requests
    if status_counts and selected_status != 'All':
        filtered_requests = [r for r in active_requests if r.get('event_status', 'pending').lower() == selected_status.lower()]
    
    # Use filtered_requests for display
    all_requests = filtered_requests
    
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
    filter_msg = f" with status '{selected_status}'" if status_counts and selected_status != 'All' else ""
    if past_count > 0:
        if is_admin:
            st.info(f"📊 Displaying {len(all_requests)} quote requests{filter_msg} (including all events - admin view)")
        else:
            st.info(f"📊 Displaying {len(all_requests)} active quote requests{filter_msg} ({past_count} past events hidden)")
    elif all_requests:
        st.info(f"📊 Displaying {len(all_requests)} quote requests{filter_msg}")
    else:
        if status_counts and selected_status != 'All':
            st.info(f"📭 No quote requests found with status '{selected_status}'")
        else:
            st.warning("📭 No quote requests found. This could mean:\n- No events have been created yet\n- All events have been deleted\n- There's a database connection issue")
    
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
            
            # Client Comments Section (from description field)
            st.markdown("---")
            st.markdown("**💬 Client Comments:**")
            client_comments = request.get('description', '')
            if client_comments:
                st.info(client_comments)
            else:
                st.caption("No comments provided by the client.")
            
            # Professional Notes Section (visible to all professionals, not clients)
            st.markdown("---")
            st.markdown("**📝 Professional Notes (Internal Use Only):**")
            st.caption("⚠️ These notes are only visible to professionals and will NOT be shown to clients.")
            
            # Get current notes
            current_notes = request.get('notes', '')
            
            # Text area for notes
            notes_text = st.text_area(
                "Add your personal notes about this quote/event:",
                value=current_notes if current_notes else "",
                key=f"notes_{event_id}",
                height=100,
                placeholder="Enter your notes here... (e.g., special considerations, follow-up items, pricing notes, etc.)",
                help="These notes are for professional use only and will not be visible to the client"
            )
            
            # Save button for notes
            if st.button("💾 Save Notes", key=f"save_notes_{event_id}", type="secondary"):
                success = client_manager.update_event_notes(
                    event_id=event_id,
                    notes=notes_text
                )
                if success:
                    st.success("✅ Notes saved successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to save notes")
            
            # Admin-only: Professional Assignments
            if is_admin:
                st.markdown("---")
                st.markdown("**👥 Assign Professionals (Admin Only):**")
                st.caption("Assign DJ, Photographer, and Event Coordinator to this event")
                
                # Get all professionals
                all_djs = client_manager.get_all_professionals('djs')
                all_photographers = client_manager.get_all_professionals('photographers')
                all_coordinators = client_manager.get_all_professionals('event_coordinators')
                
                # Get current assignments
                current_dj_id = request.get('dj_id')
                current_photographer_id = request.get('photographer_id')
                current_coordinator_id = request.get('event_coordinator_id')
                
                # Create dropdown options with "None" as first option
                dj_options = [{"id": 0, "name": "-- Not Assigned --"}] + all_djs
                photographer_options = [{"id": 0, "name": "-- Not Assigned --"}] + all_photographers
                coordinator_options = [{"id": 0, "name": "-- Not Assigned --"}] + all_coordinators
                
                # Find current index for each dropdown
                dj_index = 0
                if current_dj_id:
                    for idx, dj in enumerate(dj_options):
                        if dj['id'] == current_dj_id:
                            dj_index = idx
                            break
                
                photographer_index = 0
                if current_photographer_id:
                    for idx, photographer in enumerate(photographer_options):
                        if photographer['id'] == current_photographer_id:
                            photographer_index = idx
                            break
                
                coordinator_index = 0
                if current_coordinator_id:
                    for idx, coordinator in enumerate(coordinator_options):
                        if coordinator['id'] == current_coordinator_id:
                            coordinator_index = idx
                            break
                
                # Display current assignments
                if current_dj_id or current_photographer_id or current_coordinator_id:
                    st.info("**Current Assignments:**")
                    assign_col1, assign_col2, assign_col3 = st.columns(3)
                    with assign_col1:
                        if current_dj_id:
                            dj_name = client_manager.get_professional_name_by_id('djs', current_dj_id)
                            st.markdown(f"🎧 **DJ:** {dj_name or 'Unknown'}")
                        else:
                            st.markdown("🎧 **DJ:** Not assigned")
                    with assign_col2:
                        if current_photographer_id:
                            photographer_name = client_manager.get_professional_name_by_id('photographers', current_photographer_id)
                            st.markdown(f"📸 **Photographer:** {photographer_name or 'Unknown'}")
                        else:
                            st.markdown("📸 **Photographer:** Not assigned")
                    with assign_col3:
                        if current_coordinator_id:
                            coordinator_name = client_manager.get_professional_name_by_id('event_coordinators', current_coordinator_id)
                            st.markdown(f"📋 **Coordinator:** {coordinator_name or 'Unknown'}")
                        else:
                            st.markdown("📋 **Coordinator:** Not assigned")
                
                # Dropdowns for assignment
                prof_col1, prof_col2, prof_col3 = st.columns(3)
                
                with prof_col1:
                    selected_dj = st.selectbox(
                        "🎧 Assign DJ",
                        options=range(len(dj_options)),
                        format_func=lambda x: dj_options[x]['name'],
                        index=dj_index,
                        key=f"dj_select_{event_id}",
                        help="Select a DJ to assign to this event"
                    )
                
                with prof_col2:
                    selected_photographer = st.selectbox(
                        "📸 Assign Photographer",
                        options=range(len(photographer_options)),
                        format_func=lambda x: photographer_options[x]['name'],
                        index=photographer_index,
                        key=f"photographer_select_{event_id}",
                        help="Select a photographer to assign to this event"
                    )
                
                with prof_col3:
                    selected_coordinator = st.selectbox(
                        "📋 Assign Event Coordinator",
                        options=range(len(coordinator_options)),
                        format_func=lambda x: coordinator_options[x]['name'],
                        index=coordinator_index,
                        key=f"coordinator_select_{event_id}",
                        help="Select an event coordinator to assign to this event"
                    )
                
                # Update button for professional assignments
                if st.button("💾 Update Professional Assignments", key=f"update_professionals_{event_id}", type="primary"):
                    selected_dj_id = dj_options[selected_dj]['id']
                    selected_photographer_id = photographer_options[selected_photographer]['id']
                    selected_coordinator_id = coordinator_options[selected_coordinator]['id']
                    
                    success = client_manager.update_event_professionals(
                        event_id=event_id,
                        dj_id=selected_dj_id,
                        photographer_id=selected_photographer_id,
                        event_coordinator_id=selected_coordinator_id
                    )
                    if success:
                        st.success("✅ Professional assignments updated successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to update professional assignments")
                
                # Admin-only: Payment information
                st.markdown("---")
                st.markdown("**💳 Payment Information (Admin Only):**")
                
                # Get current values from request
                current_deposit_completed = request.get('deposit_completed', False)
                current_final_payment = request.get('payment_completed', False)
                
                deposit_col1, deposit_col2 = st.columns(2)
                
                with deposit_col1:
                    deposit_completed = st.checkbox(
                        "Deposit Paid", 
                        value=current_deposit_completed,
                        key=f"deposit_paid_{event_id}",
                        help="Has the client paid the deposit?"
                    )
                
                with deposit_col2:
                    final_payment_completed = st.checkbox(
                        "Final Payment Completed", 
                        value=current_final_payment,
                        key=f"final_payment_{event_id}",
                        help="Has the final payment been completed?"
                    )
                
                # Update button for payment fields
                if st.button("💾 Update Payment Status", key=f"update_payment_{event_id}", type="secondary"):
                    success = client_manager.update_event_deposit_status(
                        event_id=event_id,
                        deposit_completed=deposit_completed,
                        payment_completed=final_payment_completed
                    )
                    if success:
                        st.success("✅ Payment status updated successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to update payment status")
            
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
                    
                    # Safely get budget value
                    budget = event.get('estimated_budget', 1000)
                    try:
                        default_amount = float(budget) if budget else 1000.0
                    except (ValueError, TypeError):
                        default_amount = 1000.0
                    
                    quote_amount = st.number_input(
                        "Quote Amount ($) *",
                        min_value=0.0,
                        max_value=100000.0,
                        value=default_amount,
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
    
    # Get quotes sent by this professional (or all quotes if admin)
    my_quotes = client_manager.get_professional_quotes(professional_id, prof_type, is_admin=is_admin)
    
    if my_quotes:
        # Date Filter for Quotes
        st.markdown("### 🗓️ Filter by Event Date")
        filter_col1, filter_col2 = st.columns([3, 1])
        
        # Initialize date filter state if not exists
        if 'quote_date_filter' not in st.session_state:
            st.session_state.quote_date_filter = 'Future Events'
        
        with filter_col1:
            date_filter_options = ['All', 'Future Events', 'Past Events']
            selected_date_filter = st.selectbox(
                "Select Date Range to Display",
                options=date_filter_options,
                index=date_filter_options.index(st.session_state.quote_date_filter) if st.session_state.quote_date_filter in date_filter_options else 1,
                key="quote_date_selectbox",
                help="Filter quotes by event date"
            )
            # Update session state
            st.session_state.quote_date_filter = selected_date_filter
        
        with filter_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Reset Date Filter", use_container_width=True, key="reset_date_filter_btn"):
                st.session_state.quote_date_filter = 'Future Events'
                st.rerun()
        
        # Apply date filter based on event_date in quotes
        today = date.today()
        filtered_quotes = []
        
        for quote in my_quotes:
            event_date = quote.get('event_date')
            include_quote = False
            
            if event_date:
                # Convert to date if it's a datetime or string
                if isinstance(event_date, str):
                    try:
                        event_date = datetime.fromisoformat(event_date.replace('Z', '+00:00')).date()
                    except:
                        # If parsing fails, include based on filter
                        include_quote = (selected_date_filter == 'All')
                elif isinstance(event_date, datetime):
                    event_date = event_date.date()
                elif isinstance(event_date, date):
                    # Already a date object
                    pass
                else:
                    # Unknown type, include based on filter
                    include_quote = (selected_date_filter == 'All')
                
                # Apply filter logic
                if not include_quote:
                    if selected_date_filter == 'All':
                        include_quote = True
                    elif selected_date_filter == 'Future Events':
                        include_quote = (event_date >= today)
                    elif selected_date_filter == 'Past Events':
                        include_quote = (event_date < today)
            else:
                # Include quotes without event date only in "All" filter
                include_quote = (selected_date_filter == 'All')
            
            if include_quote:
                filtered_quotes.append(quote)
        
        # Use filtered quotes for display
        my_quotes = filtered_quotes
        
        st.markdown("---")
        
        if my_quotes:
            st.success(f"📊 Displaying {len(my_quotes)} quotes ({selected_date_filter})")
            
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
        else:
            st.info(f"📭 No quotes found for {selected_date_filter}")
        
        # Display quotes (only if we have filtered quotes)
        if my_quotes:
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
