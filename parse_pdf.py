import os
import pdfplumber
import psycopg2
from psycopg2 import sql
import pandas as pd

root_dir = 'Database'

# Helper: count rows in a PDF
def count_rows_in_pdf(path):
    count = 0
    row_data = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if row[0] != 'State' and len(row) == 6:
                            
                            row_data.append(row)
                            count += 1
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return 0  # Return 0 instead of -1 to avoid affecting totals
    df= pd.DataFrame(row_data,columns=['State','District','AC No.','Part No','EPIC','Name'])
    df['count'] = count
    return df,count

# Function to extract and convert PDF table data
def convert_to_csv(path):
    return count_rows_in_pdf(path)  # Unified logic with count_rows_in_pdf


def insert_count(districts,ests,month_columns,dtype):
    
    total_df = pd.DataFrame(columns=['State','District','AC No.','Part No','EPIC','Name'])
    # Loop through districts
    # for district in os.listdir(root_dir):
    for district in districts: 
        district_path = os.path.join(root_dir, district)
        # establishments = [e for e in os.listdir(district_path) if os.path.isdir(os.path.join(district_path, e))]

        # Fill the table
        for est in ests:
            for dtype in dtype:
                dtype_path = os.path.join(district_path, est, dtype)


                for month in month_columns:
                    month_path = os.path.join(dtype_path, month)
                    if not os.path.isdir(month_path):
                        continue

                    for file in os.listdir(month_path):
                        if file.endswith('.pdf'):
                            file_path = os.path.join(month_path, file)
                            mapping = {
                                'addition':'Addition',
                                'deletion':'Deletion',
                                'modification':'Modification',
                                'MARCH-2025':'March', 
                                'APRIL-2025':'April', 
                                'MAY-2025':'May'
                            }
                            df, count= convert_to_csv(file_path)
                            df['establishment']=est
                            df['type']=mapping[dtype]
                            
                            df['month']=mapping[month]
                            
                            df.to_csv(f"extra_pdf\{est}-{mapping[dtype]}-{mapping[month]}-{count}.csv")
                            
                            # total_df = pd.concat([total_df, df])
    # total_df.to_csv("All_Names.csv")



    
# ['MARCH-2025', 'APRIL-2025', 'MAY-2025']
# district = ['Agra']
# ['addition', 'deletion','modification']


  
insert_count(districts =['Bulandsahar'],ests= ['Sikandrabad'],month_columns=['MARCH-2025', 'APRIL-2025', 'MAY-2025'],dtype = ['addition', 'deletion','modification'])  # Example call