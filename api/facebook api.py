import requests

url = ""

data = requests.get(url)

print(data.text)