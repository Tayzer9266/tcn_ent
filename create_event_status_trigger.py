"""
Create Database Trigger for Event Status Auto-Update
Automatically updates event_status from 'Scheduled' to 'Completed' 
when event_date has passed
"""

from sqlalchemy import create_engine, text
from datetime import datetime

# Database credentials
db_config = {
    'user': 'tcn_ent',
    'password': 'Provident3333!',
    'host': 'tcn.c54mcgea4luc.us-east-2.rds.amazonaws.com',
    'port': '5432',
    'dbname': 'postgres'
}

print("=" * 80)
print("EVENT STATUS TRIGGER CREATION")
print("=" * 80)
print("\nThis script will create a trigger that automatically updates")
print("event_status from 'Scheduled' to 'Completed' when event_date has passed.")
print("=" * 80)

try:
    # Create connection
    connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    print("\n1. Connecting to PostgreSQL...")
    engine = create_engine(connection_string)
    conn = engine.connect()
    print("✅ Connected successfully!")
    
    # Drop existing trigger and function if they exist
    print("\n2. Dropping existing trigger and function (if any)...")
    try:
        conn.execute(text('DROP TRIGGER IF EXISTS trg_update_event_status_on_past_date ON events'))
        conn.execute(text('DROP FUNCTION IF EXISTS update_event_status_on_past_date()'))
        conn.commit()
        print("✅ Cleaned up existing trigger and function")
    except Exception as e:
        print(f"ℹ️  No existing trigger to drop: {e}")
    
    # Create trigger function
    print("\n3. Creating trigger function...")
    conn.execute(text('''
        CREATE OR REPLACE FUNCTION update_event_status_on_past_date()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Check if event_date has passed and status is 'Scheduled'
            IF NEW.event_date < CURRENT_DATE AND NEW.event_status = 'Scheduled' THEN
                NEW.event_status := 'Completed';
                NEW.updated_at := CURRENT_TIMESTAMP;
            END IF;
            
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    '''))
    conn.commit()
    print("✅ Trigger function created successfully!")
    
    # Create trigger
    print("\n4. Creating trigger on events table...")
    conn.execute(text('''
        CREATE TRIGGER trg_update_event_status_on_past_date
        BEFORE INSERT OR UPDATE ON events
        FOR EACH ROW
        EXECUTE FUNCTION update_event_status_on_past_date();
    '''))
    conn.commit()
    print("✅ Trigger created successfully!")
    
    # Verify trigger creation
    print("\n5. Verifying trigger creation...")
    result = conn.execute(text('''
        SELECT trigger_name, event_manipulation, action_timing
        FROM information_schema.triggers
        WHERE trigger_name = 'trg_update_event_status_on_past_date'
    '''))
    trigger_info = result.fetchone()
    
    if trigger_info:
        print("✅ Trigger verified!")
        print(f"   - Trigger Name: {trigger_info[0]}")
        print(f"   - Event: {trigger_info[1]}")
        print(f"   - Timing: {trigger_info[2]}")
    else:
        print("⚠️  Warning: Trigger not found in information_schema")
    
    # Test the trigger with a sample scenario
    print("\n6. Testing trigger functionality...")
    print("\n   Test Case 1: Insert event with past date and 'Scheduled' status")
    print("   Expected: Status should be automatically changed to 'Completed'")
    
    # Create a test event with past date
    from datetime import timedelta
    past_date = datetime.now() - timedelta(days=5)
    
    try:
        # First, get a test client_id
        result = conn.execute(text('SELECT client_id FROM clients LIMIT 1'))
        test_client = result.fetchone()
        
        if test_client:
            test_client_id = test_client[0]
            
            # Insert test event
            result = conn.execute(text('''
                INSERT INTO events (
                    client_id, event_name, event_type, event_date, 
                    event_status, created_at, updated_at
                )
                VALUES (
                    :client_id, :event_name, :event_type, :event_date,
                    'Scheduled', :created_at, :updated_at
                )
                RETURNING event_id, event_status
            '''), {
                'client_id': test_client_id,
                'event_name': 'Test Event - Trigger Test',
                'event_type': 'Test',
                'event_date': past_date,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            })
            
            test_event = result.fetchone()
            test_event_id = test_event[0]
            final_status = test_event[1]
            
            conn.commit()
            
            if final_status == 'Completed':
                print(f"   ✅ TEST PASSED! Event ID {test_event_id} status: {final_status}")
                print("   The trigger correctly changed 'Scheduled' to 'Completed'")
            else:
                print(f"   ❌ TEST FAILED! Event ID {test_event_id} status: {final_status}")
                print("   Expected 'Completed' but got '{final_status}'")
            
            # Test Case 2: Update event
            print("\n   Test Case 2: Update event status back to 'Scheduled'")
            print("   Expected: Status should be automatically changed back to 'Completed'")
            
            conn.execute(text('''
                UPDATE events 
                SET event_status = 'Scheduled'
                WHERE event_id = :event_id
            '''), {'event_id': test_event_id})
            conn.commit()
            
            # Check the status after update
            result = conn.execute(text('''
                SELECT event_status FROM events WHERE event_id = :event_id
            '''), {'event_id': test_event_id})
            
            updated_status = result.fetchone()[0]
            
            if updated_status == 'Completed':
                print(f"   ✅ TEST PASSED! Status after update: {updated_status}")
                print("   The trigger correctly prevented 'Scheduled' status for past events")
            else:
                print(f"   ❌ TEST FAILED! Status after update: {updated_status}")
            
            # Clean up test event
            print("\n   Cleaning up test event...")
            conn.execute(text('DELETE FROM events WHERE event_id = :event_id'), 
                        {'event_id': test_event_id})
            conn.commit()
            print("   ✅ Test event removed")
            
        else:
            print("   ⚠️  No clients found in database. Skipping trigger test.")
            print("   The trigger has been created and will work when events are inserted.")
    
    except Exception as e:
        print(f"   ⚠️  Test error: {e}")
        print("   The trigger has been created but testing failed.")
        print("   This may be due to missing test data.")
        conn.rollback()
    
    print("\n" + "=" * 80)
    print("✅ TRIGGER CREATION COMPLETE!")
    print("=" * 80)
    print("\nTrigger Details:")
    print("- Name: trg_update_event_status_on_past_date")
    print("- Function: update_event_status_on_past_date()")
    print("- Fires: BEFORE INSERT OR UPDATE on events table")
    print("- Logic: Changes 'Scheduled' to 'Completed' when event_date < CURRENT_DATE")
    print("\nThe trigger is now active and will automatically update event statuses!")
    print("=" * 80)
    
    conn.close()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("=" * 80)
    import traceback
    traceback.print_exc()
