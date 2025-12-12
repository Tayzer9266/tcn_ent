import streamlit as st
from sqlalchemy import create_engine, text

def add_gallery_columns():
    """Add gallery columns to all profile tables"""
    try:
        db_config = st.secrets["postgres"]
        connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
        engine = create_engine(connection_string)
        conn = engine.connect()
        
        tables = ['photographers', 'event_coordinators', 'djs']
        
        for table in tables:
            print(f"\nProcessing {table} table...")
            
            # Check if columns exist
            check_query = text(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = :table_name 
                AND column_name IN ('gallery_images', 'gallery_videos', 'profile_video_url', 'overview_text', 'years_experience', 'events_completed')
            """)
            
            result = conn.execute(check_query, {"table_name": table})
            existing_columns = [row[0] for row in result.fetchall()]
            print(f"Existing columns: {existing_columns}")
            
            # Add missing columns
            if 'gallery_images' not in existing_columns:
                print(f"Adding gallery_images to {table}...")
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN gallery_images TEXT DEFAULT '[]'"))
                conn.commit()
                print("✓ Added gallery_images")
            
            if 'gallery_videos' not in existing_columns:
                print(f"Adding gallery_videos to {table}...")
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN gallery_videos TEXT DEFAULT '[]'"))
                conn.commit()
                print("✓ Added gallery_videos")
            
            if 'profile_video_url' not in existing_columns:
                print(f"Adding profile_video_url to {table}...")
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN profile_video_url VARCHAR(500)"))
                conn.commit()
                print("✓ Added profile_video_url")
            
            if 'overview_text' not in existing_columns:
                print(f"Adding overview_text to {table}...")
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN overview_text TEXT"))
                conn.commit()
                print("✓ Added overview_text")
            
            if 'years_experience' not in existing_columns:
                print(f"Adding years_experience to {table}...")
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN years_experience INTEGER DEFAULT 0"))
                conn.commit()
                print("✓ Added years_experience")
            
            if 'events_completed' not in existing_columns:
                print(f"Adding events_completed to {table}...")
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN events_completed INTEGER DEFAULT 0"))
                conn.commit()
                print("✓ Added events_completed")
        
        print("\n✅ All gallery columns added successfully!")
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    add_gallery_columns()
