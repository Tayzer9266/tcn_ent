"""
Script to create professional_reviews table for client reviews

This table stores reviews from clients for professionals (DJs, Photographers, Event Coordinators)
"""

from sqlalchemy import create_engine, text

def create_reviews_table():
    """Create the professional_reviews table"""
    
    try:
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
        print("Creating Professional Reviews Table")
        print("=" * 70)
        
        # Create connection
        print("\n1. Connecting to PostgreSQL...")
        engine = create_engine(connection_string)
        conn = engine.connect()
        print("✅ Connected successfully!")
        
        # Create professional_reviews table
        print("\n2. Creating professional_reviews table...")
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS professional_reviews (
                review_id SERIAL PRIMARY KEY,
                professional_type VARCHAR(50) NOT NULL,
                professional_id VARCHAR(100) NOT NULL,
                client_id INTEGER,
                client_name VARCHAR(255) NOT NULL,
                rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                review_title VARCHAR(255),
                review_text TEXT NOT NULL,
                event_type VARCHAR(100),
                event_date DATE,
                verified_booking BOOLEAN DEFAULT FALSE,
                helpful_count INTEGER DEFAULT 0,
                response_text TEXT,
                response_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_professional 
                    CHECK (professional_type IN ('djs', 'photographers', 'event_coordinators'))
            )
        '''))
        conn.commit()
        print("✅ professional_reviews table created!")
        
        # Create indexes for better query performance
        print("\n3. Creating indexes...")
        
        try:
            conn.execute(text('''
                CREATE INDEX IF NOT EXISTS idx_reviews_professional 
                ON professional_reviews(professional_type, professional_id)
            '''))
            print("   ✅ Index on professional_type and professional_id created")
            
            conn.execute(text('''
                CREATE INDEX IF NOT EXISTS idx_reviews_client 
                ON professional_reviews(client_id)
            '''))
            print("   ✅ Index on client_id created")
            
            conn.execute(text('''
                CREATE INDEX IF NOT EXISTS idx_reviews_rating 
                ON professional_reviews(rating)
            '''))
            print("   ✅ Index on rating created")
            
            conn.execute(text('''
                CREATE INDEX IF NOT EXISTS idx_reviews_created 
                ON professional_reviews(created_at DESC)
            '''))
            print("   ✅ Index on created_at created")
            
            conn.commit()
            
        except Exception as e:
            print(f"   ⚠️  Some indexes may already exist: {e}")
        
        # Insert sample reviews for testing
        print("\n4. Inserting sample reviews...")
        
        sample_reviews = [
            {
                'professional_type': 'djs',
                'professional_id': 'dj_1',
                'client_id': None,
                'client_name': 'Kate H.',
                'rating': 5,
                'review_title': 'Best DJ Ever!',
                'review_text': 'DJ Tayzer was amazing at our charity event! He read the crowd perfectly and kept everyone dancing all night.',
                'event_type': 'Charity Event',
                'event_date': '2025-06-28',
                'verified_booking': True,
                'helpful_count': 12
            },
            {
                'professional_type': 'djs',
                'professional_id': 'dj_1',
                'client_id': None,
                'client_name': 'Niki F.',
                'rating': 5,
                'review_title': 'Best DJ ever!!!',
                'review_text': 'DJ Tayzer showed up early, was super professional, and kept the energy high all day. Highly recommend!',
                'event_type': 'Wedding',
                'event_date': '2025-06-27',
                'verified_booking': True,
                'helpful_count': 8
            },
            {
                'professional_type': 'photographers',
                'professional_id': 'photographer_1',
                'client_id': None,
                'client_name': 'Michael R.',
                'rating': 5,
                'review_title': 'Stunning Photos!',
                'review_text': 'Samantha captured our wedding beautifully. Every photo tells a story. Highly professional and creative!',
                'event_type': 'Wedding',
                'event_date': '2025-05-15',
                'verified_booking': True,
                'helpful_count': 15
            },
            {
                'professional_type': 'event_coordinators',
                'professional_id': 'coordinator_1',
                'client_id': None,
                'client_name': 'Sarah T.',
                'rating': 5,
                'review_title': 'Flawless Execution',
                'review_text': 'Isabella made our wedding day stress-free. Everything was perfectly coordinated and on time!',
                'event_type': 'Wedding',
                'event_date': '2025-04-20',
                'verified_booking': True,
                'helpful_count': 10
            }
        ]
        
        # Check if reviews already exist
        result = conn.execute(text('SELECT COUNT(*) FROM professional_reviews'))
        count = result.fetchone()[0]
        
        if count == 0:
            for review in sample_reviews:
                conn.execute(text('''
                    INSERT INTO professional_reviews (
                        professional_type, professional_id, client_id, client_name,
                        rating, review_title, review_text, event_type, event_date,
                        verified_booking, helpful_count
                    ) VALUES (
                        :professional_type, :professional_id, :client_id, :client_name,
                        :rating, :review_title, :review_text, :event_type, :event_date,
                        :verified_booking, :helpful_count
                    )
                '''), review)
            
            conn.commit()
            print(f"   ✅ {len(sample_reviews)} sample reviews inserted!")
        else:
            print(f"   ℹ️  Reviews already exist ({count} reviews), skipping sample data...")
        
        # Update professional tables with review stats
        print("\n5. Updating professional tables with review statistics...")
        
        for prof_type in ['djs', 'photographers', 'event_coordinators']:
            # Calculate and update average ratings and review counts
            conn.execute(text(f'''
                UPDATE {prof_type} p
                SET 
                    average_rating = COALESCE((
                        SELECT ROUND(AVG(rating)::numeric, 2)
                        FROM professional_reviews r
                        WHERE r.professional_type = :prof_type
                        AND r.professional_id = p.profile_id
                    ), 0.00),
                    total_reviews = COALESCE((
                        SELECT COUNT(*)
                        FROM professional_reviews r
                        WHERE r.professional_type = :prof_type
                        AND r.professional_id = p.profile_id
                    ), 0)
            '''), {'prof_type': prof_type})
            
            conn.commit()
            print(f"   ✅ Updated {prof_type} review statistics")
        
        # Verify the table
        print("\n6. Verifying professional_reviews table...")
        result = conn.execute(text('''
            SELECT 
                professional_type,
                professional_id,
                client_name,
                rating,
                review_title,
                created_at
            FROM professional_reviews
            ORDER BY created_at DESC
            LIMIT 5
        '''))
        
        reviews = result.fetchall()
        print(f"\n   Sample Reviews ({len(reviews)} shown):")
        for review in reviews:
            print(f"      ⭐ {review[2]} rated {review[1]} ({review[0]}): {review[3]}/5")
            print(f"         \"{review[4]}\"")
        
        # Show updated professional stats
        print("\n7. Professional review statistics:")
        for prof_type in ['djs', 'photographers', 'event_coordinators']:
            result = conn.execute(text(f'''
                SELECT profile_id, name, average_rating, total_reviews
                FROM {prof_type}
                WHERE role != 'admin' OR role IS NULL
                ORDER BY average_rating DESC
            '''))
            
            profs = result.fetchall()
            print(f"\n   {prof_type.upper()}:")
            for prof in profs:
                stars = "⭐" * int(prof[2]) if prof[2] else "No ratings yet"
                print(f"      {prof[1]}: {prof[2]}/5.0 ({prof[3]} reviews) {stars}")
        
        conn.close()
        
        print("\n" + "=" * 70)
        print("✅ Professional reviews table created successfully!")
        print("=" * 70)
        print("\nNext Steps:")
        print("1. Update ProfileManager to handle reviews")
        print("2. Create detailed profile pages with slideshow gallery")
        print("3. Create review submission page")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_reviews_table()
