"""
Initialize Client Login & Quote Management System
- Add password field to clients table
- Create quotes table
- Create messages table
- Populate services table
"""

from sqlalchemy import create_engine, text

# Connect to database
connection_string = "postgresql://tcn_ent:Provident3333!@tcn.c54mcgea4luc.us-east-2.rds.amazonaws.com:5432/postgres"
engine = create_engine(connection_string)
conn = engine.connect()

print("=" * 70)
print("CLIENT SYSTEM DATABASE INITIALIZATION")
print("=" * 70)

try:
    # 1. Add fields to clients table
    print("\n1. Adding fields to clients table...")
    
    # Add password field
    conn.execute(text('''
        ALTER TABLE clients 
        ADD COLUMN IF NOT EXISTS password VARCHAR(255)
    '''))
    print("   ✅ Added password field")
    
    # Add user_type field
    conn.execute(text('''
        ALTER TABLE clients 
        ADD COLUMN IF NOT EXISTS user_type VARCHAR(20) DEFAULT 'client'
    '''))
    print("   ✅ Added user_type field")
    
    # Add is_active field
    conn.execute(text('''
        ALTER TABLE clients 
        ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE
    '''))
    print("   ✅ Added is_active field")
    
    conn.commit()
    
    # 2. Create quotes table
    print("\n2. Creating quotes table...")
    conn.execute(text('''
        CREATE TABLE IF NOT EXISTS quotes (
            quote_id SERIAL PRIMARY KEY,
            event_id INTEGER REFERENCES events(event_id),
            client_id INTEGER REFERENCES clients(client_id),
            professional_id INTEGER,
            professional_type VARCHAR(50),
            professional_name VARCHAR(255),
            quote_amount NUMERIC(10,2),
            quote_status VARCHAR(50) DEFAULT 'pending',
            quote_details TEXT,
            valid_until TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''))
    print("   ✅ Created quotes table")
    conn.commit()
    
    # 3. Create messages table
    print("\n3. Creating messages table...")
    conn.execute(text('''
        CREATE TABLE IF NOT EXISTS messages (
            message_id SERIAL PRIMARY KEY,
            event_id INTEGER REFERENCES events(event_id),
            sender_id INTEGER,
            sender_type VARCHAR(20),
            sender_name VARCHAR(255),
            message_text TEXT,
            is_read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''))
    print("   ✅ Created messages table")
    conn.commit()
    
    # 4. Check and populate services table
    print("\n4. Checking services table...")
    result = conn.execute(text('SELECT COUNT(*) FROM services'))
    count = result.fetchone()[0]
    
    if count == 0:
        print("   📝 Populating services table with default services...")
        
        services = [
            {
                'name': 'DJ Services',
                'description': 'Professional DJ services for your event with music, MC services, and entertainment',
                'price': 500.00,
                'market_price': 800.00
            },
            {
                'name': 'Photography Services',
                'description': 'Professional photography services capturing every moment of your special event',
                'price': 800.00,
                'market_price': 1200.00
            },
            {
                'name': 'Event Coordination',
                'description': 'Complete event planning and coordination services to make your event perfect',
                'price': 1000.00,
                'market_price': 1500.00
            },
            {
                'name': 'Lighting & Effects',
                'description': 'Professional lighting, uplighting, and special effects for your event',
                'price': 300.00,
                'market_price': 500.00
            },
            {
                'name': 'Photo Booth',
                'description': 'Fun photo booth with props and instant prints for your guests',
                'price': 400.00,
                'market_price': 600.00
            }
        ]
        
        for service in services:
            conn.execute(text('''
                INSERT INTO services (service_name, service_description, price, market_price)
                VALUES (:name, :description, :price, :market_price)
            '''), service)
        
        conn.commit()
        print(f"   ✅ Added {len(services)} default services")
    else:
        print(f"   ✅ Services table already has {count} services")
    
    # 5. Verify tables
    print("\n5. Verifying table structure...")
    
    # Check clients table
    result = conn.execute(text('''
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'clients' 
        AND column_name IN ('password', 'user_type', 'is_active')
        ORDER BY column_name
    '''))
    client_cols = result.fetchall()
    print(f"   ✅ Clients table: {len(client_cols)} new columns added")
    for col in client_cols:
        print(f"      - {col[0]}: {col[1]}")
    
    # Check quotes table
    result = conn.execute(text('''
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'quotes'
        ORDER BY ordinal_position
    '''))
    quote_cols = result.fetchall()
    print(f"   ✅ Quotes table: {len(quote_cols)} columns")
    
    # Check messages table
    result = conn.execute(text('''
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'messages'
        ORDER BY ordinal_position
    '''))
    message_cols = result.fetchall()
    print(f"   ✅ Messages table: {len(message_cols)} columns")
    
    print("\n" + "=" * 70)
    print("✅ CLIENT SYSTEM DATABASE INITIALIZATION COMPLETE!")
    print("=" * 70)
    print("\nNext Steps:")
    print("1. Create client_manager.py for authentication")
    print("2. Create client registration page")
    print("3. Update login page to support clients")
    print("4. Create client dashboard")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    conn.rollback()
    raise
finally:
    conn.close()
