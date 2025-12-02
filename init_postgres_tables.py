"""
Script to initialize PostgreSQL tables for profiles
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
print("Initializing PostgreSQL Profile Tables")
print("=" * 60)

try:
    # Create connection
    connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    print("\n1. Connecting to PostgreSQL...")
    engine = create_engine(connection_string)
    conn = engine.connect()
    print("✅ Connected successfully!")
    
    # Create photographers table
    print("\n2. Creating photographers table...")
    conn.execute(text('''
        CREATE TABLE IF NOT EXISTS photographers (
            id SERIAL PRIMARY KEY,
            profile_id VARCHAR(100) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            title VARCHAR(255) NOT NULL,
            short_bio TEXT,
            full_bio TEXT,
            image_path VARCHAR(500),
            youtube VARCHAR(500),
            instagram VARCHAR(500),
            facebook VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''))
    conn.commit()
    print("✅ Photographers table created!")
    
    # Create event_coordinators table
    print("\n3. Creating event_coordinators table...")
    conn.execute(text('''
        CREATE TABLE IF NOT EXISTS event_coordinators (
            id SERIAL PRIMARY KEY,
            profile_id VARCHAR(100) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            title VARCHAR(255) NOT NULL,
            short_bio TEXT,
            full_bio TEXT,
            image_path VARCHAR(500),
            youtube VARCHAR(500),
            instagram VARCHAR(500),
            facebook VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''))
    conn.commit()
    print("✅ Event coordinators table created!")
    
    # Create djs table
    print("\n4. Creating djs table...")
    conn.execute(text('''
        CREATE TABLE IF NOT EXISTS djs (
            id SERIAL PRIMARY KEY,
            profile_id VARCHAR(100) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            title VARCHAR(255) NOT NULL,
            short_bio TEXT,
            full_bio TEXT,
            image_path VARCHAR(500),
            youtube VARCHAR(500),
            instagram VARCHAR(500),
            facebook VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''))
    conn.commit()
    print("✅ DJs table created!")
    
    # Insert default photographer data
    print("\n5. Inserting default photographer data...")
    result = conn.execute(text('SELECT COUNT(*) FROM photographers'))
    count = result.fetchone()[0]
    
    if count == 0:
        photographer_data = {
            "profile_id": "photographer_1",
            "name": "Samantha Lee",
            "title": "Wedding & Event Photographer",
            "short_bio": "Capturing timeless moments with artistic flair. Specializing in weddings and corporate events.",
            "image_path": "pages/images/photographer_sam.png",
            "full_bio": "Elena Vasquez is a passionate photographer with over 10 years of experience in capturing the essence of special occasions. Her work focuses on creating stunning visuals that tell the story of your event, from intimate portraits to grand celebrations. Based in Dallas, TX, she works closely with event planners to ensure every shot is perfect.",
            "youtube": None,
            "instagram": None,
            "facebook": None
        }
        conn.execute(text('''
            INSERT INTO photographers (profile_id, name, title, short_bio, full_bio, image_path, youtube, instagram, facebook)
            VALUES (:profile_id, :name, :title, :short_bio, :full_bio, :image_path, :youtube, :instagram, :facebook)
        '''), photographer_data)
        conn.commit()
        print("✅ Default photographer added!")
    else:
        print("ℹ️  Photographer data already exists, skipping...")
    
    # Insert default event coordinator data
    print("\n6. Inserting default event coordinator data...")
    result = conn.execute(text('SELECT COUNT(*) FROM event_coordinators'))
    count = result.fetchone()[0]
    
    if count == 0:
        coordinator_data = {
            "profile_id": "coordinator_1",
            "name": "Isabella Moreno",
            "title": "Wedding & Party Coordinator",
            "short_bio": "Expert in planning seamless weddings and private parties. Making your vision a reality.",
            "image_path": "pages/images/corporate event.jpg",
            "full_bio": "Isabella Moreno is a dedicated event coordinator with over 8 years of experience in creating memorable celebrations. She specializes in weddings and private parties, ensuring every detail is perfect. Based in Dallas, TX, she works closely with clients to bring their vision to life.",
            "youtube": None,
            "instagram": None,
            "facebook": None
        }
        conn.execute(text('''
            INSERT INTO event_coordinators (profile_id, name, title, short_bio, full_bio, image_path, youtube, instagram, facebook)
            VALUES (:profile_id, :name, :title, :short_bio, :full_bio, :image_path, :youtube, :instagram, :facebook)
        '''), coordinator_data)
        conn.commit()
        print("✅ Default event coordinator added!")
    else:
        print("ℹ️  Event coordinator data already exists, skipping...")
    
    # Insert default DJ data
    print("\n7. Inserting default DJ data...")
    result = conn.execute(text('SELECT COUNT(*) FROM djs'))
    count = result.fetchone()[0]
    
    if count == 0:
        dj_data = [
            {
                "profile_id": "dj_1",
                "name": "DJ Tayzer",
                "title": "Master DJ & Event Specialist",
                "short_bio": "Expert in mixing beats and creating unforgettable atmospheres. Specializing in weddings and parties.",
                "image_path": "pages/images/djs_tay.png",
                "full_bio": "DJ Tayzer is a seasoned professional with over 10 years of experience in the DJ industry. Known for his seamless transitions and crowd-engaging sets, he specializes in weddings, corporate events, and private parties. Based in Dallas, TX, he brings energy and professionalism to every gig.",
                "youtube": "https://www.youtube.com/@djtayzer",
                "instagram": "https://www.instagram.com/tayzer/",
                "facebook": "https://www.facebook.com/profile.php?id=61574735690575"
            },
            {
                "profile_id": "dj_2",
                "name": "DJ Tyler",
                "title": "House Music DJ",
                "short_bio": "Master of house music beats, creating energetic and soulful atmospheres. Specializing in dance parties and festivals.",
                "image_path": "pages/images/djs_tyler.png",
                "full_bio": "DJ Tyler is a passionate house music enthusiast with over 8 years of experience in the DJ industry. Known for his deep house sets and infectious vibes, he specializes in dance parties, festivals, and private events. Based in Dallas, TX, he brings soulful energy and professionalism to every gig.",
                "youtube": None,
                "instagram": None,
                "facebook": None
            }
        ]
        
        for dj in dj_data:
            conn.execute(text('''
                INSERT INTO djs (profile_id, name, title, short_bio, full_bio, image_path, youtube, instagram, facebook)
                VALUES (:profile_id, :name, :title, :short_bio, :full_bio, :image_path, :youtube, :instagram, :facebook)
            '''), dj)
        conn.commit()
        print("✅ Default DJs added!")
    else:
        print("ℹ️  DJ data already exists, skipping...")
    
    # Verify data
    print("\n8. Verifying data...")
    for table in ['photographers', 'event_coordinators', 'djs']:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
        count = result.fetchone()[0]
        print(f"   - {table}: {count} records")
    
    conn.close()
    print("\n" + "=" * 60)
    print("✅ PostgreSQL tables initialized successfully!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("=" * 60)
    import traceback
    traceback.print_exc()
