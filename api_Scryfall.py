import requests, sqlite3, json

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
    
    
def relevant_cards(card):
    oracle_text = card.get("oracle_text", "").lower()
    relevent_oracle = oracle_text and len(oracle_text) > 50

    return (
        relevent_oracle
    )


filtered_cards = [c for c in card_response]   


conn = sqlite3.connect("database.db", timeout=30)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS scryfallbulkdata(
                card_id TEXT PRIMARY KEY,
                name TEXT,
                mana_cost TEXT,
                cmc INTEGER,
                type_line TEXT,
                oracle_text TEXT,
                power TEXT,
                toughness TEXT,
                colors TEXT,
                color_identity TEXT,
                keywords TEXT
                )
            """)

for card in filtered_cards:

    if 'power' or 'thoughness' or 'mana_cost' or 'oracle_text' not in card.keys():
        card.update({'power':'', 'toughness':'', 'mana_cost':'', 'oracle_text':''})

    cur.execute("""INSERT INTO scryfallbulkdata(card_id, name, mana_cost, cmc, type_line, oracle_text,
                    power, toughness, colors, color_identity, keywords) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(card_id) DO UPDATE SET
                    name = excluded.name,
                    mana_cost = excluded.mana_cost,
                    cmc = excluded.cmc,
                    type_line = excluded.type_line,
                    oracle_text = excluded.oracle_text,
                    power = excluded.power,
                    toughness = excluded.toughness,
                    colors = excluded.colors,
                    color_identity = excluded.color_identity,
                    keywords = excluded.keywords """,
                (
                card['id'],
                card['name'], 
                card['mana_cost'],
                card['cmc'],
                card['type_line'],
                card['oracle_text'],
                card['power'], 
                card['toughness'],
                json.dumps(card.get('colors', [])),
                json.dumps(card.get('color_identity', [])),
                json.dumps(card.get('keywords', []))
                )
            )
    
    conn.commit()

cur.execute("""
    SELECT card_id, name, mana_cost, colors
    FROM scryfallbulkdata
    LIMIT 5
""")

for row in cur.fetchall():
    print(row)