import os
import pdfplumber
import sqlite3

root_dir = 'Database'

# Connect to SQLite database (or create it)
conn = sqlite3.connect('database_summary.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS pdf_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    district TEXT,
    bench TEXT,
    type TEXT,
    month TEXT,
    filename TEXT,
    row_count INTEGER,
    pdf_path TEXT,
    pdf_blob BLOB
)
''')

def read_pdf_as_blob(path):
    with open(path, 'rb') as file:
        return file.read()

# Loop through files and store metadata + file
for district in os.listdir(root_dir):
    district_path = os.path.join(root_dir, district)
    if not os.path.isdir(district_path):
        continue

    for bench in os.listdir(district_path):
        bench_path = os.path.join(district_path, bench)
        if not os.path.isdir(bench_path):
            continue

        for dtype in ['addition', 'modification', 'deletion']:
            dtype_path = os.path.join(bench_path, dtype)
            if not os.path.isdir(dtype_path):
                continue

            for month in os.listdir(dtype_path):
                month_path = os.path.join(dtype_path, month)
                if not os.path.isdir(month_path):
                    continue

                for file in os.listdir(month_path):
                    if file.endswith('.pdf'):
                        file_path = os.path.join(month_path, file)
                        count = 0

                        try:
                            with pdfplumber.open(file_path) as pdf:
                                for page in pdf.pages:
                                    tables = page.extract_tables()
                                    for table in tables:
                                        for row in table:
                                            if row and row[0]:
                                                count += 1
                        except Exception as e:
                            print(f"Error reading {file_path}: {e}")
                            continue

                        # Read PDF file content as BLOB
                        pdf_blob = read_pdf_as_blob(file_path)

                        # Insert into DB
                        cursor.execute('''
                        INSERT INTO pdf_summary (district, bench, type, month, filename, row_count, pdf_path, pdf_blob)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (district, bench, dtype.capitalize(), month, file, count, file_path, pdf_blob))

# Commit and close
conn.commit()
conn.close()

print("Done. Data saved to 'database_summary.db'")
