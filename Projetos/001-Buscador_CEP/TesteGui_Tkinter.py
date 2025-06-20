import tkinter as tk
import requests

def buscar_cep():
    cep = entry_cep.get()
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    data = response.json()

    if "erro" in data:
        resultado.config(text="CEP não encontrado.")
    else:
        resultado.config(text=f"Endereço: {data['logradouro']}\nBairro: {data['bairro']}\nCidade: {data['localidade']}\nEstado: {data['uf']}\nDDD: {data['ddd']}")

root = tk.Tk()
root.title("Buscador de CEP")

label_cep = tk.Label(root, text="Digite o CEP:")
entry_cep = tk.Entry(root)
button_buscar = tk.Button(root, text="Buscar", command=buscar_cep)
resultado = tk.Label(root, text="")

label_cep.pack()
entry_cep.pack()
button_buscar.pack()
resultado.pack()

root.mainloop()
