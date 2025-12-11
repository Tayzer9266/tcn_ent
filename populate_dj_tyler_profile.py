"""
Script to populate DJ Tyler's profile with complete information
Including gallery images, videos, reviews, and detailed bio
"""

from sqlalchemy import create_engine, text
import json

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
print("Populating DJ Tyler's Complete Profile")
print("=" * 70)

try:
    engine = create_engine(connection_string)
    conn = engine.connect()
    print("\n✅ Connected to database")
    
    # DJ Tyler's complete profile data
    profile_data = {
        'profile_id': 'dj_2',
        'name': 'DJ Tyler',
        'title': 'House Music Specialist & Event DJ',
        'short_bio': 'Master of house music beats, creating energetic and soulful atmospheres. Specializing in dance parties, festivals, and upscale events.',
        'full_bio': '''DJ Tyler is a passionate house music enthusiast with over 8 years of experience in the DJ industry. Known for his deep house sets and infectious vibes, he specializes in dance parties, festivals, and private events.

Tyler's journey into DJing began in college, where he fell in love with the underground house music scene. Since then, he has performed at numerous venues across Texas, from intimate lounges to large-scale festivals. His signature style blends classic house grooves with modern electronic elements, creating a unique sound that keeps dance floors packed all night long.

What sets Tyler apart is his ability to read the crowd and adapt his sets accordingly. Whether it's a sophisticated cocktail party or an all-night dance marathon, he knows exactly how to set the mood and maintain the energy. His extensive music library spans decades of house music history, from Chicago house classics to the latest tech-house releases.

Tyler is also known for his professional setup, featuring state-of-the-art equipment including Pioneer CDJ-3000s, a DJM-900NXS2 mixer, and custom lighting rigs. He works closely with event planners to ensure seamless integration with your event's theme and atmosphere.

Based in Dallas, TX, Tyler is available for weddings, corporate events, private parties, and festivals throughout Texas and beyond.''',
        'overview_text': '''🎵 House Music Specialist | 8+ Years Experience | 160+ Events

I bring the energy and sophistication of house music to your events. Whether you're planning an upscale cocktail party, a wedding reception, or an all-night dance party, I create the perfect atmosphere with carefully curated house music selections.

My sets feature:
• Deep House & Tech House
• Classic Chicago House
• Soulful & Vocal House
• Progressive & Melodic House
• Custom mixing tailored to your event

Professional equipment, extensive music library, and a passion for creating unforgettable experiences. Let's make your event legendary!''',
        'years_experience': 8,
        'events_completed': 160,
        'email': 'tyler.beats@tcnentertainment.com',
        'phone': '(214) 555-0104',
        'website': 'https://www.djtylerbeats.com',
        'youtube': 'https://www.youtube.com/@djtylerhouse',
        'instagram': 'https://www.instagram.com/djtylerbeats/',
        'facebook': 'https://www.facebook.com/djtylerofficial',
        'service_city': 'Dallas',
        'service_state': 'Texas',
        'service_radius_miles': 100,
        'profile_video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',  # Main profile video
        'gallery_images': json.dumps([
            'pages/images/djs_tyler.png',
            'pages/images/work_night.jpg',
            'pages/images/dance_party.jpg',
            'pages/images/party.jpg',
            'pages/images/reception.jpg',
            'pages/images/work_siepe.jpg'
        ]),
        'gallery_videos': json.dumps([
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://www.youtube.com/watch?v=jNQXAC9IVRw'
        ])
    }
    
    # Update DJ Tyler's profile
    print("\n1. Updating DJ Tyler's profile...")
    update_query = text('''
        UPDATE djs SET
            name = :name,
            title = :title,
            short_bio = :short_bio,
            full_bio = :full_bio,
            overview_text = :overview_text,
            years_experience = :years_experience,
            events_completed = :events_completed,
            email = :email,
            phone = :phone,
            website = :website,
            youtube = :youtube,
            instagram = :instagram,
            facebook = :facebook,
            service_city = :service_city,
            service_state = :service_state,
            service_radius_miles = :service_radius_miles,
            profile_video_url = :profile_video_url,
            gallery_images = :gallery_images,
            gallery_videos = :gallery_videos,
            updated_at = CURRENT_TIMESTAMP
        WHERE profile_id = :profile_id
    ''')
    
    conn.execute(update_query, profile_data)
    conn.commit()
    print("   ✅ Profile updated successfully!")
    
    # Add reviews for DJ Tyler
    print("\n2. Adding reviews for DJ Tyler...")
    
    reviews = [
        {
            'professional_type': 'djs',
            'professional_id': 'dj_2',
            'client_id': None,
            'client_name': 'Marcus Johnson',
            'rating': 5,
            'review_title': 'Perfect House Music Vibes!',
            'review_text': 'DJ Tyler absolutely killed it at our corporate event! His house music selection was perfect - sophisticated enough for our executives but energetic enough to get everyone dancing. The transitions were seamless and he read the crowd perfectly. Highly recommend for any upscale event!',
            'event_type': 'Corporate Event',
            'event_date': '2024-11-15',
            'verified_booking': True,
            'helpful_count': 18
        },
        {
            'professional_type': 'djs',
            'professional_id': 'dj_2',
            'client_id': None,
            'client_name': 'Jessica Martinez',
            'rating': 5,
            'review_title': 'Made Our Wedding Reception Amazing!',
            'review_text': 'We hired DJ Tyler for our wedding reception and he exceeded all expectations. He played a perfect mix of house music during cocktail hour and then transitioned beautifully into more upbeat tracks for dancing. Our guests are still talking about how great the music was! Professional, punctual, and talented.',
            'event_type': 'Wedding',
            'event_date': '2024-10-20',
            'verified_booking': True,
            'helpful_count': 22
        },
        {
            'professional_type': 'djs',
            'professional_id': 'dj_2',
            'client_id': None,
            'client_name': 'David Chen',
            'rating': 5,
            'review_title': 'Best DJ for House Music Events',
            'review_text': 'Tyler is the real deal when it comes to house music. Hired him for our annual company party and he brought incredible energy. His equipment setup was top-notch and his music selection was perfect. Everyone was on the dance floor all night!',
            'event_type': 'Private Party',
            'event_date': '2024-09-08',
            'verified_booking': True,
            'helpful_count': 15
        },
        {
            'professional_type': 'djs',
            'professional_id': 'dj_2',
            'client_id': None,
            'client_name': 'Amanda Rodriguez',
            'rating': 5,
            'review_title': 'Incredible Energy and Professionalism',
            'review_text': 'DJ Tyler brought amazing vibes to our birthday celebration. His deep house selections were exactly what we wanted. He was professional, arrived early to set up, and kept the party going strong until the very end. Would definitely book again!',
            'event_type': 'Birthday Party',
            'event_date': '2024-08-25',
            'verified_booking': True,
            'helpful_count': 12
        },
        {
            'professional_type': 'djs',
            'professional_id': 'dj_2',
            'client_id': None,
            'client_name': 'Robert Thompson',
            'rating': 4,
            'review_title': 'Great DJ, Excellent Music Selection',
            'review_text': 'Tyler did a fantastic job at our fundraiser event. The house music was perfect for the atmosphere we wanted to create. Only minor issue was some technical difficulties at the start, but he handled it professionally and the rest of the night was flawless.',
            'event_type': 'Fundraiser',
            'event_date': '2024-07-12',
            'verified_booking': True,
            'helpful_count': 8
        }
    ]
    
    # Check if reviews already exist
    check_query = text('''
        SELECT COUNT(*) FROM professional_reviews 
        WHERE professional_type = 'djs' AND professional_id = 'dj_2'
    ''')
    result = conn.execute(check_query)
    existing_count = result.fetchone()[0]
    
    if existing_count == 0:
        insert_query = text('''
            INSERT INTO professional_reviews (
                professional_type, professional_id, client_id, client_name,
                rating, review_title, review_text, event_type, event_date,
                verified_booking, helpful_count
            ) VALUES (
                :professional_type, :professional_id, :client_id, :client_name,
                :rating, :review_title, :review_text, :event_type, :event_date,
                :verified_booking, :helpful_count
            )
        ''')
        
        for review in reviews:
            conn.execute(insert_query, review)
        
        conn.commit()
        print(f"   ✅ Added {len(reviews)} reviews!")
    else:
        print(f"   ℹ️  DJ Tyler already has {existing_count} reviews, skipping...")
    
    # Update review statistics
    print("\n3. Updating review statistics...")
    stats_query = text('''
        UPDATE djs
        SET 
            average_rating = COALESCE((
                SELECT ROUND(AVG(rating)::numeric, 2)
                FROM professional_reviews
                WHERE professional_type = 'djs'
                AND professional_id = 'dj_2'
            ), 0.00),
            total_reviews = COALESCE((
                SELECT COUNT(*)
                FROM professional_reviews
                WHERE professional_type = 'djs'
                AND professional_id = 'dj_2'
            ), 0)
        WHERE profile_id = 'dj_2'
    ''')
    
    conn.execute(stats_query)
    conn.commit()
    print("   ✅ Statistics updated!")
    
    # Display final profile
    print("\n4. Verifying DJ Tyler's complete profile...")
    verify_query = text('''
        SELECT name, title, years_experience, events_completed, 
               average_rating, total_reviews, email, phone, website,
               service_city, service_state, service_radius_miles
        FROM djs
        WHERE profile_id = 'dj_2'
    ''')
    
    result = conn.execute(verify_query)
    profile = result.fetchone()
    
    print(f"\n   📋 PROFILE SUMMARY:")
    print(f"   Name: {profile[0]}")
    print(f"   Title: {profile[1]}")
    print(f"   Experience: {profile[2]} years")
    print(f"   Events Completed: {profile[3]}")
    print(f"   Average Rating: {profile[4]}/5.0 ⭐")
    print(f"   Total Reviews: {profile[5]}")
    print(f"   Email: {profile[6]}")
    print(f"   Phone: {profile[7]}")
    print(f"   Website: {profile[8]}")
    print(f"   Service Area: {profile[9]}, {profile[10]} ({profile[11]} miles radius)")
    
    # Display reviews
    print(f"\n   📝 REVIEWS:")
    review_query = text('''
        SELECT client_name, rating, review_title, event_type
        FROM professional_reviews
        WHERE professional_type = 'djs' AND professional_id = 'dj_2'
        ORDER BY created_at DESC
    ''')
    
    result = conn.execute(review_query)
    reviews_list = result.fetchall()
    
    for review in reviews_list:
        stars = "⭐" * review[1]
        print(f"      {stars} {review[0]} - \"{review[2]}\" ({review[3]})")
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("✅ DJ Tyler's profile is now complete!")
    print("=" * 70)
    print("\nYou can view his full profile at:")
    print("pages/98_Professional_Profile.py?profile_type=djs&profile_id=dj_2")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
