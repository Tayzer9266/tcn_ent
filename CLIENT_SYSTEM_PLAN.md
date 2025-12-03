# Client Login & Quote Management System - Implementation Plan

## Overview
Create a comprehensive client portal system that allows clients to:
1. Register and login
2. Request quotes for services
3. Communicate with professionals via chat
4. Track their events and quotes

## Database Analysis

### Existing Tables (Already in Database)
1. **clients** - Client information
   - client_id (PK)
   - first_name, last_name, email, phone_number
   - address, created_at, updated_at
   - best_time_contact, deleted_at

2. **events** - Event details
   - event_id (PK)
   - client_id (FK)
   - event_name, event_type, event_date
   - event_location, start_time, end_time
   - service_hours, venue
   - estimated_budget, actual_cost
   - event_status, billing_status
   - description, special_requirements

3. **services** - Available services
   - service_id (PK)
   - service_name, service_description
   - price, market_price
   - professional_id

4. **event_services** - Services linked to events
   - event_service_id (PK)
   - event_id (FK), service_id (FK)
   - quantity

### New Tables/Fields Needed

1. **clients table - ADD FIELDS:**
   - `password` VARCHAR(255) - Hashed password for login
   - `user_type` VARCHAR(20) DEFAULT 'client' - To distinguish from professionals
   - `is_active` BOOLEAN DEFAULT TRUE - Account status

2. **quotes table - NEW TABLE:**
   - `quote_id` SERIAL PRIMARY KEY
   - `event_id` INTEGER REFERENCES events(event_id)
   - `client_id` INTEGER REFERENCES clients(client_id)
   - `professional_id` INTEGER - Reference to professional
   - `professional_type` VARCHAR(50) - 'photographer', 'dj', 'event_coordinator'
   - `quote_amount` NUMERIC(10,2)
   - `quote_status` VARCHAR(50) - 'pending', 'sent', 'accepted', 'rejected'
   - `quote_details` TEXT
   - `valid_until` TIMESTAMP
   - `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   - `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

3. **messages table - NEW TABLE:**
   - `message_id` SERIAL PRIMARY KEY
   - `event_id` INTEGER REFERENCES events(event_id)
   - `sender_id` INTEGER - Can be client_id or professional_id
   - `sender_type` VARCHAR(20) - 'client' or 'professional'
   - `message_text` TEXT
   - `is_read` BOOLEAN DEFAULT FALSE
   - `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

## Implementation Steps

### Phase 1: Database Setup
1. ✅ Inspect existing tables (DONE)
2. Add password field to clients table
3. Create quotes table
4. Create messages table
5. Populate services table with DJ, Photographer, Event Coordinator services

### Phase 2: Client Authentication System
1. Update profiles_data.py to include ClientManager class
2. Add client registration functionality
3. Add client login functionality
4. Update Login page to support both professional and client login

### Phase 3: Client Registration Page
1. Create new page: pages/2_Client_Registration.py
2. Form fields:
   - First Name
   - Last Name
   - Email
   - Phone Number
   - Password
   - Confirm Password
3. Validation and account creation

### Phase 4: Client Dashboard
1. Create new page: pages/14_Client_Dashboard.py
2. Display:
   - Welcome message
   - Active events/quotes
   - Recent messages
   - Quick actions (Request Quote, View Events)

### Phase 5: Quote Request System
1. Create new page: pages/15_Request_Quote.py
2. Form fields:
   - Service Type (DJ, Photographer, Event Coordinator)
   - Event Type (Wedding, Birthday, Corporate, etc.)
   - Event Date
   - Event Location
   - Number of Hours
   - Number of Guests
   - Budget Range
   - Special Requirements
3. Create event and link to client

### Phase 6: Client Event Management
1. Create new page: pages/16_My_Events.py
2. Display all client events
3. Show event details, status, quotes
4. Access to chat for each event

### Phase 7: Chat/Messaging System
1. Create new page: pages/17_Event_Chat.py
2. Display messages for specific event
3. Allow client to send messages
4. Allow professional to respond
5. Real-time or refresh-based updates

### Phase 8: Professional Quote Management
1. Update pages/13_Profile_Management.py
2. Add section for professionals to:
   - View quote requests
   - Send quotes to clients
   - Respond to messages

### Phase 9: Quote Display & Management
1. Create quote viewing interface for clients
2. Allow clients to accept/reject quotes
3. Track quote status

## File Structure

### New Files to Create:
1. `client_manager.py` - Client authentication and management
2. `pages/2_Client_Registration.py` - Client signup
3. `pages/14_Client_Dashboard.py` - Client home page
4. `pages/15_Request_Quote.py` - Quote request form
5. `pages/16_My_Events.py` - Client event list
6. `pages/17_Event_Chat.py` - Messaging interface
7. `pages/18_Professional_Quotes.py` - Professional quote management
8. `init_client_tables.py` - Database setup script
9. `CLIENT_SYSTEM_IMPLEMENTATION.md` - Documentation

### Files to Modify:
1. `profiles_data.py` - Add client authentication
2. `pages/1_Login.py` - Support client login
3. `pages/13_Profile_Management.py` - Add quote management for professionals

## Features Summary

### For Clients:
- ✅ Register account with email, name, phone
- ✅ Login to personal dashboard
- ✅ Request quotes for services
- ✅ Select service type (DJ, Photographer, Event Coordinator)
- ✅ Specify event details (date, location, hours, guests)
- ✅ View all their events and quotes
- ✅ Chat with professionals about events
- ✅ Accept/reject quotes
- ✅ Track event status

### For Professionals:
- ✅ View incoming quote requests
- ✅ Send quotes to clients
- ✅ Chat with clients about events
- ✅ Update quote status
- ✅ Manage multiple client conversations

## Security Considerations
1. Password hashing (SHA256 or bcrypt)
2. Session management
3. Input validation
4. SQL injection prevention (using parameterized queries)
5. Access control (clients can only see their own data)

## Next Steps
1. Get user confirmation on the plan
2. Start with Phase 1: Database Setup
3. Proceed through phases sequentially
4. Test each phase before moving to next
