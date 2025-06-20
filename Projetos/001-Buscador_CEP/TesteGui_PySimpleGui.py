import PySimpleGUI as sg
import requests

layout = [
    [sg.Text("Digite o CEP:")],
    [sg.InputText(key="cep")],
    [sg.Button("Buscar")],
    [sg.Text("", size=(40, 5), key="resultado")]
]

window = sg.Window("Buscador de CEP", layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Buscar":
        cep = values["cep"]
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)
        data = response.json()

        if "erro" in data:
            window["resultado"].update("CEP não encontrado.")
        else:
            window["resultado"].update(f"Endereço: {data['logradouro']}\nBairro: {data['bairro']}\nCidade: {data['localidade']}\nEstado: {data['uf']}\nDDD: {data['ddd']}")

window.close()
