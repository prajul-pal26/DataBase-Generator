from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os
import pandas as pd

base_download_dir = os.getcwd()

chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.prompt_for_download": False,  
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--headless=new")  
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://ceouttarpradesh.nic.in/acwiserollpdf.aspx")

time.sleep(1)
columns = []
rows = []

district_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_DDLDistrict"))
district_options = district_dropdown.options[1:] 
district_data = [(district.text.strip(), district.get_attribute('value')) for district in district_options]
driver.quit()

for district in district_data:
    district_name = district[0]
    district_value = district[1]

    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://ceouttarpradesh.nic.in/acwiserollpdf.aspx")
    time.sleep(3)

    district_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_DDLDistrict"))
    district_dropdown.select_by_value(district_value)
    time.sleep(2)

    ac_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_DDL_AC"))
    ac_options = ac_dropdown.options[1:]  
    ac_data = [(city.text.strip(), city.get_attribute('value')) for city in ac_options]
    driver.quit()
    print(district)
    print(ac_data)
    if district not in columns:
        columns.append(district)
        rows.append(ac_data)
driver.quit()
df = pd.DataFrame()

for col_tuple, row_list in zip(columns, rows):
    col_name = f"{col_tuple[0]} {col_tuple[1]}"
    values = [f"{name} {code}" for name, code in row_list]

    if len(values) > len(df):
        df = df.reindex(range(len(values)))

    df[col_name] = pd.Series(values)

print(df)
df.to_csv("CEO_UP/data.csv", index=False)

print(df)
