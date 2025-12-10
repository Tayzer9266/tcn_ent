"""
Debug script to check quotes in database
"""
from sqlalchemy import create_engine, text

# Connect to database
connection_string = "postgresql://tcn_ent:Provident3333!@tcn.c54mcgea4luc.us-east-2.rds.amazonaws.com:5432/postgres"
engine = create_engine(connection_string)
conn = engine.connect()

print("=" * 70)
print("QUOTES DEBUG - Checking database for quotes")
print("=" * 70)

try:
    # Check total quotes in database
    print("\n1. Total quotes in database:")
    result = conn.execute(text("SELECT COUNT(*) FROM quotes"))
    total_quotes = result.fetchone()[0]
    print(f"   Total quotes: {total_quotes}")
    
    if total_quotes > 0:
        # Get all quotes with event details
        print("\n2. All quotes with event details:")
        query = text('''
            SELECT q.quote_id, q.event_id, q.professional_id, q.professional_type, 
                   q.professional_name, q.quote_amount, q.quote_status,
                   e.event_name, e.event_date, e.event_location,
                   c.first_name, c.last_name, c.email
            FROM quotes q
            LEFT JOIN events e ON q.event_id = e.event_id
            LEFT JOIN clients c ON e.client_id = c.client_id
            ORDER BY q.created_at DESC
        ''')
        
        result = conn.execute(query)
        quotes = result.fetchall()
        
        for idx, quote in enumerate(quotes, 1):
            print(f"\n   Quote #{idx}:")
            print(f"      Quote ID: {quote[0]}")
            print(f"      Event ID: {quote[1]}")
            print(f"      Professional ID: {quote[2]}")
            print(f"      Professional Type: {quote[3]}")
            print(f"      Professional Name: {quote[4]}")
            amount = quote[5] if quote[5] is not None else 0
            print(f"      Amount: ${amount:,.2f}")
            print(f"      Status: {quote[6]}")
            print(f"      Event Name: {quote[7]}")
            print(f"      Event Date: {quote[8]}")
            print(f"      Event Location: {quote[9]}")
            print(f"      Client: {quote[10]} {quote[11]}")
            print(f"      Client Email: {quote[12]}")
        
        # Check the query used in get_professional_quotes for admin
        print("\n3. Testing admin query (FROM events LEFT JOIN quotes):")
        admin_query = text('''
            SELECT q.*, e.event_name, e.event_date, e.event_location,
                   c.first_name, c.last_name, c.email, c.phone_number
            FROM events e
            LEFT JOIN quotes q ON q.event_id = e.event_id
            LEFT JOIN clients c ON e.client_id = c.client_id
            ORDER BY q.created_at DESC
        ''')
        
        result = conn.execute(admin_query)
        admin_quotes = result.fetchall()
        print(f"   Admin query returned {len(admin_quotes)} rows")
        
        # Count how many have NULL quote_id
        null_quotes = sum(1 for q in admin_quotes if q[0] is None)
        print(f"   Rows with NULL quote_id: {null_quotes}")
        print(f"   Rows with actual quotes: {len(admin_quotes) - null_quotes}")
        
        # Check if there are events without quotes
        print("\n4. Events without quotes:")
        result = conn.execute(text('''
            SELECT COUNT(*) 
            FROM events e
            LEFT JOIN quotes q ON e.event_id = q.event_id
            WHERE q.quote_id IS NULL
        '''))
        events_without_quotes = result.fetchone()[0]
        print(f"   Events without quotes: {events_without_quotes}")
        
    else:
        print("\n   ⚠️ No quotes found in database!")
        print("   This means no quotes have been created yet.")
    
    print("\n" + "=" * 70)
    print("DEBUG COMPLETE")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    conn.close()
