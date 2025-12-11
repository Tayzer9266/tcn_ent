import streamlit as st
from sqlalchemy import create_engine, text
from datetime import datetime
import pandas as pd
import hashlib

class ProfileManager:
    def __init__(self):
        self.engine = None
        self.conn = None
        self.init_connection()
        self.init_db()
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self, email, password):
        """
        Authenticate user across all profile tables
        Returns: (success, user_data, profile_type) or (False, None, None)
        """
        try:
            hashed_password = self.hash_password(password)
            
            # Check all three tables
            for table in ['photographers', 'event_coordinators', 'djs']:
                query = text(f'''
                    SELECT profile_id, name, email, role, title, image_path
                    FROM {table}
                    WHERE email = :email AND password = :password
                ''')
                result = self.conn.execute(query, {"email": email, "password": hashed_password})
                row = result.fetchone()
                
                if row:
                    user_data = {
                        'profile_id': row[0],
                        'name': row[1],
                        'email': row[2],
                        'role': row[3],
                        'title': row[4],
                        'image_path': row[5]
                    }
                    return True, user_data, table
            
            return False, None, None
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return False, None, None
    
    def get_user_profile(self, email):
        """
        Get user profile by email across all tables
        Returns: (profile_data, profile_type) or (None, None)
        """
        try:
            for table in ['photographers', 'event_coordinators', 'djs']:
                query = text(f'SELECT * FROM {table} WHERE email = :email')
                result = self.conn.execute(query, {"email": email})
                row = result.fetchone()
                
                if row:
                    return dict(row._mapping), table
            
            return None, None
            
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return None, None
    
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
    
    def init_db(self):
        """Initialize the database and create tables if they don't exist"""
        try:
            # Create photographers table
            self.conn.execute(text('''
                CREATE TABLE IF NOT EXISTS photographers (
                    id SERIAL PRIMARY KEY,
                    profile_id VARCHAR(100) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    short_bio TEXT,
                    full_bio TEXT,
                    image_path VARCHAR(500),
                    youtube VARCHAR(500),
                    instagram VARCHAR(500),
                    facebook VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            
            # Create event_coordinators table
            self.conn.execute(text('''
                CREATE TABLE IF NOT EXISTS event_coordinators (
                    id SERIAL PRIMARY KEY,
                    profile_id VARCHAR(100) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    short_bio TEXT,
                    full_bio TEXT,
                    image_path VARCHAR(500),
                    youtube VARCHAR(500),
                    instagram VARCHAR(500),
                    facebook VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            
            # Create djs table
            self.conn.execute(text('''
                CREATE TABLE IF NOT EXISTS djs (
                    id SERIAL PRIMARY KEY,
                    profile_id VARCHAR(100) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    short_bio TEXT,
                    full_bio TEXT,
                    image_path VARCHAR(500),
                    youtube VARCHAR(500),
                    instagram VARCHAR(500),
                    facebook VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            
            self.conn.commit()
            
            # Initialize with default data if tables are empty
            self._initialize_default_data()
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise
    
    def _initialize_default_data(self):
        """Initialize tables with existing profile data"""
        
        try:
            # Check if photographers table is empty
            result = self.conn.execute(text('SELECT COUNT(*) FROM photographers'))
            count = result.fetchone()[0]
            
            if count == 0:
                photographer_data = {
                    "profile_id": "photographer_1",
                    "name": "Samantha Lee",
                    "title": "Wedding & Event Photographer",
                    "short_bio": "Capturing timeless moments with artistic flair. Specializing in weddings and corporate events.",
                    "image_path": "pages/images/photographer_sam.png",
                    "full_bio": "Elena Vasquez is a passionate photographer with over 10 years of experience in capturing the essence of special occasions. Her work focuses on creating stunning visuals that tell the story of your event, from intimate portraits to grand celebrations. Based in Dallas, TX, she works closely with event planners to ensure every shot is perfect.",
                    "youtube": None,
                    "instagram": None,
                    "facebook": None
                }
                self.conn.execute(text('''
                    INSERT INTO photographers (profile_id, name, title, short_bio, full_bio, image_path, youtube, instagram, facebook)
                    VALUES (:profile_id, :name, :title, :short_bio, :full_bio, :image_path, :youtube, :instagram, :facebook)
                '''), photographer_data)
            
            # Check if event_coordinators table is empty
            result = self.conn.execute(text('SELECT COUNT(*) FROM event_coordinators'))
            count = result.fetchone()[0]
            
            if count == 0:
                coordinator_data = {
                    "profile_id": "coordinator_1",
                    "name": "Isabella Moreno",
                    "title": "Wedding & Party Coordinator",
                    "short_bio": "Expert in planning seamless weddings and private parties. Making your vision a reality.",
                    "image_path": "pages/images/corporate event.jpg",
                    "full_bio": "Isabella Moreno is a dedicated event coordinator with over 8 years of experience in creating memorable celebrations. She specializes in weddings and private parties, ensuring every detail is perfect. Based in Dallas, TX, she works closely with clients to bring their vision to life.",
                    "youtube": None,
                    "instagram": None,
                    "facebook": None
                }
                self.conn.execute(text('''
                    INSERT INTO event_coordinators (profile_id, name, title, short_bio, full_bio, image_path, youtube, instagram, facebook)
                    VALUES (:profile_id, :name, :title, :short_bio, :full_bio, :image_path, :youtube, :instagram, :facebook)
                '''), coordinator_data)
            
            # Check if djs table is empty
            result = self.conn.execute(text('SELECT COUNT(*) FROM djs'))
            count = result.fetchone()[0]
            
            if count == 0:
                dj_data = [
                    {
                        "profile_id": "dj_1",
                        "name": "DJ Tayzer",
                        "title": "Master DJ & Event Specialist",
                        "short_bio": "Expert in mixing beats and creating unforgettable atmospheres. Specializing in weddings and parties.",
                        "image_path": "pages/images/djs_tay.png",
                        "full_bio": "DJ Tayzer is a seasoned professional with over 10 years of experience in the DJ industry. Known for his seamless transitions and crowd-engaging sets, he specializes in weddings, corporate events, and private parties. Based in Dallas, TX, he brings energy and professionalism to every gig.",
                        "youtube": "https://www.youtube.com/@djtayzer",
                        "instagram": "https://www.instagram.com/tayzer/",
                        "facebook": "https://www.facebook.com/profile.php?id=61574735690575"
                    },
                    {
                        "profile_id": "dj_2",
                        "name": "DJ Tyler",
                        "title": "House Music DJ",
                        "short_bio": "Master of house music beats, creating energetic and soulful atmospheres. Specializing in dance parties and festivals.",
                        "image_path": "pages/images/djs_tyler.png",
                        "full_bio": "DJ Tyler is a passionate house music enthusiast with over 8 years of experience in the DJ industry. Known for his deep house sets and infectious vibes, he specializes in dance parties, festivals, and private events. Based in Dallas, TX, he brings soulful energy and professionalism to every gig.",
                        "youtube": None,
                        "instagram": None,
                        "facebook": None
                    }
                ]
                
                for dj in dj_data:
                    self.conn.execute(text('''
                        INSERT INTO djs (profile_id, name, title, short_bio, full_bio, image_path, youtube, instagram, facebook)
                        VALUES (:profile_id, :name, :title, :short_bio, :full_bio, :image_path, :youtube, :instagram, :facebook)
                    '''), dj)
            
            self.conn.commit()
            
        except Exception as e:
            print(f"Error initializing default data: {e}")
            raise
    
    def get_all_profiles(self, profile_type):
        """Get all profiles of a specific type (photographers, event_coordinators, djs)"""
        try:
            query = text(f'SELECT * FROM {profile_type} ORDER BY id')
            result = self.conn.execute(query)
            rows = result.fetchall()
            
            profiles = []
            for row in rows:
                # Convert row to dictionary
                profile_dict = dict(row._mapping)
                profiles.append(profile_dict)
            
            return profiles
            
        except Exception as e:
            print(f"Error getting profiles: {e}")
            return []
    
    def get_profile_by_id(self, profile_type, profile_id):
        """Get a specific profile by its profile_id"""
        try:
            query = text(f'SELECT * FROM {profile_type} WHERE profile_id = :profile_id')
            result = self.conn.execute(query, {"profile_id": profile_id})
            row = result.fetchone()
            
            if row:
                return dict(row._mapping)
            return None
            
        except Exception as e:
            print(f"Error getting profile by id: {e}")
            return None
    
    def update_profile(self, profile_type, profile_id, data):
        """Update a profile with new data"""
        try:
            # Build update query dynamically based on provided data
            update_fields = []
            values = {"profile_id": profile_id}
            
            allowed_fields = ['name', 'title', 'short_bio', 'full_bio', 'image_path', 'youtube', 'instagram', 'facebook', 'service_city', 'service_state', 'service_radius_miles', 'website', 'phone', 'gallery_images', 'gallery_videos', 'profile_video_url', 'overview_text', 'years_experience', 'events_completed']
            
            for field in allowed_fields:
                if field in data:
                    update_fields.append(f"{field} = :{field}")
                    values[field] = data[field]
            
            if update_fields:
                update_fields.append("updated_at = :updated_at")
                values["updated_at"] = datetime.now()
                
                query = text(f"UPDATE {profile_type} SET {', '.join(update_fields)} WHERE profile_id = :profile_id")
                self.conn.execute(query, values)
                self.conn.commit()
            
            return True
            
        except Exception as e:
            print(f"Error updating profile: {e}")
            return False
    
    def add_profile(self, profile_type, data):
        """Add a new profile"""
        try:
            query = text(f'''
                INSERT INTO {profile_type} (profile_id, name, title, short_bio, full_bio, image_path, youtube, instagram, facebook)
                VALUES (:profile_id, :name, :title, :short_bio, :full_bio, :image_path, :youtube, :instagram, :facebook)
            ''')
            
            profile_data = {
                'profile_id': data.get('profile_id'),
                'name': data.get('name'),
                'title': data.get('title'),
                'short_bio': data.get('short_bio'),
                'full_bio': data.get('full_bio'),
                'image_path': data.get('image_path'),
                'youtube': data.get('youtube'),
                'instagram': data.get('instagram'),
                'facebook': data.get('facebook')
            }
            
            self.conn.execute(query, profile_data)
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"Error adding profile: {e}")
            return False
    
    def delete_profile(self, profile_type, profile_id):
        """Delete a profile"""
        try:
            query = text(f'DELETE FROM {profile_type} WHERE profile_id = :profile_id')
            self.conn.execute(query, {"profile_id": profile_id})
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"Error deleting profile: {e}")
            return False
    
    def get_professional_reviews(self, profile_type, profile_id):
        """Get all reviews for a professional"""
        try:
            query = text('''
                SELECT review_id, client_name, rating, review_title, review_text,
                       event_type, event_date, verified_booking, helpful_count, 
                       created_at, updated_at
                FROM professional_reviews
                WHERE professional_type = :prof_type AND professional_id = :prof_id
                ORDER BY created_at DESC
            ''')
            result = self.conn.execute(query, {"prof_type": profile_type, "prof_id": profile_id})
            rows = result.fetchall()
            
            reviews = []
            for row in rows:
                reviews.append(dict(row._mapping))
            
            return reviews
            
        except Exception as e:
            print(f"Error getting reviews: {e}")
            return []
    
    def add_review(self, review_data):
        """Add a new review and update professional's rating"""
        try:
            query = text('''
                INSERT INTO professional_reviews (
                    professional_type, professional_id, client_id, client_name,
                    rating, review_title, review_text, event_type, event_date,
                    verified_booking
                ) VALUES (
                    :professional_type, :professional_id, :client_id, :client_name,
                    :rating, :review_title, :review_text, :event_type, :event_date,
                    :verified_booking
                )
            ''')
            
            self.conn.execute(query, review_data)
            self.conn.commit()
            
            # Update professional's average rating and review count
            self.update_review_stats(
                review_data['professional_type'],
                review_data['professional_id']
            )
            
            return True
            
        except Exception as e:
            print(f"Error adding review: {e}")
            return False
    
    def update_review_stats(self, profile_type, profile_id):
        """Update professional's average rating and total review count"""
        try:
            # Calculate average rating and count
            query = text(f'''
                UPDATE {profile_type}
                SET 
                    average_rating = COALESCE((
                        SELECT ROUND(AVG(rating)::numeric, 2)
                        FROM professional_reviews
                        WHERE professional_type = :prof_type
                        AND professional_id = :prof_id
                    ), 0.00),
                    total_reviews = COALESCE((
                        SELECT COUNT(*)
                        FROM professional_reviews
                        WHERE professional_type = :prof_type
                        AND professional_id = :prof_id
                    ), 0)
                WHERE profile_id = :prof_id
            ''')
            
            self.conn.execute(query, {"prof_type": profile_type, "prof_id": profile_id})
            self.conn.commit()
            
            return True
            
        except Exception as e:
            print(f"Error updating review stats: {e}")
            return False
    
    def add_gallery_item(self, profile_type, profile_id, media_type, media_path):
        """Add an image or video to professional's gallery"""
        try:
            import json
            
            # Get current profile
            profile = self.get_profile_by_id(profile_type, profile_id)
            if not profile:
                return False
            
            # Get current gallery
            if media_type == 'image':
                gallery = json.loads(profile.get('gallery_images', '[]'))
                gallery.append(media_path)
                field_name = 'gallery_images'
            else:  # video
                gallery = json.loads(profile.get('gallery_videos', '[]'))
                gallery.append(media_path)
                field_name = 'gallery_videos'
            
            # Update profile
            query = text(f'''
                UPDATE {profile_type}
                SET {field_name} = :gallery, updated_at = :updated_at
                WHERE profile_id = :profile_id
            ''')
            
            self.conn.execute(query, {
                "gallery": json.dumps(gallery),
                "updated_at": datetime.now(),
                "profile_id": profile_id
            })
            self.conn.commit()
            
            return True
            
        except Exception as e:
            print(f"Error adding gallery item: {e}")
            return False
    
    def delete_gallery_item(self, profile_type, profile_id, media_type, media_path):
        """Remove an image or video from professional's gallery"""
        try:
            import json
            
            # Get current profile
            profile = self.get_profile_by_id(profile_type, profile_id)
            if not profile:
                return False
            
            # Get current gallery and remove item
            if media_type == 'image':
                gallery = json.loads(profile.get('gallery_images', '[]'))
                field_name = 'gallery_images'
            else:  # video
                gallery = json.loads(profile.get('gallery_videos', '[]'))
                field_name = 'gallery_videos'
            
            if media_path in gallery:
                gallery.remove(media_path)
            
            # Update profile
            query = text(f'''
                UPDATE {profile_type}
                SET {field_name} = :gallery, updated_at = :updated_at
                WHERE profile_id = :profile_id
            ''')
            
            self.conn.execute(query, {
                "gallery": json.dumps(gallery),
                "updated_at": datetime.now(),
                "profile_id": profile_id
            })
            self.conn.commit()
            
            return True
            
        except Exception as e:
            print(f"Error deleting gallery item: {e}")
            return False

# Initialize the profile manager
profile_manager = ProfileManager()
