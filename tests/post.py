import requests

host = 'localhost:18888'
text = 'Привет!'
data = [{"role": "user", "condition": "GPT4 Correct", "content": text}]
headers = {'Content-Type': 'application/json'}
response = requests.post(f'http://{host}/v1/chat/completions', json={
                    "model": "model",
                    "messages": data
                }, timeout=100)
print(response.json())
