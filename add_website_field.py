"""
Script to add personal website field to profile tables
- website: Professional's personal website URL
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
print("Adding Website Field to Profile Tables")
print("=" * 60)

try:
    # Create connection
    connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    print("\n1. Connecting to PostgreSQL...")
    engine = create_engine(connection_string)
    conn = engine.connect()
    print("✅ Connected successfully!")
    
    # Add column to photographers table
    print("\n2. Adding website field to photographers table...")
    try:
        conn.execute(text('ALTER TABLE photographers ADD COLUMN IF NOT EXISTS website VARCHAR(500)'))
        conn.commit()
        print("✅ Field added to photographers table!")
    except Exception as e:
        print(f"⚠️  Field may already exist: {e}")
        conn.rollback()
    
    # Add column to event_coordinators table
    print("\n3. Adding website field to event_coordinators table...")
    try:
        conn.execute(text('ALTER TABLE event_coordinators ADD COLUMN IF NOT EXISTS website VARCHAR(500)'))
        conn.commit()
        print("✅ Field added to event_coordinators table!")
    except Exception as e:
        print(f"⚠️  Field may already exist: {e}")
        conn.rollback()
    
    # Add column to djs table
    print("\n4. Adding website field to djs table...")
    try:
        conn.execute(text('ALTER TABLE djs ADD COLUMN IF NOT EXISTS website VARCHAR(500)'))
        conn.commit()
        print("✅ Field added to djs table!")
    except Exception as e:
        print(f"⚠️  Field may already exist: {e}")
        conn.rollback()
    
    # Verify the changes
    print("\n5. Verifying website field...")
    
    for table in ['photographers', 'event_coordinators', 'djs']:
        result = conn.execute(text(f'''
            SELECT column_name, data_type, character_maximum_length
            FROM information_schema.columns 
            WHERE table_name = '{table}' AND column_name = 'website'
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
    
    # Check current values
    print("\n6. Checking current website values...")
    
    for table in ['photographers', 'event_coordinators', 'djs']:
        result = conn.execute(text(f'''
            SELECT name, website 
            FROM {table}
            WHERE role != 'admin' OR role IS NULL
        '''))
        profiles = result.fetchall()
        
        print(f"\n   {table.upper()}:")
        for profile in profiles:
            website_status = profile[1] if profile[1] else "Not set"
            print(f"   - {profile[0]}: {website_status}")
    
    conn.close()
    print("\n" + "=" * 60)
    print("✅ Website field added successfully!")
    print("=" * 60)
    print("\nNew Field:")
    print("  - website: Professional's personal website URL")
    print("  - Type: VARCHAR(500)")
    print("  - Default: NULL (not set)")
    print("\nProfessionals can now add their website URL which will be")
    print("displayed on their profile for clients to learn more.")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("=" * 60)
    import traceback
    traceback.print_exc()
