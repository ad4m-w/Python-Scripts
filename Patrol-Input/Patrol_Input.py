# By Adam Waszczyszak
from os import system
system("title " + "adamwasz.com")

import os
import sys
import tkinter
import random
import pandas as pd
from pathlib import Path
from splinter import Browser
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from tkinter import *
from tkinter import filedialog, ttk

def show_website_link():
    website_link = entry_url.get()
    print(f"Entered Website URL: {website_link}")

def select_csv_file():
    global csv_file_path
    csv_file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
    if csv_file_path:
        label_csv.config(text=f"Selected File: {csv_file_path}")
    else:
        label_csv.config(text="No file selected.")

def load_csv_file():
    global csv_file_path
    encoding = selected_encoding.get()  
    if csv_file_path:
        try:
            df = pd.read_csv(csv_file_path, encoding=encoding)
            print(f"CSV File Loaded: {csv_file_path} with encoding {encoding}")
            print(df.head()) 
        except Exception as e:
            print(f"Error loading CSV file: {e}")
    else:
        print("No CSV file selected.")

def continue_script():
    print("Script is continuing...")
    master.quit() 

def centerWindow(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - 500) // 2
    y = (screen_height - 500) // 2
    window.geometry(f"{500}x{500}+{x}+{y}")

master = Tk()
master.geometry("500x500")  
centerWindow(master)
master.title("adamwasz.com")

site_selection = StringVar(master)

# Formatted for easier visualization 
values = [
    ("Sec-2", "1"),
    ("Mi3", "2"),
    ("Mi-ES", "3"),
    ("MVW-2", "4"),
    ("demo4", "5"),
    ("Sec-6", "6"),
    ("HW", "7")
]

# GUI 
label_site = Label(master, text="Select Site Type:")
label_site.grid(row=0, column=0, pady=10, padx=20, sticky="w")

site_combobox = ttk.Combobox(master, values=[item[0] for item in values], textvariable=site_selection, state="readonly", width=20)
site_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")

button_csv = Button(master, text="Select CSV File", command=select_csv_file)
button_csv.grid(row=1, column=0, pady=10, padx=20, sticky="w")

label_csv = Label(master, text="No file selected.", anchor="w")
label_csv.grid(row=1, column=1, padx=10, sticky="w")

button_load_csv = Button(master, text="Load CSV File", command=load_csv_file)
button_load_csv.grid(row=2, column=0, pady=10, padx=20, sticky="w")

label_url = Label(master, text="Enter Website URL:")
label_url.grid(row=3, column=0, pady=10, padx=20, sticky="w")

entry_url = Entry(master, width=50) 
entry_url.grid(row=3, column=1, padx=10, pady=5, sticky="w")

button_url = Button(master, text="Submit Website URL", command=show_website_link, width=20)
button_url.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="nsew") 

label_encoding = Label(master, text="Select CSV Encoding:")
label_encoding.grid(row=5, column=0, pady=10, padx=20, sticky="w")

encoding_options = ["UTF-8", "ISO-8859-1", "Windows-1252", "ASCII"]
selected_encoding = StringVar(master)  
selected_encoding.set(encoding_options[0])  
encoding_combobox = ttk.Combobox(master, values=encoding_options, textvariable=selected_encoding, state="readonly", width=20)
encoding_combobox.grid(row=5, column=1, padx=10, pady=5, sticky="w")

label_username = Label(master, text="Username:")
label_username.grid(row=6, column=0, pady=10, padx=20, sticky="w")
entry_username = Entry(master, width=50) 
entry_username.grid(row=6, column=1, padx=10, pady=5, sticky="w")

label_password = Label(master, text="Password:")
label_password.grid(row=7, column=0, pady=10, padx=20, sticky="w")
entry_password = Entry(master, width=50, show="*") 
entry_password.grid(row=7, column=1, padx=10, pady=5, sticky="w")

button_submit = Button(master, text="Run Script", command=continue_script, width=15)
button_submit.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="nsew")

progressbar = ttk.Progressbar(master, orient="horizontal", length=400, mode="determinate", maximum=100)
progressbar.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="")

# Start of Main Loop
master.mainloop()

# Variables for script, done like this for compatibility 
website = entry_url.get()
sitetype = site_selection.get()
csvpath = csv_file_path
enc = selected_encoding.get()
uname = entry_username.get() 
pw = entry_password.get()

# Import CSV file
df = pd.read_csv(csv_file_path, encoding=enc)
pCount = len(df.index)  

if getattr(sys, 'frozen', False):
    bundle_dir = Path(sys._MEIPASS) 
else:
    bundle_dir = Path(os.path.abspath(os.path.dirname(__file__)))

chrome_binary = r'C:/Program Files/Google/Chrome/Application/chrome.exe'
chromedriver_path = bundle_dir / 'chromedriver.exe'

if not chromedriver_path.exists():
    print("Error: chromedriver.exe not found!")
    sys.exit()

options = Options()
options.binary_location = chrome_binary
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Headless Mode 
options.add_argument("--headless")  

service = Service(str(chromedriver_path))
browser = Browser('chrome', service=service, options=options)

try:
    url = website
    browser.visit(url)

    username = uname
    password = pw

    if((sitetype == 'Mi3') or (sitetype == 'Mi-ES')):
        browser.find_by_name('MsSSOBtn').click()
        browser.fill('pf.username', username)
        browser.fill('pf.pass', password)
        browser.find_by_id('SMBT').click()
    else:
        browser.fill('lgnBox', username)
        browser.fill('username', password)
        browser.find_by_name('Submit').click()

    print("\nLogged into " + sitetype + " successfully.")

    if(sitetype == 'Sec-2'):
        url = 'https://msshift-security-2.com/d/Admin/CategoryLP/AddPoint/PointTypeList_'
    elif(sitetype == 'Mi3'):
        url ='https://msshift-mi3.com/d/Admin/CategoryLP/AddPoint/PointTypeList_'
    elif(sitetype == 'Mi-ES'):
        url ='https://msshift-mi-es.com/d/Admin/CategoryLP/AddPoint/PointTypeList_'
    elif(sitetype == 'demo4'):
        url ='https://msshift-demo-4.com/d/Admin/CategoryLP/AddPoint/PointTypeList_'
    elif(sitetype == 'Sec-6'):
        url = 'https://msshift-security-6.com/d/Admin/CategoryLP/AddPoint/PointTypeList_'
    elif(sitetype == 'HW'):
        url = 'https://msshift-hw.com/d/Admin/CategoryLP/AddPoint/PointTypeList_'
    elif(sitetype == 'MVW-2'):
        url = 'https://msshift-mvw-2.com/d/Admin/CategoryLP/AddPoint/PointTypeList_'

    browser.visit(url)

    pStep = 0
    loopIteration = 0
    for index, row in df.iterrows():
        print("Looping CSV...")
        route = row['Route']
        point = row['Points']
        barcode = row['Barcode']
        print(f"Route: {route}, Point: {point}")

        # Random Number for password generation
        randomNumber = random.randint(10000000, 99999999)

        browser.visit(url)

        print("Searching for Patrol Route dropdown")
        dropdown = browser.find_by_id('PatrolName')
        print("Patrol Route dropdown found.")
        if dropdown:

            options = dropdown.find_by_tag('option')

            if options:
                for option in options:
                    if route in option.text:
                        option.click()
                        print(f"Selected: {option.text}")
                        sleep(1)  

                        point_list_dropdown = browser.find_by_id('PointList')
                        if point_list_dropdown:
                            point_options = point_list_dropdown.find_by_tag('option')
                            add_new_point_option = None
        
                        for point_option in point_options:
                            if 'Add New Point Type' in point_option.text:
                                add_new_point_option = point_option
                                break 
                                    
                        if add_new_point_option:
                            add_new_point_option.click()            

                            try:
                                point_field = WebDriverWait(browser.driver, 20).until(
                                    EC.visibility_of_element_located((By.NAME, "EditPointType"))
                                )
                                barcode_field = WebDriverWait(browser.driver, 10).until(
                                    EC.visibility_of_element_located((By.NAME, 'EditPointBarcode'))
                                )

                                if point_field:
                                    if pd.notna(point):
                                        ActionChains(browser.driver).move_to_element(point_field).click().send_keys(point).perform()
                                    else:
                                        break
                                    if pd.notna(barcode):
                                        ActionChains(browser.driver).move_to_element(barcode_field).click().send_keys(int(barcode)).perform()
                                    else:
                                        # Input a random number into the barcode number as a placeholder. 
                                        # If there is no number in the barcode field, we cannot edit it from the mobile app (for NFC and Beacon setup).
                                        ActionChains(browser.driver).move_to_element(barcode_field).click().send_keys(randomNumber).perform()


                            except Exception as e:
                                print(f"Error filling fields in iframe: {e}")
            
                            browser.driver.switch_to.default_content()
            
                            save_button = WebDriverWait(browser.driver, 10).until(
                                EC.element_to_be_clickable((By.NAME, 'NewPoint'))
                            )
                            save_button.click()
                            alert = browser.get_alert()

                            # Handle the alert
                            if alert:
                                print("Alert exception handled:", alert.text)
                                with open("Patrol Point Log.txt", "a") as f:
                                    print(f"Alert exception handled:", alert.text, file=f)
                                alert.accept()  
                            else:
                                with open("Patrol Point Log.txt", "a") as f:
                                    print(f"Saved new patrol point: {route} {point} {barcode}", file=f)
                            browser.visit(url)
                            sleep(1)
                            break
                        else:
                            print("Add new patrol point option not found.")
                                  
                            break
        loopIteration += 1
        pStep = ((loopIteration/ pCount) * 100)
        progressbar['value'] = pStep
        master.update_idletasks()
        browser.reload()

except Exception as e:
    print(f"Error during script execution: {e}")

finally:
    print("Process complete. Press Enter to close the browser...")
    input() 
    browser.quit()
