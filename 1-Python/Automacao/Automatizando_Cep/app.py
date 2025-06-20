import requests

url = 'https://viacep.com.br/ws/22041001/json/'
response = requests.request("GET", url)

print(response.json())