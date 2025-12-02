from sqlalchemy import create_engine, text

engine = create_engine('postgresql://tcn_ent:Provident3333!@tcn.c54mcgea4luc.us-east-2.rds.amazonaws.com:5432/postgres')
conn = engine.connect()

try:
    # Add phone column to photographers
    conn.execute(text('ALTER TABLE photographers ADD COLUMN IF NOT EXISTS phone VARCHAR(20)'))
    conn.commit()
    print("✅ Added phone to photographers")
    
    # Add phone column to event_coordinators
    conn.execute(text('ALTER TABLE event_coordinators ADD COLUMN IF NOT EXISTS phone VARCHAR(20)'))
    conn.commit()
    print("✅ Added phone to event_coordinators")
    
    # Add phone column to djs
    conn.execute(text('ALTER TABLE djs ADD COLUMN IF NOT EXISTS phone VARCHAR(20)'))
    conn.commit()
    print("✅ Added phone to djs")
    
    # Set default phone numbers
    conn.execute(text("UPDATE photographers SET phone = '(214) 555-0101' WHERE profile_id = 'photographer_1' AND (phone IS NULL OR phone = '')"))
    conn.execute(text("UPDATE event_coordinators SET phone = '(214) 555-0102' WHERE profile_id = 'coordinator_1' AND (phone IS NULL OR phone = '')"))
    conn.execute(text("UPDATE djs SET phone = '(214) 260-5003' WHERE profile_id = 'dj_1' AND (phone IS NULL OR phone = '')"))
    conn.execute(text("UPDATE djs SET phone = '(214) 555-0104' WHERE profile_id = 'dj_2' AND (phone IS NULL OR phone = '')"))
    conn.commit()
    print("✅ Set default phone numbers")
    
    print("\n✅ All done!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    conn.close()
