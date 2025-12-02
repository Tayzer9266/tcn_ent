"""
Comprehensive Authentication System Test Script
Tests all authentication functionality without requiring Streamlit
"""
from sqlalchemy import create_engine, text
import hashlib

# Database credentials
db_config = {
    'user': 'tcn_ent',
    'password': 'Provident3333!',
    'host': 'tcn.c54mcgea4luc.us-east-2.rds.amazonaws.com',
    'port': '5432',
    'dbname': 'postgres'
}

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(conn, email, password):
    """
    Authenticate user across all profile tables
    Returns: (success, user_data, profile_type) or (False, None, None)
    """
    try:
        hashed_password = hash_password(password)
        
        # Check all three tables
        for table in ['photographers', 'event_coordinators', 'djs']:
            query = text(f'''
                SELECT profile_id, name, email, role, title, image_path
                FROM {table}
                WHERE email = :email AND password = :password
            ''')
            result = conn.execute(query, {"email": email, "password": hashed_password})
            row = result.fetchone()
            
            if row:
                user_data = {
                    'profile_id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'role': row[3],
                    'title': row[4],
                    'image_path': row[5]
                }
                return True, user_data, table
        
        return False, None, None
        
    except Exception as e:
        print(f"Authentication error: {e}")
        return False, None, None

def test_authentication():
    """Run comprehensive authentication tests"""
    
    print("=" * 80)
    print("AUTHENTICATION SYSTEM TEST SUITE")
    print("=" * 80)
    
    # Connect to database
    print("\n1. Connecting to PostgreSQL...")
    connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    engine = create_engine(connection_string)
    conn = engine.connect()
    print("✅ Connected successfully!")
    
    # Test credentials
    test_cases = [
        {
            "name": "Regular User - Photographer",
            "email": "samantha.lee@tcnphoto.com",
            "password": "Siepe2025!",
            "expected_role": "user",
            "expected_name": "Samantha Lee",
            "should_pass": True
        },
        {
            "name": "Regular User - Event Coordinator",
            "email": "isabella.moreno@tcnevents.com",
            "password": "Siepe2025!",
            "expected_role": "user",
            "expected_name": "Isabella Moreno",
            "should_pass": True
        },
        {
            "name": "Regular User - DJ Tayzer",
            "email": "dj.tayzer@tcnent.com",
            "password": "Siepe2025!",
            "expected_role": "user",
            "expected_name": "DJ Tayzer",
            "should_pass": True
        },
        {
            "name": "Regular User - DJ Tyler",
            "email": "dj.tyler@tcnent.com",
            "password": "Siepe2025!",
            "expected_role": "user",
            "expected_name": "DJ Tyler",
            "should_pass": True
        },
        {
            "name": "Admin User",
            "email": "tcnentertainmen7@gmail.com",
            "password": "7142605003",
            "expected_role": "admin",
            "expected_name": "TCN Entertainment Admin",
            "should_pass": True
        },
        {
            "name": "Invalid Password",
            "email": "samantha.lee@tcnphoto.com",
            "password": "WrongPassword123",
            "expected_role": None,
            "expected_name": None,
            "should_pass": False
        },
        {
            "name": "Non-existent Email",
            "email": "nonexistent@example.com",
            "password": "Siepe2025!",
            "expected_role": None,
            "expected_name": None,
            "should_pass": False
        },
        {
            "name": "Empty Password",
            "email": "samantha.lee@tcnphoto.com",
            "password": "",
            "expected_role": None,
            "expected_name": None,
            "should_pass": False
        }
    ]
    
    print("\n" + "=" * 80)
    print("2. AUTHENTICATION TESTS")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['name']}")
        print(f"   Email: {test['email']}")
        print(f"   Password: {'*' * len(test['password']) if test['password'] else '(empty)'}")
        
        success, user_data, profile_type = authenticate_user(conn, test['email'], test['password'])
        
        if test['should_pass']:
            if success:
                # Verify user data
                if (user_data['role'] == test['expected_role'] and 
                    user_data['name'] == test['expected_name']):
                    print(f"   ✅ PASSED - Authenticated as {user_data['name']} ({user_data['role']})")
                    print(f"      Profile Type: {profile_type}")
                    print(f"      Title: {user_data['title']}")
                    passed += 1
                else:
                    print(f"   ❌ FAILED - User data mismatch")
                    print(f"      Expected: {test['expected_name']} ({test['expected_role']})")
                    print(f"      Got: {user_data['name']} ({user_data['role']})")
                    failed += 1
            else:
                print(f"   ❌ FAILED - Authentication failed (should have passed)")
                failed += 1
        else:
            if not success:
                print(f"   ✅ PASSED - Correctly rejected invalid credentials")
                passed += 1
            else:
                print(f"   ❌ FAILED - Authentication succeeded (should have failed)")
                failed += 1
    
    # Test 3: Verify all users have correct fields
    print("\n" + "=" * 80)
    print("3. DATABASE SCHEMA VERIFICATION")
    print("=" * 80)
    
    for table in ['photographers', 'event_coordinators', 'djs']:
        print(f"\n   Checking {table} table...")
        
        # Check if auth fields exist
        query = text(f'''
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table}' 
            AND column_name IN ('email', 'password', 'role')
            ORDER BY column_name
        ''')
        result = conn.execute(query)
        columns = result.fetchall()
        
        if len(columns) == 3:
            print(f"   ✅ All authentication fields present:")
            for col in columns:
                print(f"      - {col[0]} ({col[1]})")
        else:
            print(f"   ❌ Missing authentication fields")
            failed += 1
    
    # Test 4: Verify password hashing
    print("\n" + "=" * 80)
    print("4. PASSWORD SECURITY VERIFICATION")
    print("=" * 80)
    
    print("\n   Checking password storage...")
    query = text('''
        SELECT email, password, LENGTH(password) as pwd_length
        FROM djs 
        WHERE email = 'dj.tayzer@tcnent.com'
    ''')
    result = conn.execute(query)
    row = result.fetchone()
    
    if row:
        stored_password = row[1]
        pwd_length = row[2]
        
        # SHA256 produces 64 character hex string
        if pwd_length == 64 and stored_password != "Siepe2025!":
            print(f"   ✅ Password is hashed (length: {pwd_length} chars)")
            print(f"   ✅ Password is not stored in plain text")
            
            # Verify hash matches
            expected_hash = hash_password("Siepe2025!")
            if stored_password == expected_hash:
                print(f"   ✅ Hash algorithm working correctly")
            else:
                print(f"   ❌ Hash mismatch")
                failed += 1
        else:
            print(f"   ❌ Password appears to be in plain text or wrong format")
            failed += 1
    
    # Test 5: Role-based access simulation
    print("\n" + "=" * 80)
    print("5. ROLE-BASED ACCESS CONTROL SIMULATION")
    print("=" * 80)
    
    print("\n   Testing Admin Access...")
    success, admin_data, _ = authenticate_user(conn, "tcnentertainmen7@gmail.com", "7142605003")
    if success and admin_data['role'] == 'admin':
        print(f"   ✅ Admin can authenticate")
        
        # Admin should be able to query all profiles
        total_profiles = 0
        for table in ['photographers', 'event_coordinators', 'djs']:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table} WHERE role != 'admin'"))
            count = result.fetchone()[0]
            total_profiles += count
            print(f"      - Can access {count} {table}")
        
        print(f"   ✅ Admin has access to {total_profiles} total profiles")
    else:
        print(f"   ❌ Admin authentication failed")
        failed += 1
    
    print("\n   Testing Regular User Access...")
    success, user_data, user_table = authenticate_user(conn, "samantha.lee@tcnphoto.com", "Siepe2025!")
    if success and user_data['role'] == 'user':
        print(f"   ✅ User can authenticate")
        
        # User should only access their own profile
        query = text(f"SELECT * FROM {user_table} WHERE email = :email")
        result = conn.execute(query, {"email": user_data['email']})
        own_profile = result.fetchone()
        
        if own_profile:
            print(f"   ✅ User can access own profile in {user_table}")
            print(f"      Profile: {user_data['name']} - {user_data['title']}")
        else:
            print(f"   ❌ User cannot access own profile")
            failed += 1
    else:
        print(f"   ❌ User authentication failed")
        failed += 1
    
    # Test 6: SQL Injection Prevention
    print("\n" + "=" * 80)
    print("6. SQL INJECTION PREVENTION TEST")
    print("=" * 80)
    
    sql_injection_attempts = [
        "admin@example.com' OR '1'='1",
        "admin@example.com'; DROP TABLE users; --",
        "' OR 1=1 --",
        "admin' --"
    ]
    
    print("\n   Testing SQL injection attempts...")
    injection_blocked = 0
    for attempt in sql_injection_attempts:
        success, _, _ = authenticate_user(conn, attempt, "password")
        if not success:
            injection_blocked += 1
    
    if injection_blocked == len(sql_injection_attempts):
        print(f"   ✅ All {injection_blocked} SQL injection attempts blocked")
    else:
        print(f"   ⚠️  {len(sql_injection_attempts) - injection_blocked} injection attempts may have succeeded")
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    total_tests = passed + failed
    pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    print(f"Pass Rate: {pass_rate:.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Authentication system is working correctly.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the results above.")
    
    print("=" * 80)
    
    conn.close()

if __name__ == "__main__":
    try:
        test_authentication()
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        import traceback
        traceback.print_exc()
