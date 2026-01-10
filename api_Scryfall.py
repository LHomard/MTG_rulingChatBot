import requests, json

bulkAPI_URL = "https://api.scryfall.com/bulk-data"
bulk = requests.get(bulkAPI_URL).json()



ruling_data = next(
    item for item in bulk['data']
    if item['type'] == 'rulings'
)

oracleCard_data = next(
    card for card in bulk['data']
    if card['type'] == 'oracle_cards'
)

ruling_response = requests.get(ruling_data['download_uri']).json()
card_response = requests.get(oracleCard_data['download_uri']).json()



def getRuling(rules, oracle_id):
    return [ rule for rule in rules if rule['oracle_id'] == oracle_id
    ]

def getOracleCard(cards, name):
    name = name.lower()
    for card in cards:
        if card['name'].lower() == name:
            return card
    return None
    


RULE_KEYWORDS = {
    "deathtouch", "flying", "trample", "ward", "cascade",
    "flash", "double strike", "lifelink", "hexproof",
    "indestructible", "menace"
}
    
def relevant_cards(card):
    oracle_text = card.get("oracle_text", "").lower()
    #keyword = set(k.lower() for k in card.get('keywords', []))

    #relevent_keywords = bool(keyword & RULE_KEYWORDS)
    relevent_oracle = oracle_text and len(oracle_text) > 50

    return (
        relevent_oracle
    )


filtered_cards = [c for c in card_response]    
print(len(filtered_cards))



