"""
Simple script to add media gallery fields to professional tables
"""

from sqlalchemy import create_engine, text

# Database configuration
db_config = {
    'user': 'tcn_ent',
    'password': 'Provident3333!',
    'host': 'tcn.c54mcgea4luc.us-east-2.rds.amazonaws.com',
    'port': '5432',
    'dbname': 'postgres'
}

connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"

print("Connecting to database...")
engine = create_engine(connection_string)
conn = engine.connect()
print("✅ Connected!")

tables = ['photographers', 'event_coordinators', 'djs']

for table in tables:
    print(f"\nAdding fields to {table}...")
    
    # Add all fields in one transaction
    try:
        conn.execute(text(f'''
            ALTER TABLE {table} 
            ADD COLUMN IF NOT EXISTS gallery_images TEXT,
            ADD COLUMN IF NOT EXISTS gallery_videos TEXT,
            ADD COLUMN IF NOT EXISTS profile_video_url VARCHAR(500),
            ADD COLUMN IF NOT EXISTS overview_text TEXT,
            ADD COLUMN IF NOT EXISTS years_experience INTEGER DEFAULT 0,
            ADD COLUMN IF NOT EXISTS events_completed INTEGER DEFAULT 0,
            ADD COLUMN IF NOT EXISTS average_rating DECIMAL(3,2) DEFAULT 0.00,
            ADD COLUMN IF NOT EXISTS total_reviews INTEGER DEFAULT 0
        '''))
        conn.commit()
        print(f"✅ Fields added to {table}")
    except Exception as e:
        print(f"Error: {e}")
        # Try adding fields one by one if batch fails
        fields = [
            ('gallery_images', 'TEXT'),
            ('gallery_videos', 'TEXT'),
            ('profile_video_url', 'VARCHAR(500)'),
            ('overview_text', 'TEXT'),
            ('years_experience', 'INTEGER DEFAULT 0'),
            ('events_completed', 'INTEGER DEFAULT 0'),
            ('average_rating', 'DECIMAL(3,2) DEFAULT 0.00'),
            ('total_reviews', 'INTEGER DEFAULT 0')
        ]
        
        for field_name, field_type in fields:
            try:
                conn.execute(text(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {field_name} {field_type}'))
                conn.commit()
                print(f"  ✅ Added {field_name}")
            except Exception as e2:
                print(f"  ⚠️  {field_name}: {e2}")

# Set default values
print("\nSetting default values...")
for table in tables:
    try:
        conn.execute(text(f"UPDATE {table} SET gallery_images = '[]' WHERE gallery_images IS NULL"))
        conn.execute(text(f"UPDATE {table} SET gallery_videos = '[]' WHERE gallery_videos IS NULL"))
        conn.execute(text(f"UPDATE {table} SET overview_text = short_bio WHERE overview_text IS NULL"))
        
        if table == 'djs':
            conn.execute(text(f"UPDATE {table} SET years_experience = 10 WHERE profile_id = 'dj_1' AND years_experience = 0"))
            conn.execute(text(f"UPDATE {table} SET years_experience = 8 WHERE profile_id = 'dj_2' AND years_experience = 0"))
        elif table == 'photographers':
            conn.execute(text(f"UPDATE {table} SET years_experience = 10 WHERE years_experience = 0"))
        elif table == 'event_coordinators':
            conn.execute(text(f"UPDATE {table} SET years_experience = 8 WHERE years_experience = 0"))
        
        conn.execute(text(f"UPDATE {table} SET events_completed = years_experience * 20 WHERE events_completed = 0"))
        conn.commit()
        print(f"✅ Defaults set for {table}")
    except Exception as e:
        print(f"⚠️  Error setting defaults for {table}: {e}")

conn.close()
print("\n✅ Done!")
