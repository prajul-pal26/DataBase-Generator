import pdfplumber
import pandas as pd
filtered_rows = []
count = 0

with pdfplumber.open("CEO_UP/sample.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                if row and row[0] and str(row[0]).startswith("Uttar Pradesh"):
                    filtered_rows.append(row)
                    count += 1

df = pd.DataFrame(columns=[ 'State' ,'District', 'AC No', 'Part No' ,'EPIC', 'Name'],data = filtered_rows)
print(df)
print("Total matching rows:", count)
