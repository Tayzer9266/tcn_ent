"""
Standalone Critical Path Testing for Client System
Tests database operations directly without Streamlit dependency
"""

from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import hashlib

# Direct database connection
connection_string = "postgresql://tcn_ent:Provident3333!@tcn.c54mcgea4luc.us-east-2.rds.amazonaws.com:5432/postgres"
engine = create_engine(connection_string)
conn = engine.connect()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

print("=" * 80)
print("CLIENT SYSTEM CRITICAL PATH TESTING (STANDALONE)")
print("=" * 80)

tests_passed = 0
tests_failed = 0

def test_result(test_name, passed, message=""):
    global tests_passed, tests_failed
    if passed:
        tests_passed += 1
        status = "✅ PASS"
    else:
        tests_failed += 1
        status = "❌ FAIL"
    result = f"{status} - {test_name}"
    if message:
        result += f": {message}"
    print(result)
    return passed

# Generate unique email for testing
test_email = f"testclient_{datetime.now().strftime('%Y%m%d%H%M%S')}@test.com"

print("\n" + "=" * 80)
print("PHASE 1: DATABASE SCHEMA VERIFICATION")
print("=" * 80)

# Test 1: Verify clients table has new fields
print("\nTest 1: Verify clients table schema...")
try:
    result = conn.execute(text("""
        SELECT column_name FROM information_schema.columns 
        WHERE table_name = 'clients' 
        AND column_name IN ('password', 'user_type', 'is_active')
    """))
    columns = [row[0] for row in result.fetchall()]
    test_result("Clients Table Schema", len(columns) == 3, f"Found {len(columns)}/3 required columns")
except Exception as e:
    test_result("Clients Table Schema", False, str(e))

# Test 2: Verify quotes table exists
print("\nTest 2: Verify quotes table exists...")
try:
    result = conn.execute(text("SELECT COUNT(*) FROM quotes"))
    count = result.fetchone()[0]
    test_result("Quotes Table Exists", True, f"Table has {count} records")
except Exception as e:
    test_result("Quotes Table Exists", False, str(e))

# Test 3: Verify messages table exists
print("\nTest 3: Verify messages table exists...")
try:
    result = conn.execute(text("SELECT COUNT(*) FROM messages"))
    count = result.fetchone()[0]
    test_result("Messages Table Exists", True, f"Table has {count} records")
except Exception as e:
    test_result("Messages Table Exists", False, str(e))

print("\n" + "=" * 80)
print("PHASE 2: CLIENT REGISTRATION")
print("=" * 80)

# Test 4: Register new client
print("\nTest 4: Register new client...")
try:
    hashed_password = hash_password("TestPass123")
    result = conn.execute(text("""
        INSERT INTO clients (first_name, last_name, email, phone_number, password, user_type, is_active, created_at, updated_at)
        VALUES (:first_name, :last_name, :email, :phone_number, :password, 'client', TRUE, :created_at, :updated_at)
        RETURNING client_id
    """), {
        "first_name": "Test",
        "last_name": "Client",
        "email": test_email,
        "phone_number": "(214) 555-9999",
        "password": hashed_password,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    })
    test_client_id = result.fetchone()[0]
    conn.commit()
    test_result("Client Registration", True, f"Client ID: {test_client_id}")
except Exception as e:
    test_result("Client Registration", False, str(e))
    conn.rollback()

print("\n" + "=" * 80)
print("PHASE 3: CLIENT AUTHENTICATION")
print("=" * 80)

# Test 5: Authenticate client
print("\nTest 5: Authenticate client...")
try:
    hashed_password = hash_password("TestPass123")
    result = conn.execute(text("""
        SELECT client_id, first_name, last_name, email 
        FROM clients 
        WHERE email = :email AND password = :password AND is_active = TRUE
    """), {"email": test_email, "password": hashed_password})
    row = result.fetchone()
    test_result("Client Authentication", row is not None, f"Found client: {row[1] if row else 'N/A'}")
except Exception as e:
    test_result("Client Authentication", False, str(e))

print("\n" + "=" * 80)
print("PHASE 4: EVENT CREATION")
print("=" * 80)

# Test 6: Create event
print("\nTest 6: Create event...")
try:
    result = conn.execute(text("""
        INSERT INTO events (
            client_id, event_name, event_type, event_date, event_location,
            start_time, end_time, service_hours, venue, estimated_guest,
            estimated_budget, description, event_status, created_at, updated_at
        ) VALUES (
            :client_id, :event_name, :event_type, :event_date, :event_location,
            :start_time, :end_time, :service_hours, :venue, :estimated_guest,
            :estimated_budget, :description, 'pending', :created_at, :updated_at
        ) RETURNING event_id
    """), {
        "client_id": test_client_id,
        "event_name": "Test Wedding Reception",
        "event_type": "Wedding",
        "event_date": datetime.now() + timedelta(days=30),
        "event_location": "123 Test St, Dallas, TX",
        "start_time": "18:00:00",
        "end_time": "23:00:00",
        "service_hours": 5.0,
        "venue": "Test Venue",
        "estimated_guest": 100,
        "estimated_budget": 2000.00,
        "description": "Test wedding event",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    })
    test_event_id = result.fetchone()[0]
    conn.commit()
    test_result("Event Creation", True, f"Event ID: {test_event_id}")
except Exception as e:
    test_result("Event Creation", False, str(e))
    conn.rollback()

# Test 7: Link service to event
print("\nTest 7: Link service to event...")
try:
    # Get a service
    result = conn.execute(text("SELECT service_id FROM services LIMIT 1"))
    service_id = result.fetchone()[0]
    
    conn.execute(text("""
        INSERT INTO event_services (event_id, service_id, quantity, created_at)
        VALUES (:event_id, :service_id, 1, :created_at)
    """), {
        "event_id": test_event_id,
        "service_id": service_id,
        "created_at": datetime.now()
    })
    conn.commit()
    test_result("Link Service to Event", True, f"Service ID: {service_id}")
except Exception as e:
    test_result("Link Service to Event", False, str(e))
    conn.rollback()

print("\n" + "=" * 80)
print("PHASE 5: MESSAGING")
print("=" * 80)

# Test 8: Send message
print("\nTest 8: Send message...")
try:
    result = conn.execute(text("""
        INSERT INTO messages (event_id, sender_id, sender_type, sender_name, message_text, created_at)
        VALUES (:event_id, :sender_id, :sender_type, :sender_name, :message_text, :created_at)
        RETURNING message_id
    """), {
        "event_id": test_event_id,
        "sender_id": test_client_id,
        "sender_type": "client",
        "sender_name": "Test Client",
        "message_text": "Hello! I'm interested in your services.",
        "created_at": datetime.now()
    })
    message_id = result.fetchone()[0]
    conn.commit()
    test_result("Send Message", True, f"Message ID: {message_id}")
except Exception as e:
    test_result("Send Message", False, str(e))
    conn.rollback()

# Test 9: Retrieve messages
print("\nTest 9: Retrieve messages...")
try:
    result = conn.execute(text("""
        SELECT message_id, sender_name, message_text 
        FROM messages 
        WHERE event_id = :event_id
    """), {"event_id": test_event_id})
    messages = result.fetchall()
    test_result("Retrieve Messages", len(messages) > 0, f"Found {len(messages)} message(s)")
except Exception as e:
    test_result("Retrieve Messages", False, str(e))

print("\n" + "=" * 80)
print("PHASE 6: QUOTE MANAGEMENT")
print("=" * 80)

# Test 10: Create quote
print("\nTest 10: Create quote...")
try:
    result = conn.execute(text("""
        INSERT INTO quotes (
            event_id, client_id, professional_id, professional_type, professional_name,
            quote_amount, quote_status, quote_details, valid_until, created_at, updated_at
        ) SELECT 
            :event_id, e.client_id, 1, 'dj', 'DJ Tayzer',
            :quote_amount, 'sent', :quote_details, :valid_until, :created_at, :updated_at
        FROM events e WHERE e.event_id = :event_id
        RETURNING quote_id
    """), {
        "event_id": test_event_id,
        "quote_amount": 1500.00,
        "quote_details": "Complete DJ package for 5 hours",
        "valid_until": datetime.now() + timedelta(days=30),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    })
    quote_id = result.fetchone()[0]
    conn.commit()
    test_result("Create Quote", True, f"Quote ID: {quote_id}")
    test_quote_id = quote_id
except Exception as e:
    test_result("Create Quote", False, str(e))
    conn.rollback()

# Test 11: Retrieve quotes
print("\nTest 11: Retrieve quotes...")
try:
    result = conn.execute(text("""
        SELECT quote_id, professional_name, quote_amount, quote_status
        FROM quotes WHERE event_id = :event_id
    """), {"event_id": test_event_id})
    quotes = result.fetchall()
    test_result("Retrieve Quotes", len(quotes) > 0, f"Found {len(quotes)} quote(s)")
    if quotes:
        for quote in quotes:
            print(f"   Quote ID: {quote[0]}, Professional: {quote[1]}, Amount: ${quote[2]}, Status: {quote[3]}")
except Exception as e:
    test_result("Retrieve Quotes", False, str(e))

# Test 12: Update quote status
print("\nTest 12: Update quote status...")
try:
    conn.execute(text("""
        UPDATE quotes SET quote_status = 'accepted', updated_at = :updated_at
        WHERE quote_id = :quote_id
    """), {
        "quote_id": test_quote_id,
        "updated_at": datetime.now()
    })
    conn.commit()
    test_result("Update Quote Status", True, "Status changed to 'accepted'")
except Exception as e:
    test_result("Update Quote Status", False, str(e))
    conn.rollback()

print("\n" + "=" * 80)
print("PHASE 7: COMPLEX QUERIES")
print("=" * 80)

# Test 13: Get all quote requests (professional view)
print("\nTest 13: Get all quote requests...")
try:
    result = conn.execute(text("""
        SELECT e.event_id, e.event_name, c.first_name, c.last_name, c.email,
               COUNT(DISTINCT q.quote_id) as quote_count
        FROM events e
        JOIN clients c ON e.client_id = c.client_id
        LEFT JOIN quotes q ON e.event_id = q.event_id
        WHERE e.deleted_at IS NULL
        GROUP BY e.event_id, c.client_id
        LIMIT 5
    """))
    requests = result.fetchall()
    test_result("Get Quote Requests", len(requests) > 0, f"Found {len(requests)} request(s)")
except Exception as e:
    test_result("Get Quote Requests", False, str(e))

# Test 14: Get client events with stats
print("\nTest 14: Get client events with stats...")
try:
    result = conn.execute(text("""
        SELECT e.event_id, e.event_name,
               COUNT(DISTINCT q.quote_id) as quote_count,
               COUNT(DISTINCT m.message_id) as message_count
        FROM events e
        LEFT JOIN quotes q ON e.event_id = q.event_id
        LEFT JOIN messages m ON e.event_id = m.event_id
        WHERE e.client_id = :client_id
        GROUP BY e.event_id
    """), {"client_id": test_client_id})
    events = result.fetchall()
    test_result("Get Client Events with Stats", len(events) > 0, f"Found {len(events)} event(s)")
    if events:
        for event in events:
            print(f"   Event: {event[1]}, Quotes: {event[2]}, Messages: {event[3]}")
except Exception as e:
    test_result("Get Client Events with Stats", False, str(e))

print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)

print(f"\nTotal Tests: {tests_passed + tests_failed}")
print(f"✅ Passed: {tests_passed}")
print(f"❌ Failed: {tests_failed}")
print(f"Success Rate: {(tests_passed / (tests_passed + tests_failed) * 100):.1f}%")

if tests_failed == 0:
    print("\n" + "=" * 80)
    print("🎉 ALL CRITICAL PATH TESTS PASSED!")
    print("=" * 80)
    print("\nThe system is ready for use. Key workflows verified:")
    print("✅ Database schema correct")
    print("✅ Client registration works")
    print("✅ Client authentication works")
    print("✅ Event creation works")
    print("✅ Service linking works")
    print("✅ Messaging system works")
    print("✅ Quote management works")
    print("✅ Complex queries work")
else:
    print("\n" + "=" * 80)
    print("⚠️  SOME TESTS FAILED - REVIEW REQUIRED")
    print("=" * 80)

conn.close()
print("\n" + "=" * 80)
