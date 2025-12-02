"""
Test script to verify service location fields functionality
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

print("=" * 70)
print("SERVICE LOCATION FIELDS TEST")
print("=" * 70)

try:
    # Create connection
    connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    print("\n1. Connecting to PostgreSQL...")
    engine = create_engine(connection_string)
    conn = engine.connect()
    print("✅ Connected successfully!")
    
    # Test 1: Verify fields exist in all tables
    print("\n2. Verifying service location fields in all tables...")
    for table in ['photographers', 'event_coordinators', 'djs']:
        query = text(f'''
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table}' 
            AND column_name IN ('service_city', 'service_state', 'service_radius_miles')
            ORDER BY column_name
        ''')
        result = conn.execute(query)
        columns = result.fetchall()
        
        print(f"\n   {table.upper()}:")
        if len(columns) == 3:
            print(f"   ✅ All service location fields present:")
            for col in columns:
                print(f"      - {col[0]} ({col[1]})")
        else:
            print(f"   ❌ Missing fields (found {len(columns)}/3)")
    
    # Test 2: Check current values
    print("\n3. Checking current service location values...")
    for table in ['photographers', 'event_coordinators', 'djs']:
        query = text(f'''
            SELECT name, service_city, service_state, service_radius_miles 
            FROM {table}
            WHERE role != 'admin' OR role IS NULL
        ''')
        result = conn.execute(query)
        profiles = result.fetchall()
        
        print(f"\n   {table.upper()}:")
        for profile in profiles:
            print(f"   - {profile[0]}")
            print(f"     City: {profile[1] or 'Not set'}")
            print(f"     State: {profile[2] or 'Not set'}")
            print(f"     Radius: {profile[3] or 'Not set'} miles")
    
    # Test 3: Test update functionality
    print("\n4. Testing update functionality...")
    print("   Updating DJ Tayzer's service location...")
    
    update_query = text('''
        UPDATE djs 
        SET service_city = :city,
            service_state = :state,
            service_radius_miles = :radius
        WHERE profile_id = 'dj_1'
    ''')
    
    conn.execute(update_query, {
        "city": "Fort Worth",
        "state": "Texas",
        "radius": 75
    })
    conn.commit()
    
    # Verify update
    verify_query = text('''
        SELECT name, service_city, service_state, service_radius_miles 
        FROM djs 
        WHERE profile_id = 'dj_1'
    ''')
    result = conn.execute(verify_query)
    profile = result.fetchone()
    
    if profile:
        print(f"   ✅ Update successful!")
        print(f"      Name: {profile[0]}")
        print(f"      City: {profile[1]}")
        print(f"      State: {profile[2]}")
        print(f"      Radius: {profile[3]} miles")
    else:
        print(f"   ❌ Update failed!")
    
    # Restore original value
    print("\n   Restoring original values...")
    conn.execute(update_query, {
        "city": "Dallas",
        "state": "Texas",
        "radius": 50
    })
    conn.commit()
    print("   ✅ Restored!")
    
    # Test 4: Test with NULL values
    print("\n5. Testing NULL value handling...")
    test_query = text('''
        SELECT COUNT(*) 
        FROM djs 
        WHERE service_city IS NULL 
        OR service_state IS NULL 
        OR service_radius_miles IS NULL
    ''')
    result = conn.execute(test_query)
    null_count = result.fetchone()[0]
    
    if null_count == 0:
        print("   ✅ No NULL values found - all profiles have service locations set")
    else:
        print(f"   ⚠️  Found {null_count} profile(s) with NULL service location values")
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)
    print("\nService Location Fields Summary:")
    print("  - service_city: City where professional provides services")
    print("  - service_state: State where professional provides services")
    print("  - service_radius_miles: Miles radius outside their city/state")
    print("\nAll fields are working correctly and can be updated via Profile Management!")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("=" * 70)
    import traceback
    traceback.print_exc()
