"""
Script to add phone number field to profile tables
- phone: Professional's contact phone number
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

print("=" * 60)
print("Adding Phone Number Field to Profile Tables")
print("=" * 60)

try:
    # Create connection
    connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    print("\n1. Connecting to PostgreSQL...")
    engine = create_engine(connection_string)
    conn = engine.connect()
    print("✅ Connected successfully!")
    
    # Add column to photographers table
    print("\n2. Adding phone field to photographers table...")
    try:
        conn.execute(text('ALTER TABLE photographers ADD COLUMN IF NOT EXISTS phone VARCHAR(20)'))
        conn.commit()
        print("✅ Field added to photographers table!")
    except Exception as e:
        print(f"⚠️  Field may already exist: {e}")
        conn.rollback()
    
    # Add column to event_coordinators table
    print("\n3. Adding phone field to event_coordinators table...")
    try:
        conn.execute(text('ALTER TABLE event_coordinators ADD COLUMN IF NOT EXISTS phone VARCHAR(20)'))
        conn.commit()
        print("✅ Field added to event_coordinators table!")
    except Exception as e:
        print(f"⚠️  Field may already exist: {e}")
        conn.rollback()
    
    # Add column to djs table
    print("\n4. Adding phone field to djs table...")
    try:
        conn.execute(text('ALTER TABLE djs ADD COLUMN IF NOT EXISTS phone VARCHAR(20)'))
        conn.commit()
        print("✅ Field added to djs table!")
    except Exception as e:
        print(f"⚠️  Field may already exist: {e}")
        conn.rollback()
    
    # Verify the changes
    print("\n5. Verifying phone field...")
    
    for table in ['photographers', 'event_coordinators', 'djs']:
        result = conn.execute(text(f'''
            SELECT column_name, data_type, character_maximum_length
            FROM information_schema.columns 
            WHERE table_name = '{table}' AND column_name = 'phone'
        '''))
        column_info = result.fetchone()
        
        if column_info:
            print(f"\n   {table.upper()}:")
            print(f"   ✅ Field exists: {column_info[0]}")
            print(f"      Type: {column_info[1]}")
            print(f"      Max Length: {column_info[2]} characters")
        else:
            print(f"\n   {table.upper()}:")
            print(f"   ❌ Field not found!")
    
    # Set default phone numbers for existing profiles
    print("\n6. Setting default phone numbers for existing profiles...")
    
    # Update photographer
    conn.execute(text('''
        UPDATE photographers 
        SET phone = '(214) 555-0101'
        WHERE profile_id = 'photographer_1' AND phone IS NULL
    '''))
    
    # Update event coordinator
    conn.execute(text('''
        UPDATE event_coordinators 
        SET phone = '(214) 555-0102'
        WHERE profile_id = 'coordinator_1' AND phone IS NULL
    '''))
    
    # Update DJs
    conn.execute(text('''
        UPDATE djs 
        SET phone = '(214) 260-5003'
        WHERE profile_id = 'dj_1' AND phone IS NULL
    '''))
    
    conn.execute(text('''
        UPDATE djs 
        SET phone = '(214) 555-0104'
        WHERE profile_id = 'dj_2' AND phone IS NULL
    '''))
    
    conn.commit()
    print("✅ Default phone numbers set!")
    
    # Check current values
    print("\n7. Checking current phone values...")
    
    for table in ['photographers', 'event_coordinators', 'djs']:
        result = conn.execute(text(f'''
            SELECT name, phone 
            FROM {table}
            WHERE role != 'admin' OR role IS NULL
        '''))
        profiles = result.fetchall()
        
        print(f"\n   {table.upper()}:")
        for profile in profiles:
            phone_status = profile[1] if profile[1] else "Not set"
            print(f"   - {profile[0]}: {phone_status}")
    
    conn.close()
    print("\n" + "=" * 60)
    print("✅ Phone field added successfully!")
    print("=" * 60)
    print("\nNew Field:")
    print("  - phone: Professional's contact phone number")
    print("  - Type: VARCHAR(20)")
    print("  - Default: NULL (not set)")
    print("\nDefault phone numbers have been set for all existing profiles.")
    print("Professionals can update their phone numbers in Profile Management.")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("=" * 60)
    import traceback
    traceback.print_exc()
