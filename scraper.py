from bs4 import BeautifulSoup
import requests
import cloudscraper
import pandas as pd

user_input = "0x5FFA235A2478A1e3E1b01CC1EE968Bee915351AF"
scraper = cloudscraper.create_scraper()


### hash overview scraper ###
url_main = scraper.get('https://etherscan.io/address/0x5FFA235A2478A1e3E1b01CC1EE968Bee915351AF')

# if url_main.status_code == 200:
#     print("connected to page")
# else:
#     print("unable to fetch page")
# get hash overview
hash_scan = BeautifulSoup(url_main.text, 'lxml')
hash_title = hash_scan.title.text
print("-- hash main title --")
print(hash_title.strip())

# get hash eth balance
overview = hash_scan.find('div', class_='row mb-4')
body = overview.find('div', class_='card-body')
balance_eth = body.select_one('div:nth-child(1)')
hash_eth_balance = balance_eth.text
split_string = hash_eth_balance. split(":", 1)
eth_balance = split_string[1]
print("-- hash eth balance --")
print(eth_balance.strip())

# get hash usd balance
balance_usd = body.select_one('div:nth-child(3)')
hash_usd_balance = balance_usd.text
split_string = hash_usd_balance. split(":", 1)
usd_balance = split_string[1]
print("-- hash usd balance --")
print(usd_balance.strip())

### token/nft scraper ###
print("-- eth token/nft holdings --")
nft_body = body.find('ul', class_='list list-unstyled mb-0')

nfts = {}
nft_count = 0
for li in nft_body.find_all('li'):
    for a in li.find_all('a'):
        nft = {}
        hash = a['href']
        new_hash = hash.replace('/token/', '')
        nft['hash'] = new_hash
        name_quantity = a.div.text
        split_string = name_quantity. split(")", 1)
        name = split_string[0]+')'
        nft['name'] = name
        quantity = ''.join(i for i in split_string[1] if i.isdigit())
        nft['quantity'] = quantity
        nft_count = nft_count + 1
        nfts[nft_count] = nft

# create a dataframe 
df_tokens = pd.DataFrame.from_dict(nfts, orient='index')
print(df_tokens.head())

## token overview scraper ###
url_tokens = scraper.get('https://etherscan.io/tokenholdings?a=0x5FFA235A2478A1e3E1b01CC1EE968Bee915351AF')

# if url_tokens.status_code == 200:
#     print("connected to page")
# else:
#     print("unable to fetch page")
# get token overview
token_scan = BeautifulSoup(url_tokens.text, 'lxml')
token_title = token_scan.title.text
print("-- hash token title --")
print(token_title)

# get token usd balance
tokens_overview = token_scan.find('div', class_='wrapper')
token_body = tokens_overview.find('main', id='content')
token_overview = token_body.find('div', class_='container space-bottom-2')
token_usd_networth = token_overview.find('div', class_='row mx-gutters-md-2').div
print("-- token usd total networth --")
token_usd_networth_total = token_usd_networth.text
split_string = token_usd_networth_total. split("$", 1)
usd_networth_total = '$' + split_string[1]
print(usd_networth_total.strip())

# get token eth balance
token_eth_networth = token_overview.find('div', class_='col-md col-md-auto u-ver-divider u-ver-divider--left u-ver-divider--none-md mb-md-4').div
print("-- token eth total networth --")
token_eth_networth_total = token_eth_networth.text
print(token_eth_networth_total.strip())

# get token assets
token_asssets_overview = token_overview.find('div', id='assets-wallet')
print("-- token assets --")
token_assets_total = token_asssets_overview.h2.text
print(token_assets_total)
# get token assets card
token_asssets_card = token_overview.find('div', class_='card')
token_asssets_table = token_asssets_card.find('table', id='mytable').tbody
tokens = {}
token_count = 0
for td in token_asssets_table.find_all('tr'):
    token = {}
    token_name = td.select_one('td:nth-child(2)', style='text').text
    token_quantity = td.select_one('td:nth-child(4)', style='text').text
    token['quantity'] = token_quantity
    token_price = td.select_one('td:nth-child(5)', style='text').text
    token['eth_price'] = token_price
    token_24change = td.select_one('td:nth-child(6)', style='text').text
    token['24r_change'] = token_24change
    token_usdvalue = td.select_one('td:nth-child(7)', style='text').text
    token['usd_value'] = token_usdvalue
    tokens[token_name] = token
    token_count = token_count + 1
# print(tokens)
df_tokens = pd.DataFrame.from_dict(tokens, orient='index')
print(df_tokens.head())

### hash transaction scraper ###
print('-- transactions --')
page_count = 0
transaction_count = 0
transactions = {}
while page_count >= 0:
    url_transactions = scraper.get(f'https://etherscan.io/txs?a=0x5FFA235A2478A1e3E1b01CC1EE968Bee915351AF&p={page_count}')

    # get transactions overview
    hash_transactions = BeautifulSoup(url_transactions.text, 'lxml')
    hash_transactions_overview = hash_transactions
    hash_transactions_title = hash_transactions_overview.title.text

    hash_transactions_card = hash_transactions.find('div', class_='container space-bottom-2')
    hash_transactions_list = hash_transactions_card.find('div', class_='card-body')
    hash_transactions_table = hash_transactions_list.find('tbody')
    nomore_alert = hash_transactions_table.find('div', class_='alert alert-warning mb-0')

    if nomore_alert is None:
        for td in hash_transactions_table.find_all('tr'):
            transaction = {}
            transaction_hash = td.select_one('td:nth-child(2)', style='text').text
            transaction['hash'] = transaction_hash
            transaction_method = td.select_one('td:nth-child(3)', style='text').text
            transaction['method'] = transaction_method
            transaction_block = td.select_one('td:nth-child(4)', style='text').text
            transaction['block'] = transaction_block
            transaction_age = td.select_one('td:nth-child(6)', style='text').text
            transaction['age'] = transaction_age
            transaction_from = td.select_one('td:nth-child(7)', style='text').text
            transaction['sender'] = transaction_from
            transaction_direction = td.select_one('td:nth-child(8)', style='text').text
            transaction['direction'] = transaction_direction
            transaction_to = td.select_one('td:nth-child(9)', style='text').text
            transaction['reciever'] = transaction_to
            transaction_ethvalue = td.select_one('td:nth-child(10)', style='text').text
            transaction['eth_value'] = transaction_ethvalue
            transaction_ethfee = td.select_one('td:nth-child(11)', style='text').text
            transaction['eth_fee'] = transaction_ethfee
            transactions[transaction_count] = transaction
            transaction_count = transaction_count + 1
        page_count = page_count + 1
    else:
        break

print(f'number of transaction pages #{page_count}')
print(f'number of transactions total #{transaction_count}')

df_transactions = pd.DataFrame.from_dict(transactions, orient='index')

df_transactions.eth_value = df_transactions.eth_value.str.rstrip(' Ether')
df_transactions.hash = df_transactions.hash.astype(object)
df_transactions.method = df_transactions.method.astype(object)
df_transactions.block = df_transactions.block.astype(int)
df_transactions.age = df_transactions.age.astype(object)
df_transactions.sender = df_transactions.sender.astype(object)
df_transactions.direction = df_transactions.direction.astype(object)
df_transactions.reciever = df_transactions.reciever.astype(object)
df_transactions.eth_value = df_transactions.eth_value.astype(float)
df_transactions.eth_fee = df_transactions.eth_fee.astype(float)
print(df_transactions.head())

# df_transactions.to_csv('df_transactions.csv',index=False)