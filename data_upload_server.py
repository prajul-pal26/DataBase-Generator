import os
import pandas as pd
total_df = pd.DataFrame()
for path in os.listdir('extra_pdf'):
    df = pd.read_csv(os.path.join('extra_pdf', path))
    df = df.drop(columns=['Unnamed: 0'])
    total_df = pd.concat([total_df, df],ignore_index=True)


df = total_df  
df['State']='Uttar Pradesh'
df.to_csv('Extra_data.csv', index=False)