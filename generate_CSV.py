import psycopg2
import sqlite3
import pandas as pd
import os

# Step 1: Connect to PostgreSQL
pg_conn = psycopg2.connect(
    dbname="Generator",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
pg_cursor = pg_conn.cursor()

# Step 2: Connect to SQLite
sqlite_conn = sqlite3.connect('data.db')

# Step 3: Fetch all table names from PostgreSQL
pg_cursor.execute("""
    SELECT tablename FROM pg_tables
    WHERE schemaname = 'public';
""")
tables = pg_cursor.fetchall()

# Step 4: Migrate data from PostgreSQL to SQLite
for table in tables:
    table_name = table[0]
    print(f"🔄 Migrating table: {table_name}")
    
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", pg_conn)
    df.to_sql(table_name, sqlite_conn, if_exists='replace', index=False)

# Close PostgreSQL connection
pg_cursor.close()
pg_conn.close()
sqlite_conn.commit()

# Step 5: Create output folder 'data' if it doesn't exist
output_folder = 'data'
os.makedirs(output_folder, exist_ok=True)

# Step 6: Export each table from SQLite to CSV in 'data/' folder
cursor = sqlite_conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
sqlite_tables = cursor.fetchall()

for table in sqlite_tables:
    table_name = table[0]
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", sqlite_conn)
    csv_file_path = os.path.join(output_folder, f"{table_name}.csv")
    df.to_csv(csv_file_path, index=False)
    print(f"✅ Exported {table_name} → {csv_file_path}")

# Close SQLite connection
sqlite_conn.close()

print("\n🎉 All PostgreSQL tables migrated to data.db and exported as CSVs in the 'data/' folder.")
