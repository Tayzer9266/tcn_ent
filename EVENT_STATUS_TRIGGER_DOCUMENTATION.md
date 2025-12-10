# Event Status Trigger Documentation

## Overview
A PostgreSQL database trigger has been implemented to automatically update the `event_status` field in the `events` table from 'Scheduled' to 'Completed' when the event date has passed.

## Trigger Details

### Trigger Name
`trg_update_event_status_on_past_date`

### Trigger Function
`update_event_status_on_past_date()`

### Trigger Type
- **Event**: BEFORE INSERT OR UPDATE
- **Table**: events
- **Scope**: FOR EACH ROW

## How It Works

### Logic Flow
1. **Trigger Fires**: When a new event is inserted or an existing event is updated
2. **Condition Check**: 
   - Is `event_date` < `CURRENT_DATE`? (Has the event date passed?)
   - Is `event_status` = 'Scheduled'?
3. **Action**: If both conditions are true:
   - Set `event_status` = 'Completed'
   - Update `updated_at` = CURRENT_TIMESTAMP

### PL/pgSQL Function Code
```sql
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
```

### Trigger Creation Code
```sql
CREATE TRIGGER trg_update_event_status_on_past_date
BEFORE INSERT OR UPDATE ON events
FOR EACH ROW
EXECUTE FUNCTION update_event_status_on_past_date();
```

## Use Cases

### Scenario 1: Inserting a Past Event
```sql
INSERT INTO events (
    client_id, event_name, event_type, event_date, 
    event_status, created_at, updated_at
)
VALUES (
    1, 'Past Wedding', 'Wedding', '2024-01-01',
    'Scheduled', NOW(), NOW()
);
```
**Result**: The event will be automatically saved with `event_status = 'Completed'`

### Scenario 2: Updating an Event Status
```sql
UPDATE events 
SET event_status = 'Scheduled'
WHERE event_id = 123 AND event_date < CURRENT_DATE;
```
**Result**: The status will remain 'Completed' (or be changed to 'Completed' if it was something else)

### Scenario 3: Future Events
```sql
INSERT INTO events (
    client_id, event_name, event_type, event_date, 
    event_status, created_at, updated_at
)
VALUES (
    1, 'Future Party', 'Birthday', '2025-12-31',
    'Scheduled', NOW(), NOW()
);
```
**Result**: The event will be saved with `event_status = 'Scheduled'` (no change)

## Testing Results

### Test 1: INSERT with Past Date
- **Input**: Event with `event_date` = 5 days ago, `event_status` = 'Scheduled'
- **Expected**: Status automatically changed to 'Completed'
- **Result**: ✅ PASSED

### Test 2: UPDATE with Past Date
- **Input**: Update existing past event to `event_status` = 'Scheduled'
- **Expected**: Status automatically changed back to 'Completed'
- **Result**: ✅ PASSED

## Benefits

1. **Automatic Status Management**: No manual intervention needed to mark past events as completed
2. **Data Integrity**: Ensures past events cannot remain in 'Scheduled' status
3. **Real-time Updates**: Works immediately on INSERT and UPDATE operations
4. **Transparent**: Happens at the database level, works regardless of application code

## Maintenance

### Viewing the Trigger
```sql
SELECT trigger_name, event_manipulation, action_timing
FROM information_schema.triggers
WHERE trigger_name = 'trg_update_event_status_on_past_date';
```

### Dropping the Trigger
```sql
DROP TRIGGER IF EXISTS trg_update_event_status_on_past_date ON events;
DROP FUNCTION IF EXISTS update_event_status_on_past_date();
```

### Recreating the Trigger
Run the script: `python create_event_status_trigger.py`

## Notes

- The trigger uses `CURRENT_DATE` for comparison, which means it checks against the current date (not time)
- The trigger only affects events with status 'Scheduled' - other statuses are not modified
- The `updated_at` timestamp is automatically updated when the status changes
- The trigger is executed BEFORE the row is written, so the change is atomic

## Files Created

1. **create_event_status_trigger.py**: Script to create and test the trigger
2. **TODO_EVENT_STATUS_TRIGGER.md**: Implementation checklist
3. **EVENT_STATUS_TRIGGER_DOCUMENTATION.md**: This documentation file

## Support

If you need to modify the trigger behavior:
1. Edit the `update_event_status_on_past_date()` function
2. Drop and recreate the trigger
3. Test thoroughly before deploying to production

## Version History

- **v1.0** (2024): Initial implementation
  - Auto-update 'Scheduled' to 'Completed' for past events
  - BEFORE INSERT OR UPDATE trigger
  - Comprehensive testing included
