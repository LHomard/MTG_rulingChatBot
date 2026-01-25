import ollama, mysql.connector

client = ollama.Client(host='http://localhost:11434',
  headers={'x-some-header': 'some-value'}
)

def fetch_content(question):
    
    conn = mysql.connector.connect(
      host='localhost',
      user='root',
      password="(Lolochac1!)",
      database = 'db_mtg'
    )

    cur = conn.cursor()

    cur = conn.cursor(dictionary=True)

    user_input = f"%{question}%"
    user_input.lower()

    cur.execute(
        """SELECT name, oracle_text
        FROM scryfallbulkdata
        WHERE name LIKE %s
        OR oracle_text LIKE %s
        LIMIT 5""", (user_input, user_input)
    )

    rows = cur.fetchall()
    conn.close()

    if not rows:
        return ""
    
    context = ""
    for row in rows:
        context += f"Card : {row['name']}\n"
        context += f"Oracle text : {row['oracle_text']}\n\n"

    return context


def build_prompt(context, question):
    return f"""
        You are an expert Magic: The Gathering rules judge.

        You must follow these rules:
        1. Do NOT invent cards or rules.
        2. If the context is insufficient, say so.
        3. Use official MTG terminology.
        4. Oracle text is authoritative.

        If the scenario is incomplete or fragmented, explicitly say:
        "I need the full game state and stack to answer correctly."

        Context:
        {context}

        Question:
        {question}
        """
    
def ask_judge(question):
    context = fetch_content(question)

    prompt = build_prompt(context, question)

    response = client.chat(model='llama3.1',
        messages=[{
          'role': 'user',
          'content': prompt}],
        options={'temperature':0.1})

    print(response["message"]["content"])


print("Bonjour! Écrire Bye pour sortir")
exit_list = ["Bye", "bye"]
while True:
    question = input()
    if question in exit_list:
      break

    ask_judge(question)