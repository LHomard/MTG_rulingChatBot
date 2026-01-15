import sqlite3, json
from api_Scryfall import filtered_cards

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

    card.setdefault('power', '')
    card.setdefault('toughness', '')
    card.setdefault('mana_cost', '')
    card.setdefault('oracle_text', '')
    
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