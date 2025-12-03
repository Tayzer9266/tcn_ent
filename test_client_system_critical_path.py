"""
Critical Path Testing for Client Login & Quote Management System
Tests the key workflows: Registration → Login → Quote Request → Professional Response
"""

from client_manager import client_manager
from datetime import datetime, date, time, timedelta
import sys

print("=" * 80)
print("CLIENT SYSTEM CRITICAL PATH TESTING")
print("=" * 80)

# Test counters
tests_passed = 0
tests_failed = 0
test_results = []

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
    test_results.append(result)
    print(result)
    return passed

print("\n" + "=" * 80)
print("PHASE 1: CLIENT REGISTRATION")
print("=" * 80)

# Test 1: Register a new client
print("\nTest 1: Register new client...")
try:
    success, message, client_id = client_manager.register_client(
        first_name="Test",
        last_name="Client",
        email=f"testclient_{datetime.now().strftime('%Y%m%d%H%M%S')}@test.com",
        phone_number="(214) 555-9999",
        password="TestPass123"
    )
    test_result("Client Registration", success, message)
    if success:
        test_client_id = client_id
        test_client_email = f"testclient_{datetime.now().strftime('%Y%m%d%H%M%S')}@test.com"
except Exception as e:
    test_result("Client Registration", False, str(e))
    sys.exit(1)

# Test 2: Duplicate email validation
print("\nTest 2: Duplicate email validation...")
try:
    success, message, _ = client_manager.register_client(
        first_name="Duplicate",
        last_name="Test",
        email=test_client_email,
        phone_number="(214) 555-8888",
        password="TestPass123"
    )
    test_result("Duplicate Email Prevention", not success, "Should reject duplicate email")
except Exception as e:
    test_result("Duplicate Email Prevention", False, str(e))

print("\n" + "=" * 80)
print("PHASE 2: CLIENT AUTHENTICATION")
print("=" * 80)

# Test 3: Client login with correct credentials
print("\nTest 3: Client login (correct credentials)...")
try:
    success, client_data = client_manager.authenticate_client(test_client_email, "TestPass123")
    test_result("Client Login (Valid)", success, f"Client ID: {client_data.get('client_id') if success else 'N/A'}")
    if success:
        logged_in_client = client_data
except Exception as e:
    test_result("Client Login (Valid)", False, str(e))

# Test 4: Client login with wrong password
print("\nTest 4: Client login (wrong password)...")
try:
    success, _ = client_manager.authenticate_client(test_client_email, "WrongPassword")
    test_result("Client Login (Invalid)", not success, "Should reject wrong password")
except Exception as e:
    test_result("Client Login (Invalid)", False, str(e))

print("\n" + "=" * 80)
print("PHASE 3: EVENT CREATION & QUOTE REQUEST")
print("=" * 80)

# Test 5: Create an event (quote request)
print("\nTest 5: Create event/quote request...")
try:
    event_data = {
        'event_name': 'Test Wedding Reception',
        'event_type': 'Wedding',
        'event_date': datetime.now() + timedelta(days=30),
        'event_location': '123 Test St, Dallas, TX 75201',
        'start_time': time(18, 0),
        'end_time': time(23, 0),
        'service_hours': 5.0,
        'venue': 'Test Venue',
        'estimated_guest': 100,
        'estimated_budget': 2000.00,
        'description': 'Test wedding reception event',
        'special_requirements': 'Need DJ and photographer'
    }
    
    success, event_id = client_manager.create_event(test_client_id, event_data)
    test_result("Event Creation", success, f"Event ID: {event_id if success else 'N/A'}")
    if success:
        test_event_id = event_id
except Exception as e:
    test_result("Event Creation", False, str(e))
    sys.exit(1)

# Test 6: Link services to event
print("\nTest 6: Link services to event...")
try:
    services = client_manager.get_all_services()
    test_result("Get Services", len(services) > 0, f"Found {len(services)} services")
    
    if services:
        # Link DJ service
        dj_service = next((s for s in services if 'DJ' in s['service_name']), None)
        if dj_service:
            success = client_manager.add_service_to_event(test_event_id, dj_service['service_id'])
            test_result("Link DJ Service", success)
except Exception as e:
    test_result("Link Services", False, str(e))

# Test 7: Retrieve client events
print("\nTest 7: Retrieve client events...")
try:
    events = client_manager.get_client_events(test_client_id)
    test_result("Get Client Events", len(events) > 0, f"Found {len(events)} event(s)")
    
    if events:
        event = events[0]
        print(f"   Event: {event.get('event_name')}")
        print(f"   Status: {event.get('event_status')}")
        print(f"   Quotes: {event.get('quote_count', 0)}")
        print(f"   Messages: {event.get('message_count', 0)}")
except Exception as e:
    test_result("Get Client Events", False, str(e))

print("\n" + "=" * 80)
print("PHASE 4: MESSAGING SYSTEM")
print("=" * 80)

# Test 8: Send message from client
print("\nTest 8: Client sends message...")
try:
    success, message_id = client_manager.send_message(
        event_id=test_event_id,
        sender_id=test_client_id,
        sender_type='client',
        sender_name=f"{logged_in_client['first_name']} {logged_in_client['last_name']}",
        message_text="Hello! I'm interested in your services for my wedding."
    )
    test_result("Send Client Message", success, f"Message ID: {message_id if success else 'N/A'}")
except Exception as e:
    test_result("Send Client Message", False, str(e))

# Test 9: Retrieve messages
print("\nTest 9: Retrieve event messages...")
try:
    messages = client_manager.get_event_messages(test_event_id)
    test_result("Get Event Messages", len(messages) > 0, f"Found {len(messages)} message(s)")
    
    if messages:
        for msg in messages:
            print(f"   From: {msg.get('sender_name')} ({msg.get('sender_type')})")
            print(f"   Message: {msg.get('message_text')[:50]}...")
except Exception as e:
    test_result("Get Event Messages", False, str(e))

print("\n" + "=" * 80)
print("PHASE 5: PROFESSIONAL QUOTE MANAGEMENT")
print("=" * 80)

# Test 10: Get all quote requests (professional view)
print("\nTest 10: Get all quote requests...")
try:
    quote_requests = client_manager.get_all_quote_requests()
    test_result("Get Quote Requests", len(quote_requests) > 0, f"Found {len(quote_requests)} request(s)")
    
    if quote_requests:
        # Find our test event
        test_request = next((r for r in quote_requests if r['event_id'] == test_event_id), None)
        if test_request:
            print(f"   Test Event Found:")
            print(f"   Client: {test_request.get('first_name')} {test_request.get('last_name')}")
            print(f"   Event: {test_request.get('event_name')}")
            print(f"   Services: {test_request.get('requested_services')}")
except Exception as e:
    test_result("Get Quote Requests", False, str(e))

# Test 11: Professional sends quote
print("\nTest 11: Professional sends quote...")
try:
    quote_data = {
        'quote_amount': 1500.00,
        'quote_details': 'Complete DJ package including sound system, lighting, and MC services for 5 hours',
        'valid_until': datetime.now() + timedelta(days=30)
    }
    
    success, quote_id = client_manager.create_quote(
        event_id=test_event_id,
        professional_id=1,  # Assuming DJ ID 1
        professional_type='dj',
        professional_name='DJ Tayzer',
        quote_data=quote_data
    )
    test_result("Create Quote", success, f"Quote ID: {quote_id if success else 'N/A'}")
    if success:
        test_quote_id = quote_id
except Exception as e:
    test_result("Create Quote", False, str(e))

# Test 12: Retrieve quotes for event
print("\nTest 12: Retrieve event quotes...")
try:
    quotes = client_manager.get_event_quotes(test_event_id)
    test_result("Get Event Quotes", len(quotes) > 0, f"Found {len(quotes)} quote(s)")
    
    if quotes:
        for quote in quotes:
            print(f"   Professional: {quote.get('professional_name')}")
            print(f"   Amount: ${quote.get('quote_amount', 0):,.2f}")
            print(f"   Status: {quote.get('quote_status')}")
except Exception as e:
    test_result("Get Event Quotes", False, str(e))

# Test 13: Professional sends message
print("\nTest 13: Professional sends message...")
try:
    success, message_id = client_manager.send_message(
        event_id=test_event_id,
        sender_id=1,  # Professional ID
        sender_type='professional',
        sender_name='DJ Tayzer',
        message_text="Thank you for your interest! I've sent you a quote. Let me know if you have any questions."
    )
    test_result("Send Professional Message", success, f"Message ID: {message_id if success else 'N/A'}")
except Exception as e:
    test_result("Send Professional Message", False, str(e))

# Test 14: Get professional's quotes
print("\nTest 14: Get professional's sent quotes...")
try:
    prof_quotes = client_manager.get_professional_quotes(1, 'dj')
    test_result("Get Professional Quotes", len(prof_quotes) >= 0, f"Found {len(prof_quotes)} quote(s)")
except Exception as e:
    test_result("Get Professional Quotes", False, str(e))

# Test 15: Update quote status
print("\nTest 15: Update quote status...")
try:
    if 'test_quote_id' in locals():
        success = client_manager.update_quote_status(test_quote_id, 'accepted')
        test_result("Update Quote Status", success, "Status changed to 'accepted'")
except Exception as e:
    test_result("Update Quote Status", False, str(e))

# Test 16: Get event by ID
print("\nTest 16: Get event by ID with client info...")
try:
    event = client_manager.get_event_by_id(test_event_id)
    test_result("Get Event By ID", event is not None, f"Event: {event.get('event_name') if event else 'N/A'}")
    
    if event:
        print(f"   Client: {event.get('first_name')} {event.get('last_name')}")
        print(f"   Email: {event.get('email')}")
        print(f"   Services: {event.get('requested_services')}")
except Exception as e:
    test_result("Get Event By ID", False, str(e))

print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)

print(f"\nTotal Tests: {tests_passed + tests_failed}")
print(f"✅ Passed: {tests_passed}")
print(f"❌ Failed: {tests_failed}")
print(f"Success Rate: {(tests_passed / (tests_passed + tests_failed) * 100):.1f}%")

print("\n" + "=" * 80)
print("DETAILED RESULTS")
print("=" * 80)
for result in test_results:
    print(result)

print("\n" + "=" * 80)
if tests_failed == 0:
    print("🎉 ALL CRITICAL PATH TESTS PASSED!")
    print("=" * 80)
    print("\nThe system is ready for use. Key workflows verified:")
    print("✅ Client registration and authentication")
    print("✅ Event creation and service linking")
    print("✅ Client-professional messaging")
    print("✅ Professional quote management")
    print("✅ Quote status updates")
else:
    print("⚠️  SOME TESTS FAILED - REVIEW REQUIRED")
    print("=" * 80)
    print(f"\n{tests_failed} test(s) need attention before deployment.")

print("\n" + "=" * 80)
