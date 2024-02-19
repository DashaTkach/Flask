import requests

response = requests.get(
    "http://127.0.0.1:5000/ann/1",
    json={"title": "My first announcement", "description": "something about that", "owner": "1"},
    timeout=(15, 20), )
print(response.status_code)
print(response.json())
