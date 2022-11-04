'''
Current chromedriver version: 98
Chromedriver download page: https://chromedriver.chromium.org/downloads
'''

'''----------------------------------------- 🚨 PACKAGES 🚨 ------------------------------------------------'''
from datetime import date, datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import random
from pyotp import *

'''----------------------------------------- 🚨 LOG-IN SETTINGS 🚨 ------------------------------------------------'''
# from secret.logins import message_email, message_password, qualify_email, qualify_password

# write your own logins here! 👇👇👇

# qualify_email =
# qualify_password =
# message_email =
# message_password =
# messenger_link = 

'''----------------------------------------- 🚨 Filepaths of CSV, Activity Log, Chrome Webdriver, Backup CSV 🚨 ------------------------------------------------'''

'''
- Column names must be: Qualified, Messaged Yet, Messenger
- Qualifed must be marked with "y"
- If haven't messaged yet, leave cell empty (i.e. don't mark n)
'''
csv_file = 'assets\leads.csv'
activity_log_fp = 'assets\Activity Log.txt'
chrome_driver_fp = 'assets\chromedriver.exe'

current_dt = datetime.now().strftime("%m-%d-%Y %H-%M-%S")
backup_df = pd.read_csv(csv_file)
backup_csv_location = f'assets\Backups\{current_dt}.csv'
backup_df.to_csv(f'{backup_csv_location}', index = False)

'''----------------------------------------- 🚨 UNIVERSAL FUNCTIONS 🚨 ------------------------------------------------'''
def login_to_fb(webd, email, password):
    '''
    Takes a given webdriver -> goes to facebook.com & signs in
    '''
    print("Remember: Always click *Don't Save* when logging into FB.\nevery webdriver opens a new instance, so there's no point in saving.")
    webd.get('https://www.facebook.com/')
    email_field = webd.find_element_by_id('email')
    email_field.send_keys(email, Keys.TAB, password, Keys.ENTER) # imported from secret.py
    WebDriverWait(webd, 300).until(EC.presence_of_element_located(
        (By.XPATH, '//span[@class="a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7"]')))

def line_prepender(filename, line): # Writes to beginning of activity log
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)
