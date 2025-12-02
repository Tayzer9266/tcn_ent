"""
Test script to verify PostgreSQL connection and table creation
"""
from sqlalchemy import create_engine, text
import sys

# Database credentials
db_config = {
    'user': 'tcn_ent',
    'password': 'Provident3333!',
    'host': 'tcn.c54mcgea4luc.us-east-2.rds.amazonaws.com',
    'port': '5432',
    'dbname': 'postgres'
}

print("=" * 60)
print("PostgreSQL Connection Test")
print("=" * 60)

try:
    # Create connection
    connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    print("\n1. Creating database connection...")
    engine = create_engine(connection_string)
    conn = engine.connect()
    print("✅ Connection successful!")
    
    # Test query
    print("\n2. Testing database query...")
    result = conn.execute(text("SELECT version()"))
    version = result.fetchone()[0]
    print(f"✅ PostgreSQL version: {version[:50]}...")
    
    # Check if tables exist
    print("\n3. Checking for profile tables...")
    tables = ['photographers', 'event_coordinators', 'djs']
    
    for table in tables:
        result = conn.execute(text(f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = '{table}'
            )
        """))
        exists = result.fetchone()[0]
        
        if exists:
            # Count records
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.fetchone()[0]
            print(f"✅ Table '{table}' exists with {count} records")
        else:
            print(f"❌ Table '{table}' does not exist")
    
    conn.close()
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("=" * 60)
    sys.exit(1)
