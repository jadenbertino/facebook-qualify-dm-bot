from global_settings import *
import tkinter as tk
from tkinter import messagebox
import sys
from assets.car_brands import car_brands

def ask_if_qualified():
    '''
    Shows a pop-up that prompts user to choose if qualified or not.
    Returns 'y' or 'n', or ends session if user chooses to cancel.
    '''
    root = tk.Tk()
    user_input = messagebox.askyesnocancel(
        title = 'Are they qualified?',
        message = 'Would you work with them?',
        detail = 'Click cancel to stop the program.',
    )
    root.destroy()
    if user_input == None: # if they click cancel
        print(f"You found {new_prospects} new prospects this session.")
        sys.exit()

    return user_input

def check_if_franchise(facebook_name):
    '''
    Checks if a franchise name is in the facebook page name.
    Use it to skip any franchise pages.
    '''
    return any(brand in facebook_name for brand in car_brands)

def add_prospect(prospect_count):
    '''
    Returns prospect_count + 1, and updates activity log with new prospect.
    '''
    num_prospects = prospect_count + 1
    today = date.today().strftime("%m-%d-%Y")
    line_prepender(activity_log_fp, f'{today} - Found {num_prospects} new prospects')
    return num_prospects

def print_num_available_prospects(f):
    '''
    Prints number of prospects available to message: qualified & not messaged yet
    '''
    count = 0
    for index, row in f.iterrows():
        if row['Qualified'] == 'y' and pd.isnull(row['Messaged Yet']):
            count += 1
        elif pd.isnull(row['Qualified']) and pd.isnull(row['Messaged Yet']):
            break
    print(f'You currently have {count} prospects available to message')

# ---------------------------------- START ------------------------------------- #

df = pd.read_csv(f'{csv_file}').sort_values(by=['Qualified'])
start_index = df['Qualified'].last_valid_index()
print_num_available_prospects(df)
driver = webdriver.Chrome(chrome_driver_fp)
login_to_fb(driver, qualify_email, qualify_password)
new_prospects = 0
skip_first_prospect = True

try:
    for index, row in df.loc[start_index:].iterrows():

        link = row['Facebook']
        name = row['Name']

        # Automated Checks
        if skip_first_prospect: # skip the first person because that the the last prospect I qualified
            skip_first_prospect = False # no idea how to implement this into the for loop above so i just put it here
            continue
        if check_if_franchise(name) or pd.isnull(link): # skip if franchise or no link
            df.loc[index, 'Qualified'] = 'n'
            continue
        else:
            driver.get(link)

        # Manual checks -> Update CSV
        print_num_available_prospects(df)
        if ask_if_qualified():
            df.loc[index, 'Qualified'] = 'y'
            new_prospects = add_prospect(new_prospects)
        else:
            df.loc[index, 'Qualified'] = 'n'
        df.sort_index().to_csv(f'{csv_file}', index = False) # updates original csv
except:
    print(f'You found {new_prospects} prospects this session.')
