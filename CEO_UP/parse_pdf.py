# fetching pdf from the website from the use of data.csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os
import pandas as pd
months = ['MAY-2025','APRIL-2025','MARCH-2025']
data_types =[['addition','ctl00_ContentPlaceHolder1_rbAddition'],[ 'modification','ctl00_ContentPlaceHolder1_rbModification'],['deletion','ctl00_ContentPlaceHolder1_rbDeletion']]
base_download_dir = os.path.dirname(os.path.abspath(__file__))
base_download_dir = os.path.join(base_download_dir, 'DATABASE')

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


df = pd.read_csv('CEO_UP/data.csv')

# for city in range(1,10):
city = 58
data = df.iloc[:,city]

district = data.name.rsplit(' ',1)
district_name = district[0].strip()
district_value = district[1].strip()

ac_options  = [i.rsplit(' ',1) for i in data.to_list() if pd.notna(i)]
for ac_option in ac_options[2:]:
    ac_name = ac_option[0].strip()
    ac_value = ac_option[1].strip()
    for data_type in data_types:
        data_type_name = data_type[0]
        data_type_value = data_type[1]
        
        for month in months:
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://ceouttarpradesh.nic.in/acwiserollpdf.aspx")
            time.sleep(3)
            
            district_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_DDLDistrict"))
            district_dropdown.select_by_value(district_value)
            time.sleep(2)

            ac_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_DDL_AC"))
            ac_dropdown.select_by_value(ac_value)
            time.sleep(2)

            month_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_DDlmonth"))
            month_dropdown.select_by_value(month)  

            radio_addition = driver.find_element(By.ID, data_type_value)
            radio_addition.click()
            
            district_folder = os.path.join(base_download_dir, district_name)
            ac_folder = os.path.join(district_folder, ac_name)
            data_type_name = os.path.join(ac_folder, data_type_name)
            
            month_folder = os.path.join(data_type_name, month)
            os.makedirs(month_folder, exist_ok=True)

            prefs["download.default_directory"] = month_folder
            chrome_options.add_experimental_option("prefs", prefs)
            driver.execute_cdp_cmd("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": month_folder})

            time.sleep(1) 
            download_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btndownload")
            download_button.click()

            time.sleep(5)  

            print(f"Downloaded for {district_name} - {ac_name} in {ac_folder}")
            driver.quit()
