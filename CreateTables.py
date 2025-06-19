import os
import psycopg2
from psycopg2 import sql

root_dir = 'Database'
conn = psycopg2.connect(
    dbname="Generator",
    user="postgres",
    password="1234",
    host="localhost", 
    port="5432"         
)
def creatTable(month_columns, table=None, create=None, delete = None, skip=None):
    cursor = conn.cursor()

    # Get existing tables
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    existing_tables = set(row[0] for row in cursor.fetchall())

    # Loop through districts
    for district in os.listdir(root_dir):
        district_path = os.path.join(root_dir, district)
        if not os.path.isdir(district_path):
            continue
        table_name = district.lower().replace(" ", "_") 
        if table:
            table_name=table_name+'_'+table.lower()

        if table_name in existing_tables:
            if skip:
                'skip the table'
                print(f"Skipping existing table: {table_name}")
                continue
            if delete:
                'delete the table'
                drop_query = sql.SQL("DROP TABLE IF EXISTS {} CASCADE;").format(sql.Identifier(table_name))
                cursor.execute(drop_query)
                print(f"Dropped table if existed: {table_name}")
        
        if create:
            'Create SQL for table month wise and create a columns '
            column_defs = [
                sql.SQL("id SERIAL PRIMARY KEY"), 
                sql.SQL("establishment TEXT"),
                sql.SQL("type TEXT")
            ] + [sql.SQL("{} INTEGER").format(sql.Identifier(month)) for month in month_columns]

            create_query = sql.SQL("CREATE TABLE {} ({});").format(
                sql.Identifier(table_name),
                sql.SQL(", ").join(column_defs)
            )

            cursor.execute(create_query)
            print(f"Created table: {table_name}")
        
        elif delete is None:
            'add the next month in the table'
            alter_query = sql.SQL("ALTER TABLE {} ADD COLUMN {} INTEGER;").format(
            sql.Identifier(table_name), 
            sql.Identifier(month_columns) 
                )

            cursor.execute(alter_query)
            conn.commit()



    # Finalize
    conn.commit()
    conn.close()
    print("Done. Tables created and data inserted.")

"""
month_columns     ex. ['MARCH-2025','APRIL-2025','MAY-2025' ]    ex. 'MAY-2025'  for single addition 
table             table='DATA'    table='None'
create            True   for creating table
delete          delete = True    delete the table
skip            skip=True   skop the tables for modificaation
"""

# creatTable(month_columns=['MARCH-2025'],table='DATA', create=True)

creatTable(month_columns=['MARCH-2025','APRIL-2025','MAY-2025' ],create=True,skip=True)