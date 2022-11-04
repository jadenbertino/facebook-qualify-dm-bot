# Overview 🦅
**This program helps to rapidly achieve two goals:**
1. Qualify businesses (i.e. used car dealerships) that may be in need of marketing services *
2. Message said businesses to offer them marketing services

The qualification process is semi-automated. The message process is fully automated.

Note that these programs are modular! You do not need to use them together. If you are only interested in one of the programs, then just use that :)

# Setup 🔧

First of all, go to `global_settings.py` and find the section labeled `LOG-IN SETTINGS`.

Set the following values:
- `qualify_email` - email you'll use to login to facebook
- `qualify_password` - password you'll use to login to facebook
- `message_email` - email you'll use to login to facebook messenger
- `message_password` - password for messenger login
- `messenger_link` - set your unique messenger link.
    - Go to your facebook profile (ex: `https://www.facebook.com/jadenbertino`)
    - Take note of text after the `.com/` -- in the above example `jadenbertino`
    - Add that to `https://m.me/` -- ex my link is `https://m.me/jadenbertino`

*Note: I separated facebook & messenger logins because I personally used a separate account without 2FA for qualification. Feel free to set both logins to the same username / password.*

Next, navigate to the `assets` folder and create a file called `leads.csv` file containing the following:
- `Name` column with the name of the business
- `Facebook` column containing links to the businesess' facebook page
- `Messenger` column containing links to the businesses' messenger

**Use a lead scraper tool such as D7, leadkahuna, leadscrape, etc in order to rapidly generate giant lists of leads**

Additionally, you'll also add two more columns. Put the following headers on each column, but leave the rest of the column empty to start.
- `Qualified` - Will use it to track whether a prospect is qualified or not
- `Messaged Yet` - Will use to keep track of businesses that have already been contacted

**Confused? See `assets/leads-example.csv` for an example of how to format the `.csv` file!**

# qualify.py — Rapid Lead Qualification ✔
Run `qualify.py`. It will go to each URL in `Leads.csv` and a pop-up will appear that asks if the prospect is qualified. Click Yes Or No to mark their status. Click the `X` on the top right of the pop up to exit.

Anytime you'd like to continue, simply run `qualify.py` again. It will start with the earliest prospect that does not have a status yet (anyone who you haven't marked as qualified / unqualified).

# message.py — Direct Message Automation 📲
First, adjust the settings in `message.py` to your preferences:
1. Go to the section titled `ALL MESSAGES`
2. Customize or create your own **message list**. Should be a list of messages you'd like to send, with each message being a string. Bot will select a random message then send it to the next queued prospect, wait for a set time, then repeat.
    -  If you'd like to send a mult-line message, then create a sub-list that contains multiple strings.
    - Example: `my_messages = [['hello', 'world'], 'hi there']` -> will send `hello` and `world` in separate messages if selected. if `hi there` is selected then it will send in one message.
    - Can use to make it send more human texts, rather than giant paragraphs.
3. Can also create a **"message tag" list**. Bot will add a random message from tag list to the end of the random message it selects. Used to make messages seem more random to reduce chances of ban.
    - Format is identical to other messages lists, see step 2
4. Go the section titled `MESSAGING SETTINGS`
5. Set `messages_to_send` to your desired list of messages. Bot will select a random message from the list each time it sends a message.
6. Set `tags` equal to the tags list you want to use (without quotes), or to `""` if you don't want to send tags.
7. Set your `send_limit`, the maximum of messages you want to send before the bot stops.
8. Can optionally change `time_between_messages`, which is a list of the lowest and highest amount of time to wait between messages

**Congrats! You're ready to go!**

**Simply run `message.py` and let it work it's magic!**

# Why I Created This Tool 🤔

In the past I was doing a Social Media Marketing Agency as a side project.

This is a business where you sell marketing services to businesses.

I used `D7 Lead Finder` to scrape large (and publicly available!!) amounts of data on used car dealerships.

I then used these scripts to rapidly qualify & message those dealerships, while avoiding a ban on Facebook for spamming messages to people due to using the same messages and/or sending messages too quickly.
