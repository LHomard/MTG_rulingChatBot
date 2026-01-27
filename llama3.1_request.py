import ollama, mysql.connector, faiss
from langchain_ollama import OllamaEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from mysql.connector import pooling, Error
#embedding_dim = len(embeddings.embed_query("hello world"))
#index = faiss.IndexFlatL2(embedding_dim)

##vector_store = FAISS(
#    embedding_function=embeddings,
#    index=index,
#    docstore=InMemoryDocstore(),
#    index_to_docstore_id={},
#)

client = ollama.Client(host='http://localhost:11434',
  headers={'x-some-header': 'some-value'}
)

conn = mysql.connector.connect(
      host='localhost',
      user='root',
      password="(Lolochac1!)",
      database = 'db_mtg'
    )

#embeddings = OllamaEmbeddings(model="llama3")


try:
    connPool = pooling.MySQLConnectionPool(
        pool_name='mtgPool',
        pool_size=5,
        host='localhost',
        user='root',
        password="(Lolochac1!)",
        database = 'db_mtg'
        )     
except Error as e:
    print(f"Error creating connection pool: {e}")
    connPool = None
    

def fetch_content(question):
    if not connPool:
        print("echec a la creation de pool")
        return ""
    
    connection = None
    cursor = None

    try:
        conn = connPool.get_connection()

        if conn.is_connected():
            print("je suis connecter")

        cursor = conn.cursor(dictionary=True)

        user_input = f"{question}"
        user_input.lower()

        cursor.execute(
            """SELECT name, oracle_text, power, toughness,
                MATCH(name, oracle_text) AGAINST (%s IN NATURAL LANGUAGE MODE) AS score
                FROM scryfallbulkdata
                WHERE MATCH(name, oracle_text) AGAINST (%s IN NATURAL LANGUAGE MODE)
                ORDER BY score DESC
                LIMIT 3;""", (user_input, user_input)
        )

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return ""
        
        context = ""
        for row in rows:
            context += f"Card : {row['name']}\n"
            context += f"Oracle text : {row['oracle_text']}\n\n"
            if row.get('power') and row.get('toughness'):
                context += f"Power/Toughness : {row['power']}/{row['toughness']}\n"
            context += "\n"
        return context

    except Error as e:
        print(f"Erreur de connection : {e}")
        return ""

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


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

        Always respond in the user language

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