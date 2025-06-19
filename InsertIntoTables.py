import os
import pdfplumber
import psycopg2
from psycopg2 import sql

root_dir = 'Database'

# Helper: count rows in a PDF
def count_rows_in_pdf(path):
    count = 0
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if row[0] != 'State' and len(row) == 6:
                            count += 1
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return 0  # Return 0 instead of -1 to avoid affecting totals
    return count

# Function to extract and convert PDF table data
def convert_to_csv(path):
    return count_rows_in_pdf(path)  # Unified logic with count_rows_in_pdf

def table_exists(cursor, table_name):
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = %s
        )
    """, (table_name,))
    return cursor.fetchone()[0]

def insert_count(month_columns, table=None):
    

    # Loop through districts
    for district in os.listdir(root_dir)[1:2]: 
        conn = psycopg2.connect(
            dbname="Generator",
            user="postgres",
            password="1234",
            host="localhost", 
            port="5432"          
        )

        cursor = conn.cursor() 
        district_path = os.path.join(root_dir, district)
        if not os.path.isdir(district_path):
            continue
        
        table_name = district.lower().replace(" ", "_")  
        if table:
            table_name += f'_{table.lower()}'
        
        if not table_exists(cursor, table_name):
            create_table_query = sql.SQL("""
                CREATE TABLE {} (
                    establishment TEXT,
                    type TEXT,
                    {}
                )
            """).format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(sql.Identifier(month) + sql.SQL(" INTEGER DEFAULT 0") for month in month_columns)
            )
            cursor.execute(create_table_query)
        
        establishments = [e for e in os.listdir(district_path) if os.path.isdir(os.path.join(district_path, e))]

        # Fill the table
        for est in establishments:
            for dtype in ['addition', 'modification', 'deletion']:
                dtype_path = os.path.join(district_path, est, dtype)
                if not os.path.isdir(dtype_path):
                    continue

                month_counts = {month: 0 for month in month_columns}

                for month in os.listdir(dtype_path):
                    month_path = os.path.join(dtype_path, month)
                    if not os.path.isdir(month_path):
                        continue

                    count = 0  # Initialize properly
                    for file in os.listdir(month_path):
                        if file.endswith('.pdf'):
                            file_path = os.path.join(month_path, file)
                            count += convert_to_csv(file_path)

                    if month in month_counts:
                        month_counts[month] += count

                # Insert the row
                insert_query = sql.SQL("""
                    INSERT INTO {} (establishment, type, {})
                    VALUES (%s, %s, {})
                """).format(
                    sql.Identifier(table_name),
                    sql.SQL(', ').join(map(sql.Identifier, month_columns)),
                    sql.SQL(', ').join(sql.Placeholder() * len(month_columns))
                )
                values = [est, dtype.capitalize()] + [month_counts[month] for month in month_columns]
                cursor.execute(insert_query, values)

        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")
        print(f"Processed: {district}")

        conn.commit()
        cursor.close()  # Explicitly close cursor
        conn.close()
        print("Done. Tables created and data inserted.")

insert_count(month_columns=['MARCH-2025', 'APRIL-2025', 'MAY-2025'])