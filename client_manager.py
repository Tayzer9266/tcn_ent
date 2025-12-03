"""
Client Manager - Handle client authentication and data management
"""

import streamlit as st
from sqlalchemy import create_engine, text
from datetime import datetime
import hashlib

class ClientManager:
    def __init__(self):
        self.engine = None
        self.conn = None
        self.init_connection()
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def init_connection(self):
        """Initialize PostgreSQL connection using Streamlit secrets"""
        try:
            db_config = st.secrets["postgres"]
            connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
            self.engine = create_engine(connection_string)
            self.conn = self.engine.connect()
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}")
            raise
    
    def register_client(self, first_name, last_name, email, phone_number, password):
        """
        Register a new client
        Returns: (success, message, client_id)
        """
        try:
            # Check if email already exists
            query = text('SELECT client_id FROM clients WHERE email = :email')
            result = self.conn.execute(query, {"email": email})
            existing = result.fetchone()
            
            if existing:
                return False, "Email already registered. Please login instead.", None
            
            # Hash password
            hashed_password = self.hash_password(password)
            
            # Insert new client
            query = text('''
                INSERT INTO clients (first_name, last_name, email, phone_number, password, user_type, is_active, created_at, updated_at)
                VALUES (:first_name, :last_name, :email, :phone_number, :password, 'client', TRUE, :created_at, :updated_at)
                RETURNING client_id
            ''')
            
            result = self.conn.execute(query, {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone_number": phone_number,
                "password": hashed_password,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            })
            
            client_id = result.fetchone()[0]
            self.conn.commit()
            
            return True, "Registration successful! You can now login.", client_id
            
        except Exception as e:
            print(f"Registration error: {e}")
            self.conn.rollback()
            return False, f"Registration failed: {str(e)}", None
    
    def authenticate_client(self, email, password):
        """
        Authenticate client login
        Returns: (success, client_data) or (False, None)
        """
        try:
            hashed_password = self.hash_password(password)
            
            query = text('''
                SELECT client_id, first_name, last_name, email, phone_number, user_type, is_active
                FROM clients
                WHERE email = :email AND password = :password AND is_active = TRUE
            ''')
            
            result = self.conn.execute(query, {"email": email, "password": hashed_password})
            row = result.fetchone()
            
            if row:
                client_data = {
                    'client_id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone_number': row[4],
                    'user_type': row[5],
                    'is_active': row[6]
                }
                return True, client_data
            
            return False, None
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return False, None
    
    def get_client_by_id(self, client_id):
        """Get client data by ID"""
        try:
            query = text('SELECT * FROM clients WHERE client_id = :client_id')
            result = self.conn.execute(query, {"client_id": client_id})
            row = result.fetchone()
            
            if row:
                return dict(row._mapping)
            return None
            
        except Exception as e:
            print(f"Error getting client: {e}")
            return None
    
    def update_client(self, client_id, data):
        """Update client information"""
        try:
            update_fields = []
            values = {"client_id": client_id}
            
            allowed_fields = ['first_name', 'last_name', 'phone_number', 'address', 'best_time_contact']
            
            for field in allowed_fields:
                if field in data:
                    update_fields.append(f"{field} = :{field}")
                    values[field] = data[field]
            
            if update_fields:
                update_fields.append("updated_at = :updated_at")
                values["updated_at"] = datetime.now()
                
                query = text(f"UPDATE clients SET {', '.join(update_fields)} WHERE client_id = :client_id")
                self.conn.execute(query, values)
                self.conn.commit()
                return True
            
            return False
            
        except Exception as e:
            print(f"Error updating client: {e}")
            self.conn.rollback()
            return False
    
    def get_client_events(self, client_id):
        """Get all events for a client"""
        try:
            query = text('''
                SELECT e.*, 
                       COUNT(DISTINCT q.quote_id) as quote_count,
                       COUNT(DISTINCT m.message_id) as message_count
                FROM events e
                LEFT JOIN quotes q ON e.event_id = q.event_id
                LEFT JOIN messages m ON e.event_id = m.event_id
                WHERE e.client_id = :client_id AND e.deleted_at IS NULL
                GROUP BY e.event_id
                ORDER BY e.event_date DESC
            ''')
            
            result = self.conn.execute(query, {"client_id": client_id})
            rows = result.fetchall()
            
            events = []
            for row in rows:
                event_dict = dict(row._mapping)
                events.append(event_dict)
            
            return events
            
        except Exception as e:
            print(f"Error getting client events: {e}")
            return []
    
    def create_event(self, client_id, event_data):
        """Create a new event for a client"""
        try:
            query = text('''
                INSERT INTO events (
                    client_id, event_name, event_type, event_date, event_location,
                    start_time, end_time, service_hours, venue, estimated_guest,
                    estimated_budget, description, special_requirements,
                    event_status, created_at, updated_at
                )
                VALUES (
                    :client_id, :event_name, :event_type, :event_date, :event_location,
                    :start_time, :end_time, :service_hours, :venue, :estimated_guest,
                    :estimated_budget, :description, :special_requirements,
                    'Pending', :created_at, :updated_at
                )
                RETURNING event_id
            ''')
            
            result = self.conn.execute(query, {
                "client_id": client_id,
                "event_name": event_data.get('event_name'),
                "event_type": event_data.get('event_type'),
                "event_date": event_data.get('event_date'),
                "event_location": event_data.get('event_location'),
                "start_time": event_data.get('start_time'),
                "end_time": event_data.get('end_time'),
                "service_hours": event_data.get('service_hours'),
                "venue": event_data.get('venue'),
                "estimated_guest": event_data.get('estimated_guest'),
                "estimated_budget": event_data.get('estimated_budget'),
                "description": event_data.get('description'),
                "special_requirements": event_data.get('special_requirements'),
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            })
            
            event_id = result.fetchone()[0]
            self.conn.commit()
            
            return True, event_id
            
        except Exception as e:
            print(f"Error creating event: {e}")
            self.conn.rollback()
            return False, None
    
    def add_service_to_event(self, event_id, service_id, quantity=1):
        """Link a service to an event"""
        try:
            query = text('''
                INSERT INTO event_services (event_id, service_id, quantity, created_at)
                VALUES (:event_id, :service_id, :quantity, :created_at)
            ''')
            
            self.conn.execute(query, {
                "event_id": event_id,
                "service_id": service_id,
                "quantity": quantity,
                "created_at": datetime.now()
            })
            
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"Error adding service to event: {e}")
            self.conn.rollback()
            return False
    
    def get_all_services(self):
        """Get all available services"""
        try:
            query = text('SELECT * FROM services ORDER BY service_name')
            result = self.conn.execute(query)
            rows = result.fetchall()
            
            services = []
            for row in rows:
                service_dict = dict(row._mapping)
                services.append(service_dict)
            
            return services
            
        except Exception as e:
            print(f"Error getting services: {e}")
            return []
    
    def get_event_quotes(self, event_id):
        """Get all quotes for an event"""
        try:
            query = text('''
                SELECT * FROM quotes 
                WHERE event_id = :event_id 
                ORDER BY created_at DESC
            ''')
            
            result = self.conn.execute(query, {"event_id": event_id})
            rows = result.fetchall()
            
            quotes = []
            for row in rows:
                quote_dict = dict(row._mapping)
                quotes.append(quote_dict)
            
            return quotes
            
        except Exception as e:
            print(f"Error getting quotes: {e}")
            return []
    
    def get_event_messages(self, event_id):
        """Get all messages for an event"""
        try:
            query = text('''
                SELECT * FROM messages 
                WHERE event_id = :event_id 
                ORDER BY created_at ASC
            ''')
            
            result = self.conn.execute(query, {"event_id": event_id})
            rows = result.fetchall()
            
            messages = []
            for row in rows:
                message_dict = dict(row._mapping)
                messages.append(message_dict)
            
            return messages
            
        except Exception as e:
            print(f"Error getting messages: {e}")
            return []
    
    def send_message(self, event_id, sender_id, sender_type, sender_name, message_text):
        """Send a message in an event chat"""
        try:
            query = text('''
                INSERT INTO messages (event_id, sender_id, sender_type, sender_name, message_text, created_at)
                VALUES (:event_id, :sender_id, :sender_type, :sender_name, :message_text, :created_at)
                RETURNING message_id
            ''')
            
            result = self.conn.execute(query, {
                "event_id": event_id,
                "sender_id": sender_id,
                "sender_type": sender_type,
                "sender_name": sender_name,
                "message_text": message_text,
                "created_at": datetime.now()
            })
            
            message_id = result.fetchone()[0]
            self.conn.commit()
            
            return True, message_id
            
        except Exception as e:
            print(f"Error sending message: {e}")
            self.conn.rollback()
            return False, None
    
    def mark_messages_as_read(self, event_id, sender_type):
        """Mark messages as read for a specific user type"""
        try:
            # Mark messages from the OTHER sender type as read
            other_type = 'professional' if sender_type == 'client' else 'client'
            
            query = text('''
                UPDATE messages 
                SET is_read = TRUE 
                WHERE event_id = :event_id AND sender_type = :other_type AND is_read = FALSE
            ''')
            
            self.conn.execute(query, {
                "event_id": event_id,
                "other_type": other_type
            })
            
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"Error marking messages as read: {e}")
            self.conn.rollback()
            return False
    
    def get_all_quote_requests(self):
        """Get all events that are quote requests (for professionals to view)"""
        try:
            query = text('''
                SELECT e.*, 
                       c.first_name, c.last_name, c.email, c.phone_number,
                       COUNT(DISTINCT q.quote_id) as quote_count,
                       COUNT(DISTINCT m.message_id) as message_count,
                       STRING_AGG(DISTINCT s.service_name, ', ') as requested_services
                FROM events e
                JOIN clients c ON e.client_id = c.client_id
                LEFT JOIN quotes q ON e.event_id = q.event_id
                LEFT JOIN messages m ON e.event_id = m.event_id
                LEFT JOIN event_services es ON e.event_id = es.event_id
                LEFT JOIN services s ON es.service_id = s.service_id
                WHERE e.deleted_at IS NULL
                GROUP BY e.event_id, c.client_id
                ORDER BY e.created_at DESC
            ''')
            
            result = self.conn.execute(query)
            rows = result.fetchall()
            
            events = []
            for row in rows:
                event_dict = dict(row._mapping)
                events.append(event_dict)
            
            return events
            
        except Exception as e:
            print(f"Error getting quote requests: {e}")
            return []
    
    def create_quote(self, event_id, professional_id, professional_type, professional_name, quote_data):
        """Create a new quote for an event"""
        try:
            from datetime import datetime, timedelta
            
            # Default valid until date (30 days from now)
            valid_until = quote_data.get('valid_until')
            if not valid_until:
                valid_until = datetime.now() + timedelta(days=30)
            
            query = text('''
                INSERT INTO quotes (
                    event_id, client_id, professional_id, professional_type, professional_name,
                    quote_amount, quote_status, quote_details, valid_until, created_at, updated_at
                )
                SELECT 
                    :event_id, e.client_id, :professional_id, :professional_type, :professional_name,
                    :quote_amount, 'sent', :quote_details, :valid_until, :created_at, :updated_at
                FROM events e
                WHERE e.event_id = :event_id
                RETURNING quote_id
            ''')
            
            result = self.conn.execute(query, {
                "event_id": event_id,
                "professional_id": professional_id,
                "professional_type": professional_type,
                "professional_name": professional_name,
                "quote_amount": quote_data.get('quote_amount'),
                "quote_details": quote_data.get('quote_details'),
                "valid_until": valid_until,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            })
            
            quote_id = result.fetchone()[0]
            self.conn.commit()
            
            return True, quote_id
            
        except Exception as e:
            print(f"Error creating quote: {e}")
            self.conn.rollback()
            return False, None
    
    def update_quote_status(self, quote_id, new_status):
        """Update the status of a quote"""
        try:
            query = text('''
                UPDATE quotes 
                SET quote_status = :new_status, updated_at = :updated_at
                WHERE quote_id = :quote_id
            ''')
            
            self.conn.execute(query, {
                "quote_id": quote_id,
                "new_status": new_status,
                "updated_at": datetime.now()
            })
            
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"Error updating quote status: {e}")
            self.conn.rollback()
            return False
    
    def get_professional_quotes(self, professional_id, professional_type):
        """Get all quotes sent by a specific professional"""
        try:
            query = text('''
                SELECT q.*, e.event_name, e.event_date, e.event_location,
                       c.first_name, c.last_name, c.email, c.phone_number
                FROM quotes q
                JOIN events e ON q.event_id = e.event_id
                JOIN clients c ON q.client_id = c.client_id
                WHERE q.professional_id = :professional_id 
                AND q.professional_type = :professional_type
                ORDER BY q.created_at DESC
            ''')
            
            result = self.conn.execute(query, {
                "professional_id": professional_id,
                "professional_type": professional_type
            })
            rows = result.fetchall()
            
            quotes = []
            for row in rows:
                quote_dict = dict(row._mapping)
                quotes.append(quote_dict)
            
            return quotes
            
        except Exception as e:
            print(f"Error getting professional quotes: {e}")
            return []
    
    def get_event_by_id(self, event_id):
        """Get a specific event by ID with client information"""
        try:
            query = text('''
                SELECT e.*, 
                       c.first_name, c.last_name, c.email, c.phone_number,
                       STRING_AGG(DISTINCT s.service_name, ', ') as requested_services
                FROM events e
                JOIN clients c ON e.client_id = c.client_id
                LEFT JOIN event_services es ON e.event_id = es.event_id
                LEFT JOIN services s ON es.service_id = s.service_id
                WHERE e.event_id = :event_id
                GROUP BY e.event_id, c.client_id
            ''')
            
            result = self.conn.execute(query, {"event_id": event_id})
            row = result.fetchone()
            
            if row:
                return dict(row._mapping)
            return None
            
        except Exception as e:
            print(f"Error getting event by ID: {e}")
            return None

# Initialize the client manager
client_manager = ClientManager()
