import psycopg2
import sqlite3
import pandas as pd

# Connect to PostgreSQL
pg_conn = psycopg2.connect(
    dbname="Generator",
    user="postgres",
    password="1234",
    host="localhost", 
    port="5432"         
)
pg_cursor = pg_conn.cursor()

# Connect to SQLite
sqlite_conn = sqlite3.connect('data.db')

# Fetch all table names from PostgreSQL
pg_cursor.execute("""
    SELECT tablename FROM pg_tables
    WHERE schemaname = 'public';
""")
tables = pg_cursor.fetchall()

# Loop through each table and copy data
for table in tables:
    table_name = table[0]
    print(f"Migrating table: {table_name}")
    
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", pg_conn)
    df.to_sql(table_name, sqlite_conn, if_exists='replace', index=False)

# Close connections
pg_cursor.close()
pg_conn.close()
sqlite_conn.close()

print("✅ PostgreSQL data successfully migrated to data.db")
