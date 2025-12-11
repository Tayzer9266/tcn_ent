"""
Robust script to add media gallery fields - handles connection issues
"""

from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
import time

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
print("Adding Media Gallery Fields - Robust Version")
print("=" * 70)

tables = ['photographers', 'event_coordinators', 'djs']
fields_to_add = [
    ('gallery_images', 'TEXT'),
    ('gallery_videos', 'TEXT'),
    ('profile_video_url', 'VARCHAR(500)'),
    ('overview_text', 'TEXT'),
    ('years_experience', 'INTEGER DEFAULT 0'),
    ('events_completed', 'INTEGER DEFAULT 0'),
    ('average_rating', 'DECIMAL(3,2) DEFAULT 0.00'),
    ('total_reviews', 'INTEGER DEFAULT 0')
]

for table in tables:
    print(f"\n{'='*70}")
    print(f"Processing table: {table}")
    print(f"{'='*70}")
    
    for field_name, field_type in fields_to_add:
        try:
            # Create fresh connection for each operation
            engine = create_engine(connection_string, poolclass=NullPool)
            conn = engine.connect()
            
            print(f"  Adding {field_name}...", end=" ")
            conn.execute(text(f'ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {field_name} {field_type}'))
            conn.commit()
            conn.close()
            engine.dispose()
            print("✅")
            
            time.sleep(0.5)  # Small delay between operations
            
        except Exception as e:
            print(f"⚠️  {str(e)[:100]}")
            try:
                conn.close()
                engine.dispose()
            except:
                pass

# Set default values
print(f"\n{'='*70}")
print("Setting default values")
print(f"{'='*70}")

for table in tables:
    print(f"\n{table}:")
    
    updates = [
        ("gallery_images = '[]'", "gallery_images IS NULL"),
        ("gallery_videos = '[]'", "gallery_videos IS NULL"),
        ("overview_text = short_bio", "overview_text IS NULL"),
    ]
    
    for update_set, where_clause in updates:
        try:
            engine = create_engine(connection_string, poolclass=NullPool)
            conn = engine.connect()
            
            conn.execute(text(f"UPDATE {table} SET {update_set} WHERE {where_clause}"))
            conn.commit()
            conn.close()
            engine.dispose()
            print(f"  ✅ Updated: {update_set.split('=')[0].strip()}")
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"  ⚠️  {str(e)[:100]}")
            try:
                conn.close()
                engine.dispose()
            except:
                pass

# Set experience values
print(f"\nSetting experience values...")

experience_updates = {
    'djs': [
        ("years_experience = 10", "profile_id = 'dj_1' AND (years_experience = 0 OR years_experience IS NULL)"),
        ("years_experience = 8", "profile_id = 'dj_2' AND (years_experience = 0 OR years_experience IS NULL)"),
    ],
    'photographers': [
        ("years_experience = 10", "years_experience = 0 OR years_experience IS NULL"),
    ],
    'event_coordinators': [
        ("years_experience = 8", "years_experience = 0 OR years_experience IS NULL"),
    ]
}

for table, updates in experience_updates.items():
    for update_set, where_clause in updates:
        try:
            engine = create_engine(connection_string, poolclass=NullPool)
            conn = engine.connect()
            
            conn.execute(text(f"UPDATE {table} SET {update_set} WHERE {where_clause}"))
            conn.commit()
            conn.close()
            engine.dispose()
            print(f"  ✅ {table}: {update_set}")
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"  ⚠️  {str(e)[:100]}")
            try:
                conn.close()
                engine.dispose()
            except:
                pass

# Set events completed
for table in tables:
    try:
        engine = create_engine(connection_string, poolclass=NullPool)
        conn = engine.connect()
        
        conn.execute(text(f"UPDATE {table} SET events_completed = years_experience * 20 WHERE events_completed = 0 OR events_completed IS NULL"))
        conn.commit()
        conn.close()
        engine.dispose()
        print(f"  ✅ {table}: events_completed calculated")
        
        time.sleep(0.5)
        
    except Exception as e:
        print(f"  ⚠️  {str(e)[:100]}")
        try:
            conn.close()
            engine.dispose()
        except:
            pass

print(f"\n{'='*70}")
print("✅ Process completed!")
print(f"{'='*70}")
print("\nNext step: Run create_reviews_table.py")
