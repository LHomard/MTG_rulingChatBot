import mysql.connector, json
from api_Scryfall import filtered_cards

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password="(Lolochac1!)",
    database = 'db_mtg')

if conn.is_connected():
    print("Connected to MySQL")

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS scryfallbulkdata(
                card_id VARCHAR(36) PRIMARY KEY,
                name TEXT,
                mana_cost TEXT,
                cmc INT,
                type_line TEXT,
                oracle_text TEXT,
                power VARCHAR(5),
                toughness VARCHAR(5),
                colors JSON,
                color_identity JSON,
                keywords JSON,
                rawCard_json JSON
                )"""
            )

for card in filtered_cards:

    card.setdefault('power', '')
    card.setdefault('toughness', '')
    card.setdefault('mana_cost', '')
    card.setdefault('oracle_text', '')
    
    cur.execute("""INSERT INTO scryfallbulkdata(card_id, name, mana_cost, cmc, type_line, oracle_text,
                    power, toughness, colors, color_identity, keywords, rawCard_json) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    mana_cost = VALUES(mana_cost),
                    cmc = VALUES(cmc),
                    type_line = VALUES(type_line),
                    oracle_text = VALUES(oracle_text),
                    power = VALUES(power),
                    toughness = VALUES(toughness),
                    colors = VALUES(colors),
                    color_identity = VALUES(color_identity),
                    keywords = VALUES(keywords),
                    rawCard_json = VALUES(rawCard_json)
                 """,
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
                json.dumps(card.get('keywords', [])),
                json.dumps(card)
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