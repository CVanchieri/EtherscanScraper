from bs4 import BeautifulSoup
import requests
import cloudscraper
import pandas as pd

user_input = "0x5FFA235A2478A1e3E1b01CC1EE968Bee915351AF"
scraper = cloudscraper.create_scraper()


### token scraper ###
token_url_main = scraper.get('https://etherscan.io/token/0x3f5fb35468e9834a43dca1c160c69eaae78b6360?a=0x5FFA235A2478A1e3E1b01CC1EE968Bee915351AF')

# if url_main.status_code == 200:
#     print("connected to page")
# else:
#     print("unable to fetch page")
# get hash overview
hash_scan = BeautifulSoup(token_url_main.text, 'lxml')
hash_title = hash_scan.title.text
print("-- hash main title --")
print(hash_title.strip())

# # get hash eth balance
token_overview = hash_scan.find('div', id='ContentPlaceHolder1_divSummary')
token_card = token_overview.find('div', class_='card h-100')
card_body = token_card.find('div', class_='card-body')
token_floor = card_body.find('div', class_='col-12')
price_floor = token_floor.find('span', class_='d-block').text #
split_string = price_floor. split("@", 1)
usd_floor = split_string[0].strip()
eth_floor = split_string[1].strip()
token_supply = card_body.find('div', class_='row align-items-center')
total_supply = token_supply.find('div', class_='col-md-8 font-weight-medium').text #
split_string = total_supply. split(" ", 1)
total_supply = split_string[0]
token_holders = card_body.find('div', id='ContentPlaceHolder1_tr_tokenHolders')
total_holders = token_holders.find('div', class_='col-md-8').text.strip() #
print(total_holders)


