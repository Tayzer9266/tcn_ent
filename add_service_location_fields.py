"""
Script to add service location fields to profile tables
- service_city: City where professional provides services
- service_state: State where professional provides services
- service_radius_miles: Miles radius outside their city/state
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
print("Adding Service Location Fields to Profile Tables")
print("=" * 60)

try:
    # Create connection
    connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    print("\n1. Connecting to PostgreSQL...")
    engine = create_engine(connection_string)
    conn = engine.connect()
    print("✅ Connected successfully!")
    
    # Add columns to photographers table
    print("\n2. Adding service location fields to photographers table...")
    try:
        conn.execute(text('ALTER TABLE photographers ADD COLUMN IF NOT EXISTS service_city VARCHAR(100)'))
        conn.execute(text('ALTER TABLE photographers ADD COLUMN IF NOT EXISTS service_state VARCHAR(50)'))
        conn.execute(text('ALTER TABLE photographers ADD COLUMN IF NOT EXISTS service_radius_miles INTEGER DEFAULT 50'))
        conn.commit()
        print("✅ Fields added to photographers table!")
    except Exception as e:
        print(f"⚠️  Fields may already exist: {e}")
        conn.rollback()
    
    # Add columns to event_coordinators table
    print("\n3. Adding service location fields to event_coordinators table...")
    try:
        conn.execute(text('ALTER TABLE event_coordinators ADD COLUMN IF NOT EXISTS service_city VARCHAR(100)'))
        conn.execute(text('ALTER TABLE event_coordinators ADD COLUMN IF NOT EXISTS service_state VARCHAR(50)'))
        conn.execute(text('ALTER TABLE event_coordinators ADD COLUMN IF NOT EXISTS service_radius_miles INTEGER DEFAULT 50'))
        conn.commit()
        print("✅ Fields added to event_coordinators table!")
    except Exception as e:
        print(f"⚠️  Fields may already exist: {e}")
        conn.rollback()
    
    # Add columns to djs table
    print("\n4. Adding service location fields to djs table...")
    try:
        conn.execute(text('ALTER TABLE djs ADD COLUMN IF NOT EXISTS service_city VARCHAR(100)'))
        conn.execute(text('ALTER TABLE djs ADD COLUMN IF NOT EXISTS service_state VARCHAR(50)'))
        conn.execute(text('ALTER TABLE djs ADD COLUMN IF NOT EXISTS service_radius_miles INTEGER DEFAULT 50'))
        conn.commit()
        print("✅ Fields added to djs table!")
    except Exception as e:
        print(f"⚠️  Fields may already exist: {e}")
        conn.rollback()
    
    # Update existing profiles with default service location (Dallas, TX)
    print("\n5. Setting default service locations for existing profiles...")
    
    # Update photographer
    conn.execute(text('''
        UPDATE photographers 
        SET service_city = 'Dallas',
            service_state = 'Texas',
            service_radius_miles = 50
        WHERE service_city IS NULL
    '''))
    
    # Update event coordinator
    conn.execute(text('''
        UPDATE event_coordinators 
        SET service_city = 'Dallas',
            service_state = 'Texas',
            service_radius_miles = 50
        WHERE service_city IS NULL
    '''))
    
    # Update DJs
    conn.execute(text('''
        UPDATE djs 
        SET service_city = 'Dallas',
            service_state = 'Texas',
            service_radius_miles = 50
        WHERE service_city IS NULL
    '''))
    
    conn.commit()
    print("✅ Default service locations set!")
    
    # Verify the changes
    print("\n6. Verifying service location fields...")
    
    for table in ['photographers', 'event_coordinators', 'djs']:
        result = conn.execute(text(f'''
            SELECT name, service_city, service_state, service_radius_miles 
            FROM {table}
            WHERE role != 'admin' OR role IS NULL
        '''))
        profiles = result.fetchall()
        
        print(f"\n   {table.upper()}:")
        for profile in profiles:
            print(f"   - {profile[0]}")
            print(f"     Location: {profile[1]}, {profile[2]}")
            print(f"     Service Radius: {profile[3]} miles")
    
    conn.close()
    print("\n" + "=" * 60)
    print("✅ Service location fields added successfully!")
    print("=" * 60)
    print("\nNew Fields:")
    print("  - service_city: City where professional provides services")
    print("  - service_state: State where professional provides services")
    print("  - service_radius_miles: Miles radius outside their city/state")
    print("\nDefault Values:")
    print("  - City: Dallas")
    print("  - State: Texas")
    print("  - Radius: 50 miles")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("=" * 60)
    import traceback
    traceback.print_exc()
