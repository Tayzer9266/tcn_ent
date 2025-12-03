from sqlalchemy import create_engine, text, inspect

# Connect to database
connection_string = "postgresql://tcn_ent:Provident3333!@tcn.c54mcgea4luc.us-east-2.rds.amazonaws.com:5432/postgres"
engine = create_engine(connection_string)
inspector = inspect(engine)

# Get all tables
tables = inspector.get_table_names()
print("=" * 70)
print("EXISTING TABLES IN DATABASE")
print("=" * 70)
print(f"All tables: {tables}\n")

# Check specific tables
target_tables = ['clients', 'events', 'event_services', 'services']

for table in target_tables:
    if table in tables:
        print(f"\n{'=' * 70}")
        print(f"TABLE: {table}")
        print("=" * 70)
        columns = inspector.get_columns(table)
        for col in columns:
            print(f"  - {col['name']}: {col['type']} {'(nullable)' if col['nullable'] else '(NOT NULL)'}")
    else:
        print(f"\n⚠️  Table '{table}' does NOT exist")

print("\n" + "=" * 70)
