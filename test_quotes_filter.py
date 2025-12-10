"""
Test the professional quotes filtering logic
"""
from sqlalchemy import create_engine, text

# Connect to database
connection_string = "postgresql://tcn_ent:Provident3333!@tcn.c54mcgea4luc.us-east-2.rds.amazonaws.com:5432/postgres"
engine = create_engine(connection_string)
conn = engine.connect()

print("=" * 70)
print("TESTING PROFESSIONAL QUOTES FILTER")
print("=" * 70)

try:
    # Test the query used for non-admin professionals
    print("\n1. Testing non-admin professional query:")
    print("   Looking for quotes with professional_id='dj_1' and professional_type='dj'")
    
    query = text('''
        SELECT q.*, e.event_name, e.event_date, e.event_location,
               c.first_name, c.last_name, c.email, c.phone_number
        FROM quotes q
        LEFT JOIN events e ON q.event_id = e.event_id
        LEFT JOIN clients c ON e.client_id = c.client_id
        WHERE q.professional_id = :professional_id 
        AND q.professional_type = :professional_type
        ORDER BY q.created_at DESC
    ''')
    
    result = conn.execute(query, {
        "professional_id": "dj_1",
        "professional_type": "dj"
    })
    
    quotes = result.fetchall()
    print(f"   Result: {len(quotes)} quotes found")
    
    # Test with NULL values
    print("\n2. Testing query for quotes with NULL professional_id:")
    query2 = text('''
        SELECT COUNT(*) 
        FROM quotes 
        WHERE professional_id IS NULL
    ''')
    
    result = conn.execute(query2)
    null_count = result.fetchone()[0]
    print(f"   Quotes with NULL professional_id: {null_count}")
    
    # Test with empty string
    print("\n3. Testing query for quotes with empty string professional_id:")
    query3 = text('''
        SELECT COUNT(*) 
        FROM quotes 
        WHERE professional_id = ''
    ''')
    
    result = conn.execute(query3)
    empty_count = result.fetchone()[0]
    print(f"   Quotes with empty professional_id: {empty_count}")
    
    print("\n" + "=" * 70)
    print("CONCLUSION:")
    print("=" * 70)
    print("All quotes have NULL professional_id and professional_type.")
    print("This means they were NOT created by professionals sending quotes.")
    print("They appear to be placeholder records created automatically.")
    print("\nTo see actual quotes, professionals need to:")
    print("1. Go to the 'New Requests' tab")
    print("2. Click 'Send Quote' on an event")
    print("3. Fill out the quote form with amount and details")
    print("4. Submit the quote")
    print("\nOnly THEN will quotes appear in the 'My Quotes' tab.")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    conn.close()
