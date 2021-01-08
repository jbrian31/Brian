from twilio.rest import Client
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os
import time
import requests
import schedule
import random

load_dotenv()
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
out_of_stock = True
time_wait = 61
url = 'https://www.repfitness.com/rep-iso-arms-2020'


def is_within_schedule():
    daily_start_time = "06:00"
    daily_stop_time = "16:30"
    if datetime.now().weekday() < 5 and datetime.now().strftime("%H:%M") > daily_start_time and datetime.now().strftime("%H:%M") < daily_stop_time:
        return True


def get_current_date_time():
    now = datetime.now()
    return now


def find_item():
    # List of brower user agents to pick from
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]

    # randomize user-agent
    user_agent = random.choice(user_agent_list)
    # headers['User-Agent']=user_agent
    headers = {'User-Agent': user_agent}

    try:
        # scrape website
        html_text = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html_text, 'lxml')
        stock_status = soup.find(
            'div', class_='product-info-stock-sku').p.span.text.replace(' ', '').strip().lower()

        # Stock Logic
        if stock_status == "instock":
            global out_of_stock
            out_of_stock = False
            print(f'Item in stock at {get_current_date_time()}')
            print('Stock monitor ended')
            with open('log.txt', 'a') as writer:
                writer.write(
                    f'Item in stock at {get_current_date_time()} \n')
                writer.write('Stock monitor ended')
            schedule.cancel_job(find_item)

            client = Client(account_sid, auth_token)

            client.api.account.messages.create(
                to="+13019106757",
                from_="+13343452141",
                body=url)
        else:
            print(
                f'Item out of stock at {get_current_date_time()}. Waiting {time_wait} seconds to check again')
            with open('log.txt', 'a') as writer:
                writer.write(
                    f'Item out of stock at {get_current_date_time()}. Waiting {time_wait} seconds to check again \n')
    except Exception as e:
        print(f'ERROR : {type(e)} at {get_current_date_time()}')


if __name__ == '__main__':
    print(f'Running Gym Stock monitor on {url}')
    schedule.every(time_wait).seconds.do(find_item)
    while True:
        while out_of_stock == True and is_within_schedule():
            schedule.run_pending()
            time.sleep(1)
        if out_of_stock == False:
            break
