import streamlit as st
import hashlib
import sqlite3
import os
from datetime import datetime, timedelta
import jwt
import bcrypt

class AuthSystem:
    def __init__(self):
        self.secret_key = os.environ.get("JWT_SECRET_KEY", "your-super-secret-key-change-in-production")
        self.db_path = "auth.db"
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Create sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_token TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create default admin user if not exists
        cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',))
        if not cursor.fetchone():
            default_password = self.hash_password("admin123")
            cursor.execute(
                'INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)',
                ('admin', default_password, 'admin@tcnent.com')
            )
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def create_jwt_token(self, username, user_id):
        payload = {
            'username': username,
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_jwt_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def login(self, username, password):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, username, password_hash FROM users WHERE username = ? AND is_active = 1', (username,))
        user = cursor.fetchone()
        
        if user and self.verify_password(password, user[2]):
            user_id, username, _ = user
            token = self.create_jwt_token(username, user_id)
            
            # Update last login
            cursor.execute(
                'UPDATE users SET last_login = ? WHERE id = ?',
                (datetime.now(), user_id)
            )
            
            # Store session
            expires_at = datetime.now() + timedelta(hours=24)
            cursor.execute(
                'INSERT INTO sessions (user_id, session_token, expires_at) VALUES (?, ?, ?)',
                (user_id, token, expires_at)
            )
            
            conn.commit()
            conn.close()
            return token
        else:
            conn.close()
            return None
    
    def logout(self, token):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sessions WHERE session_token = ?', (token,))
        conn.commit()
        conn.close()
    
    def is_authenticated(self):
        if 'auth_token' not in st.session_state:
            return False
        
        token = st.session_state.auth_token
        payload = self.verify_jwt_token(token)
        
        if not payload:
            return False
        
        # Verify session exists in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM sessions WHERE session_token = ? AND expires_at > ?',
            (token, datetime.now())
        )
        session_exists = cursor.fetchone() is not None
        conn.close()
        
        return session_exists
    
    def get_current_user(self):
        if not self.is_authenticated():
            return None
        
        token = st.session_state.auth_token
        payload = self.verify_jwt_token(token)
        return payload

# Initialize auth system
auth = AuthSystem()

def login_form():
    st.title("🔐 TCN Entertainment - Admin Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username and password:
                token = auth.login(username, password)
                if token:
                    st.session_state.auth_token = token
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.error("Please enter both username and password")

def logout_button():
    if st.sidebar.button("Logout"):
        if 'auth_token' in st.session_state:
            auth.logout(st.session_state.auth_token)
            del st.session_state.auth_token
        st.rerun()

def require_auth():
    if not auth.is_authenticated():
        login_form()
        st.stop()

def admin_dashboard():
    require_auth()
    
    st.title("TCN Entertainment - Admin Dashboard")
    st.success(f"Welcome, {auth.get_current_user()['username']}!")
    
    # Admin functionality can be added here
    st.write("## Website Analytics")
    st.write("## Content Management")
    st.write("## User Management")
    
    logout_button()

# For testing/development
if __name__ == "__main__":
    admin_dashboard()
