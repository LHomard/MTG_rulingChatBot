import ollama

client = ollama.Client(host='http://localhost:11434',
  headers={'x-some-header': 'some-value'}
)


response = client.chat(model='llama3.1', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])

print(response["message"]["content"])