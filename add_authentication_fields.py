"""
Script to add authentication fields to profile tables
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

print("=" * 60)
print("Adding Authentication Fields to Profile Tables")
print("=" * 60)

try:
    # Create connection
    connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    print("\n1. Connecting to PostgreSQL...")
    engine = create_engine(connection_string)
    conn = engine.connect()
    print("✅ Connected successfully!")
    
    # Add columns to photographers table
    print("\n2. Adding authentication fields to photographers table...")
    try:
        conn.execute(text('ALTER TABLE photographers ADD COLUMN IF NOT EXISTS email VARCHAR(255) UNIQUE'))
        conn.execute(text('ALTER TABLE photographers ADD COLUMN IF NOT EXISTS password VARCHAR(255)'))
        conn.execute(text('ALTER TABLE photographers ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT \'user\''))
        conn.commit()
        print("✅ Fields added to photographers table!")
    except Exception as e:
        print(f"⚠️  Fields may already exist: {e}")
        conn.rollback()
    
    # Add columns to event_coordinators table
    print("\n3. Adding authentication fields to event_coordinators table...")
    try:
        conn.execute(text('ALTER TABLE event_coordinators ADD COLUMN IF NOT EXISTS email VARCHAR(255) UNIQUE'))
        conn.execute(text('ALTER TABLE event_coordinators ADD COLUMN IF NOT EXISTS password VARCHAR(255)'))
        conn.execute(text('ALTER TABLE event_coordinators ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT \'user\''))
        conn.commit()
        print("✅ Fields added to event_coordinators table!")
    except Exception as e:
        print(f"⚠️  Fields may already exist: {e}")
        conn.rollback()
    
    # Add columns to djs table
    print("\n4. Adding authentication fields to djs table...")
    try:
        conn.execute(text('ALTER TABLE djs ADD COLUMN IF NOT EXISTS email VARCHAR(255) UNIQUE'))
        conn.execute(text('ALTER TABLE djs ADD COLUMN IF NOT EXISTS password VARCHAR(255)'))
        conn.execute(text('ALTER TABLE djs ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT \'user\''))
        conn.commit()
        print("✅ Fields added to djs table!")
    except Exception as e:
        print(f"⚠️  Fields may already exist: {e}")
        conn.rollback()
    
    # Update existing profiles with email and password
    default_password = hash_password("Siepe2025!")
    
    print("\n5. Updating photographer with email and password...")
    conn.execute(text('''
        UPDATE photographers 
        SET email = 'samantha.lee@tcnphoto.com',
            password = :password,
            role = 'user'
        WHERE profile_id = 'photographer_1' AND email IS NULL
    '''), {"password": default_password})
    conn.commit()
    print("✅ Photographer updated!")
    
    print("\n6. Updating event coordinator with email and password...")
    conn.execute(text('''
        UPDATE event_coordinators 
        SET email = 'isabella.moreno@tcnevents.com',
            password = :password,
            role = 'user'
        WHERE profile_id = 'coordinator_1' AND email IS NULL
    '''), {"password": default_password})
    conn.commit()
    print("✅ Event coordinator updated!")
    
    print("\n7. Updating DJs with email and password...")
    conn.execute(text('''
        UPDATE djs 
        SET email = 'dj.tayzer@tcnent.com',
            password = :password,
            role = 'user'
        WHERE profile_id = 'dj_1' AND email IS NULL
    '''), {"password": default_password})
    
    conn.execute(text('''
        UPDATE djs 
        SET email = 'dj.tyler@tcnent.com',
            password = :password,
            role = 'user'
        WHERE profile_id = 'dj_2' AND email IS NULL
    '''), {"password": default_password})
    conn.commit()
    print("✅ DJs updated!")
    
    # Create admin profile in djs table
    print("\n8. Creating admin profile...")
    admin_password = hash_password("7142605003")
    
    # Check if admin already exists
    result = conn.execute(text("SELECT COUNT(*) FROM djs WHERE email = 'tcnentertainmen7@gmail.com'"))
    admin_exists = result.fetchone()[0] > 0
    
    if not admin_exists:
        conn.execute(text('''
            INSERT INTO djs (profile_id, name, title, short_bio, full_bio, image_path, email, password, role, youtube, instagram, facebook)
            VALUES (
                'admin_profile',
                'TCN Entertainment Admin',
                'System Administrator',
                'Administrative account for managing all profiles and system settings.',
                'This is the administrative account with full access to all profiles and system management features. This account can view, edit, and manage all photographer, event coordinator, and DJ profiles.',
                'pages/images/company_logo_icon.png',
                'tcnentertainmen7@gmail.com',
                :password,
                'admin',
                NULL,
                NULL,
                NULL
            )
        '''), {"password": admin_password})
        conn.commit()
        print("✅ Admin profile created!")
    else:
        print("ℹ️  Admin profile already exists, skipping...")
    
    # Verify all profiles
    print("\n9. Verifying profiles...")
    
    for table in ['photographers', 'event_coordinators', 'djs']:
        result = conn.execute(text(f"SELECT profile_id, name, email, role FROM {table}"))
        profiles = result.fetchall()
        print(f"\n   {table.upper()}:")
        for profile in profiles:
            print(f"   - {profile[1]} ({profile[2]}) - Role: {profile[3]}")
    
    conn.close()
    print("\n" + "=" * 60)
    print("✅ Authentication fields added successfully!")
    print("=" * 60)
    print("\nDefault Credentials:")
    print("  Regular Users: password = 'Siepe2025!'")
    print("  Admin: email = 'tcnentertainmen7@gmail.com', password = '7142605003'")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("=" * 60)
    import traceback
    traceback.print_exc()
