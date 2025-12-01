import sqlite3
import os
from datetime import datetime
import json

class ProfileManager:
    def __init__(self):
        self.db_path = "profiles.db"
        self.init_db()
    
    def init_db(self):
        """Initialize the database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create photographers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS photographers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                title TEXT NOT NULL,
                short_bio TEXT,
                full_bio TEXT,
                image_path TEXT,
                youtube TEXT,
                instagram TEXT,
                facebook TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create event_coordinators table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS event_coordinators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                title TEXT NOT NULL,
                short_bio TEXT,
                full_bio TEXT,
                image_path TEXT,
                youtube TEXT,
                instagram TEXT,
                facebook TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create djs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS djs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                title TEXT NOT NULL,
                short_bio TEXT,
                full_bio TEXT,
                image_path TEXT,
                youtube TEXT,
                instagram TEXT,
                facebook TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        
        # Initialize with default data if tables are empty
        self._initialize_default_data(cursor, conn)
        
        conn.close()
    
    def _initialize_default_data(self, cursor, conn):
        """Initialize tables with existing profile data"""
        
        # Check if photographers table is empty
        cursor.execute('SELECT COUNT(*) FROM photographers')
        if cursor.fetchone()[0] == 0:
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
            cursor.execute('''
                INSERT INTO photographers (profile_id, name, title, short_bio, full_bio, image_path, youtube, instagram, facebook)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                photographer_data["profile_id"],
                photographer_data["name"],
                photographer_data["title"],
                photographer_data["short_bio"],
                photographer_data["full_bio"],
                photographer_data["image_path"],
                photographer_data["youtube"],
                photographer_data["instagram"],
                photographer_data["facebook"]
            ))
        
        # Check if event_coordinators table is empty
        cursor.execute('SELECT COUNT(*) FROM event_coordinators')
        if cursor.fetchone()[0] == 0:
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
            cursor.execute('''
                INSERT INTO event_coordinators (profile_id, name, title, short_bio, full_bio, image_path, youtube, instagram, facebook)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                coordinator_data["profile_id"],
                coordinator_data["name"],
                coordinator_data["title"],
                coordinator_data["short_bio"],
                coordinator_data["full_bio"],
                coordinator_data["image_path"],
                coordinator_data["youtube"],
                coordinator_data["instagram"],
                coordinator_data["facebook"]
            ))
        
        # Check if djs table is empty
        cursor.execute('SELECT COUNT(*) FROM djs')
        if cursor.fetchone()[0] == 0:
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
                cursor.execute('''
                    INSERT INTO djs (profile_id, name, title, short_bio, full_bio, image_path, youtube, instagram, facebook)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    dj["profile_id"],
                    dj["name"],
                    dj["title"],
                    dj["short_bio"],
                    dj["full_bio"],
                    dj["image_path"],
                    dj["youtube"],
                    dj["instagram"],
                    dj["facebook"]
                ))
        
        conn.commit()
    
    def get_all_profiles(self, profile_type):
        """Get all profiles of a specific type (photographers, event_coordinators, djs)"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT * FROM {profile_type} ORDER BY id')
        rows = cursor.fetchall()
        
        profiles = []
        for row in rows:
            profiles.append(dict(row))
        
        conn.close()
        return profiles
    
    def get_profile_by_id(self, profile_type, profile_id):
        """Get a specific profile by its profile_id"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT * FROM {profile_type} WHERE profile_id = ?', (profile_id,))
        row = cursor.fetchone()
        
        conn.close()
        return dict(row) if row else None
    
    def update_profile(self, profile_type, profile_id, data):
        """Update a profile with new data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build update query dynamically based on provided data
        update_fields = []
        values = []
        
        allowed_fields = ['name', 'title', 'short_bio', 'full_bio', 'image_path', 'youtube', 'instagram', 'facebook']
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = ?")
                values.append(data[field])
        
        if update_fields:
            update_fields.append("updated_at = ?")
            values.append(datetime.now())
            values.append(profile_id)
            
            query = f"UPDATE {profile_type} SET {', '.join(update_fields)} WHERE profile_id = ?"
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()
        return True
    
    def add_profile(self, profile_type, data):
        """Add a new profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f'''
            INSERT INTO {profile_type} (profile_id, name, title, short_bio, full_bio, image_path, youtube, instagram, facebook)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('profile_id'),
            data.get('name'),
            data.get('title'),
            data.get('short_bio'),
            data.get('full_bio'),
            data.get('image_path'),
            data.get('youtube'),
            data.get('instagram'),
            data.get('facebook')
        ))
        
        conn.commit()
        conn.close()
        return True
    
    def delete_profile(self, profile_type, profile_id):
        """Delete a profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f'DELETE FROM {profile_type} WHERE profile_id = ?', (profile_id,))
        conn.commit()
        conn.close()
        return True

# Initialize the profile manager
profile_manager = ProfileManager()
