import requests

data = requests.get("http://127.0.0.1:5000/hello")

print(data.json())
