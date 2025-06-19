import pandas as pd
import os

df = pd.read_csv('COMBINED_DATA.csv')
print(df)
# folder_path = 'data/'

# # Get list of all CSV files in the folder
# csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
# print(len(csv_files))
# # Empty list to hold all transformed DataFrames
# all_dfs = []
# for file in csv_files:
#     file_path = os.path.join(folder_path, file)
#     df = pd.read_csv(file_path)
#     if df.empty is True:
#         print(df)
#     # Melt the data to long format
#     df_long = pd.melt(
#         df,
#         id_vars=["id", "establishment", "type"],
#         value_vars=["MARCH-2025", "APRIL-2025", "MAY-2025"],
#         var_name="month",
#         value_name="value"
#     )

#     # Drop id column (optional)
#     df_long = df_long[["establishment", "type", "month", "value"]]
#     # Append to list
#     all_dfs.append(df_long)

# final_df = pd.concat(all_dfs, ignore_index=True)
# final_df.to_csv('combined_output.csv', index=True)
# print(len(all_dfs))
