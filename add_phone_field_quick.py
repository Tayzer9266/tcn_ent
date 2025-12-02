"""
Quick script to add phone number field to profile tables
"""
from sqlalchemy import create_engine, text

# Database credentials
db_config = {
    'user': 'tcn_ent',
    'password': 'Provident3333!',
    'host': 'tcn.c54mcgea4luc.us-east-2.rds.amazonaws.com',
    'port': '5432',
    'dbname': 'postgres'
}

print("Adding phone field...")

try:
    connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    engine = create_engine(connection_string)
    conn = engine.connect()
    
    # Add phone column to all tables
    for table in ['photographers', 'event_coordinators', 'djs']:
        try:
            conn.execute(text(f'ALTER TABLE {table} ADD COLUMN phone VARCHAR(20)'))
            conn.commit()
            print(f"✅ Added phone to {table}")
        except Exception as e:
            if 'already exists' in str(e):
                print(f"⚠️  phone already exists in {table}")
            else:
                print(f"❌ Error on {table}: {e}")
            conn.rollback()
    
    # Set default phone numbers
    conn.execute(text("UPDATE photographers SET phone = '(214) 555-0101' WHERE profile_id = 'photographer_1' AND phone IS NULL"))
    conn.execute(text("UPDATE event_coordinators SET phone = '(214) 555-0102' WHERE profile_id = 'coordinator_1' AND phone IS NULL"))
    conn.execute(text("UPDATE djs SET phone = '(214) 260-5003' WHERE profile_id = 'dj_1' AND phone IS NULL"))
    conn.execute(text("UPDATE djs SET phone = '(214) 555-0104' WHERE profile_id = 'dj_2' AND phone IS NULL"))
    conn.commit()
    print("✅ Set default phone numbers")
    
    conn.close()
    print("✅ Done!")
    
except Exception as e:
    print(f"❌ Error: {e}")
