from global_settings import *

'''----------------------------------------- 🚨 ALL MESSAGES 🚨 ------------------------------------------------'''

# feel free to add in your own lists of messages you'd like to send

opening_inventory = [
    "has your inventory been affected by the car shortage?",
    "how is your inventory right now with the car shortage going on?",
    "is the inventory shortage affecting you guys as well?",
    "are you guys being affected by the inventory shortage as well?",
    "are you having issues with the inventory shortage as well?",
    "has the inventory shortage been affecting you also?",
    "has the inventory shortage affected you as well?",
    "have you been affected by the inventory shortage by any chance?",
    "have you guys been having inventory difficulties?",
    "have you guys been having issues with the inventory shortage?",
]
opening_inventory_tags = [
    "heard the car market is crazy rn",
    "heard a lot of stories about how crazy the car market is rn",
    "i've heard a lot of stories about how crazy the car market is rn",
    "heard that a lot of dealerships are having issues with sourcing inventory rn",
    "heard that a lot of dealerships are kinda scrambling to source inventory rn",
]
opening_test_drive = [
    "Do you guys do test drive appointments?",
    "do you guys do test drive appointments?",
    "do you guys do test drive appts?",
    "I was wondering if you're available for more bookings this week?",
    "are you available for more bookings this week?",
    "Do you guys have room for more bookings this week?",
]
opening_quick_question = [
    # multi-line messages always do better because they seem less spammy
    ["hi", "i have a quick question", "is this the best place to get an answer?"],
    ["hi i got a quick question", "should i ask it here or somewhere else?"],
    ["I have a quick question", "is this the best place to ask?"],
    ["i got a quick question", "is this the best place to contact you?"],
]

opening__google_reviews = [
    ["I have a quick question about your google reviews", "is this the best place to ask it?"],
    ["I got a quick question about your google reviews", "is this the best place to contact you?"],
    ["i have a quick question", "about your google reviews", "is this the best place to ask?"],
]

'''----------------------------------------- 🚨 MESSAGING SETTINGS 🚨 ------------------------------------------------'''

# Customize these to your liking before turning on

messages_to_send = opening_quick_question # change this to desired list
message_tags = opening_inventory_tags

send_limit = 5 # max number of messages to send
time_between_messages = [15, 20]  # lowest and highest number of minutes to wait between each message

# Constants -- do not change!
loading_delay = 10
msgs_sent = 0

'''----------------------------------------- 🚨 FUNCTIONS 🚨 ------------------------------------------------'''

def go_to_messenger(webd):

    webd.get(messenger_link)
    WebDriverWait(webd, 300).until(EC.presence_of_element_located((By.CLASS_NAME, '_9dls'))) # waits for 5 minutes or until messenger HTML is detected
    print('Logged in to Messenger.')

def send_message(focus, message):
    '''
    Sends message to whatever field you choose to focus on
    '''
    # Multi-Line Message
    if type(message) == list:
        for line in message:
            focus.send_keys(line, Keys.ENTER) # type message then hit enter
            time.sleep(loading_delay)

    # Single-Line Message
    else:
        focus.send_keys(message, Keys.ENTER) # type message then hit enter
        time.sleep(loading_delay)

'''----------------------------------------- 🚨 START OF PROGRAM 🚨 ------------------------------------------------'''

# Setup webdriver & DF
webd = webdriver.Chrome(chrome_driver_fp)
login_to_fb(webd, message_email, message_password)
go_to_messenger(webd)
df = pd.read_csv(f'{csv_file}').sort_values(by=['Qualified', 'Messaged Yet'])
start_index = df['Messaged Yet'].last_valid_index()

for index, row in df.loc[start_index:].iterrows(): # iterates through each line of df

    # Get prospect data from current row
    link = row['Messenger']
    qualified = row['Qualified']
    messaged_yet = row['Messaged Yet']
    name = row['Name']

    # Message them IF qualified, haven't messaged yet, and have a messenger link
    if qualified == 'y' and pd.isnull(messaged_yet) and pd.notnull(link):

        # Go to prospect's messenger, then wait for delay to avoid getting blocked
        webd.get(link)
        time.sleep(loading_delay)
        try: # this is to handle cases where prospect has the "get started" button (you have to skip them)
            message_field = webd.find_element_by_xpath('//div[@aria-label="Message"]') # focus message field
        except:
            print(f"Had issue sending message to '{name}'.")
            continue
        message_delay = random.randint(time_between_messages[0] * 60, time_between_messages[1] * 60)
        time.sleep(message_delay)

        # Send message to prospect
        message = random.choice(messages_to_send) # do not change anything here!
        send_message(message_field, message) # choose message to send in "messaging settings" section at the start!
        if type(tags) == list:
            send_message(message_field, random.choice(tags))
        # note: will move to next prospect after sending message, so if they reply then the message won't be "seen"

        # Update CSV + activity log
        msgs_sent += 1
        today = date.today().strftime("%m-%d-%Y")
        df.loc[index, 'Messaged Yet'] = today # Mark as messaged on df. have to use .loc, not .at for some reason
        df.sort_index().to_csv(f'{csv_file}', index = False) # updates original csv. index = false makes it save without adding an extra column of indexes at the start.
        line_prepender(activity_log_fp, f'Messaged {name} on {today}. Messages sent this session: {msgs_sent}') # Update activity Log
        print(f"Messaged {name}.\nYou've sent {msgs_sent} messages this session.")

        # Stop if you've hit the send limit
        if msgs_sent >= send_limit:
            break

    # If you haven't hit send limit, but you've ran out of qualified prospects to message. Time to do more leadsourcing!
    elif pd.isnull(qualified):
        break

webd.quit()
