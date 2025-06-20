import tkinter as tk
import requests
from tkinter import ttk

# Função para realizar a pesquisa do CEP
def pesqusiar_cep(cep):
    response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
    address_data = response.json()
    return address_data

def register_user():
    user_data = {}
    user_data['cep'] = input('Digite seu CEP: ')
    
    address_data = get_address_from_cep(user_data['cep'])
    
    user_data['address'] = address_data['logradouro']
    user_data['neighborhood'] = address_data['bairro']
    user_data['city'] = address_data['localidade']
    user_data['state'] = address_data['uf']
    user_data['ddd'] = address_data['ddd']
    
    return user_data

# Configurações da janela principal
root = tk.Tk()
root.title("Buscador de CEP")
root.title("Botão Personalizado")
root.geometry("500x350")

# Carregue a imagem de fundo
bg_image = tk.PhotoImage(file="C:\\Users\\Dell\\Downloads\\Aulas_Python\\BuscaCEP\\BuscadorCEP.png")

# Crie um canvas para exibir a imagem de fundo
canvas = tk.Canvas(root, width=500, height=350)
canvas.pack()

# Exiba a imagem no canvas
canvas.create_image(0, 0, anchor="nw", image=bg_image)

# Caixa de texto para digitar o CEP
cep_entry = tk.Entry(root, width=19, bg="#007c8a", relief="flat", font=("Helvetica", 10))
cep_entry.place(x=283, y=76)

# Carregue a imagem do botão
button_image = tk.PhotoImage(file="C:\\Users\\Dell\\Downloads\\BotaoPeq.png")
# button_image.place(x=430, y=72)

# Crie o botão com a imagem como fundo
custom_button = tk.Button(root, image=button_image, borderwidth=0, command=pesquisar_cep)
custom_button.pack()

# Botão de pesquisa
#pesquisar_button = tk.Button(root, text="Pesquisar", command=pesquisar_cep)
#pesquisar_button.place(x=430, y=72)

# Crie um rótulo para exibir a imagem como botão
custom_button = tk.Button(root, image=button_image, borderwidth=0)
custom_button.place(x=440, y=68)

# Resto do seu código (rótulos para informações sobre o CEP)
endereco_label = tk.Label(root, font=("Helvetica", 12), fg="white", bg="#001c30")
endereco_label.place(x=50, y=100)

bairro_label = tk.Label(root, font=("Helvetica", 12), fg="white", bg="#001c30")
bairro_label.place(x=250, y=100)

cidade_estado_label = tk.Label(root, font=("Helvetica", 12), fg="white", bg="#001c30")
cidade_estado_label.place(x=50, y=150)

ddd_label = tk.Label(root, font=("Helvetica", 12), fg="white", bg="#001c30")
ddd_label.place(x=250, y=150)

root.mainloop()
