import os
import pdfplumber
import pandas as pd

root_dir = 'Database'

data = []

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

                        data.append({
                            'District': district,
                            'Bench': bench,
                            'Type': dtype.capitalize(),
                            'Month': month,
                            'FileName': file,
                            'RowCount': count
                        })

df = pd.DataFrame(data)

df.to_csv('Database_summary.csv', index=False)

print("Done. Summary saved to 'Database_summary.csv'")
