import requests

api_URL = "https://api.scryfall.com/bulk-data"

response = requests.get(api_URL).json()

ruling_data = next(
    item for item in response['data']
    if item['type'] == 'rulings'
)


oracleCard_data = next(
    card for card in response['data']
    if card['type'] == 'oracle_cards'
)


print(ruling_data['download_uri'])

card_info = requests.get(oracleCard_data['download_uri']).json()
print(card_info)