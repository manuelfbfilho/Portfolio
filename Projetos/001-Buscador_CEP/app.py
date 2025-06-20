# Token do design: figd_rSU2QgLxaq7P5E32D1R2k-mgfRH8vKrEYivM8yYX
# Link do design: https://www.figma.com/file/nUtinGktwzh3uxy1EhNzSb/Buscador_CEP?type=design&mode=design&t=ldbu6bU9fLt1YaFZ-1
# Obs.: Utilizar um ambiente virtual

import requests
import sys

print(sys.version)

url = 'https://viacep.com.br/ws/51011530/json/'
response = requests.request("GET", url)
print(response.json())
