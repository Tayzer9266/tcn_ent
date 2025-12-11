"""
Script to add media gallery and overview fields to professional profile tables

New Fields:
- gallery_images: JSON array of image paths for gallery
- gallery_videos: JSON array of video URLs for gallery
- profile_video_url: Main profile video URL (YouTube, Vimeo, etc.)
- overview_text: Professional's overview/pitch text
- years_experience: Years of professional experience
- events_completed: Total number of events completed
- average_rating: Average rating from reviews (calculated)
- total_reviews: Total number of reviews (calculated)
"""

from sqlalchemy import create_engine, text

def add_media_fields():
    """Add media gallery and overview fields to all professional tables"""
    
    try:
        # Database configuration
        db_config = {
            'user': 'tcn_ent',
            'password': 'Provident3333!',
            'host': 'tcn.c54mcgea4luc.us-east-2.rds.amazonaws.com',
            'port': '5432',
            'dbname': 'postgres'
        }
        connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
        
        print("=" * 70)
        print("Adding Media Gallery & Overview Fields to Professional Tables")
        print("=" * 70)
        
        # Create connection
        print("\n1. Connecting to PostgreSQL...")
        engine = create_engine(connection_string)
        conn = engine.connect()
        print("✅ Connected successfully!")
        
        # List of tables to update
        tables = ['photographers', 'event_coordinators', 'djs']
        
        for table in tables:
            print(f"\n2. Adding fields to {table} table...")
            
            try:
                # Add gallery_images field (JSON array stored as TEXT)
                conn.execute(text(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS gallery_images TEXT'))
                print(f"   ✅ Added gallery_images to {table}")
                
                # Add gallery_videos field (JSON array stored as TEXT)
                conn.execute(text(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS gallery_videos TEXT'))
                print(f"   ✅ Added gallery_videos to {table}")
                
                # Add profile_video_url field
                conn.execute(text(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS profile_video_url VARCHAR(500)'))
                print(f"   ✅ Added profile_video_url to {table}")
                
                # Add overview_text field
                conn.execute(text(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS overview_text TEXT'))
                print(f"   ✅ Added overview_text to {table}")
                
                # Add years_experience field
                conn.execute(text(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS years_experience INTEGER DEFAULT 0'))
                print(f"   ✅ Added years_experience to {table}")
                
                # Add events_completed field
                conn.execute(text(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS events_completed INTEGER DEFAULT 0'))
                print(f"   ✅ Added events_completed to {table}")
                
                # Add average_rating field
                conn.execute(text(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS average_rating DECIMAL(3,2) DEFAULT 0.00'))
                print(f"   ✅ Added average_rating to {table}")
                
                # Add total_reviews field
                conn.execute(text(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS total_reviews INTEGER DEFAULT 0'))
                print(f"   ✅ Added total_reviews to {table}")
                
                conn.commit()
                print(f"   ✅ All fields added to {table} successfully!")
                
            except Exception as e:
                print(f"   ⚠️  Error adding fields to {table}: {e}")
                continue
        
        # Set default values for existing profiles
        print("\n3. Setting default values for existing profiles...")
        
        for table in tables:
            try:
                # Set default overview text
                conn.execute(text(f'''
                    UPDATE {table}
                    SET overview_text = COALESCE(overview_text, short_bio)
                    WHERE overview_text IS NULL
                '''))
                
                # Set default years of experience based on profile
                if table == 'djs':
                    conn.execute(text(f'''
                        UPDATE {table}
                        SET years_experience = CASE 
                            WHEN profile_id = 'dj_1' THEN 10
                            WHEN profile_id = 'dj_2' THEN 8
                            ELSE 5
                        END
                        WHERE years_experience = 0 OR years_experience IS NULL
                    '''))
                elif table == 'photographers':
                    conn.execute(text(f'''
                        UPDATE {table}
                        SET years_experience = 10
                        WHERE years_experience = 0 OR years_experience IS NULL
                    '''))
                elif table == 'event_coordinators':
                    conn.execute(text(f'''
                        UPDATE {table}
                        SET years_experience = 8
                        WHERE years_experience = 0 OR years_experience IS NULL
                    '''))
                
                # Set default events completed
                conn.execute(text(f'''
                    UPDATE {table}
                    SET events_completed = years_experience * 20
                    WHERE events_completed = 0 OR events_completed IS NULL
                '''))
                
                # Initialize empty JSON arrays for gallery fields
                conn.execute(text(f'''
                    UPDATE {table}
                    SET gallery_images = '[]'
                    WHERE gallery_images IS NULL
                '''))
                
                conn.execute(text(f'''
                    UPDATE {table}
                    SET gallery_videos = '[]'
                    WHERE gallery_videos IS NULL
                '''))
                
                conn.commit()
                print(f"   ✅ Default values set for {table}")
                
            except Exception as e:
                print(f"   ⚠️  Error setting defaults for {table}: {e}")
                continue
        
        # Verify the changes
        print("\n4. Verifying new fields...")
        for table in tables:
            result = conn.execute(text(f'''
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table}' 
                AND column_name IN (
                    'gallery_images', 'gallery_videos', 'profile_video_url',
                    'overview_text', 'years_experience', 'events_completed',
                    'average_rating', 'total_reviews'
                )
                ORDER BY column_name
            '''))
            
            columns = result.fetchall()
            print(f"\n   {table.upper()}:")
            for col in columns:
                print(f"      ✓ {col[0]} ({col[1]})")
        
        # Display sample data
        print("\n5. Sample data from updated tables...")
        for table in tables:
            result = conn.execute(text(f'''
                SELECT profile_id, name, years_experience, events_completed, 
                       average_rating, total_reviews
                FROM {table}
                WHERE role != 'admin' OR role IS NULL
                LIMIT 2
            '''))
            
            rows = result.fetchall()
            print(f"\n   {table.upper()}:")
            for row in rows:
                print(f"      {row[1]} ({row[0]})")
                print(f"         Experience: {row[2]} years | Events: {row[3]}")
                print(f"         Rating: {row[4]} | Reviews: {row[5]}")
        
        conn.close()
        
        print("\n" + "=" * 70)
        print("✅ Media gallery and overview fields added successfully!")
        print("=" * 70)
        print("\nNext Steps:")
        print("1. Run create_reviews_table.py to create the reviews table")
        print("2. Update ProfileManager to handle new fields")
        print("3. Create detailed profile pages")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_media_fields()
