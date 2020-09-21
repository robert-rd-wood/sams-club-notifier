# Sam's Club Notifier

**Description**  
Script to check stock status on Sam's Club items and send an SMS alert when any followed items are in stock.  

---

**Instructions**  
  * Create environment using the included requirements file  
  * Sign up for a free trial account with Twilio (https://www.twilio.com)  
  * Populate Twilio credentials and phone numbers in __twilio_creds.py__  
  * Add URLs for desired items into __shopping_list.py__  
  * Run __sams_club_notifier.py__, which will ping the Sam's Club site for each of the desired items at random intervals (default between 5-15 minutes)  
  * Upon finding any of the items in stock, the script will trigger an SMS message including the item name and a shortened link to the item page