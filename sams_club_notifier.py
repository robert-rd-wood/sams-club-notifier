from twilio.rest import Client
from bs4 import BeautifulSoup
import requests
import pyshorteners
import time
import random
from datetime import datetime

# Import shopping list
import shopping_list

# Import Twilio credentials
import twilio_creds

# Instantiate URL shortener
s = pyshorteners.Shortener()

# List of URLs to be checked for stock
URLs = shopping_list.URLs

def check_stock_status():

    i=0

    while i==0:

        now = datetime.now().strftime('%m/%d/%y %I:%M %p')
        print(f'{now}:')

        for index,URL in enumerate(URLs, start=1):

            # Pull html of target product page
            page = requests.get(URL)

            # Parse content and create bs object
            soup = BeautifulSoup(page.content, 'html.parser')

            # Product name
            try:
                prod_name = soup.find('div',class_="sc-product-header-title-container").text
            except AttributeError:
                print(f'*** ERROR ***\n\nProduct name div =\n{soup.find("div",class_="sc-product-header-title-container")}')

            # Check to see if div for "add to cart" exists
            try:
                # Wrapper div
                online_button_wrapper = soup.find('div', class_='sc-cart-qty-button online')
                # Button for 'Ship this item'
                online_button = online_button_wrapper.find('button',class_='sc-btn sc-btn-primary')
            except:
                online_button_wrapper = ''
                online_button = ''

            # Double-check button text, see if there is a disabled flag
            try:
                if (online_button.find('span').text == 'Ship this item') and (online_button['disabled'] == ''):
                    print(f'Item {index} out of stock - {prod_name}')
            except AttributeError:
                print(f'Item {index} out of stock - {prod_name}')
            except KeyError as err:
                if (online_button.find('span').text == 'Ship this item'):
                    print(f'Item {index} IN STOCK! {prod_name}')

                    # Shorten URL
                    tinyURL = s.tinyurl.short(URL)

                    # Text of SMS
                    msg_text = "In-Stock Alert!  " + prod_name + " " + tinyURL

                    # Send SMS
                    send_sms(msg_text)

                    # Break out of loop
                    i=1
                    return

        print('')
        # Seconds to wait (5-15 minutes)
        wait_secs = random.randrange(300, 900)
        time.sleep(wait_secs)

def send_sms(text):

    # Instantiate Twilio client
    client = Client(twilio_creds.account_sid, twilio_creds.auth_token)

    # Send SMS notification
    client.messages.create(to = twilio_creds.rec_number,
                            from_ = twilio_creds.my_number, 
                            body = text
                            )

if __name__ == "__main__":
    check_stock_status()