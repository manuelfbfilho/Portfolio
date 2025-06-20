import tkinter as tk
import requests
import re
import folium

def get_address_info(address_or_cep):
    # Define a base URL for the ViaCEP API
    base_url = "https://viacep.com.br/ws/"

    # Check if the input is a valid CEP (ZIP code)
    if address_or_cep.isdigit() and len(address_or_cep) == 8:
        endpoint = f"{base_url}{address_or_cep}/json/"
    else:
        # Assume the input is an address
        endpoint = f"{base_url}json/{address_or_cep}/"

    # Make a GET request to the API
    response = requests.get(endpoint)

    # Parse the JSON response
    data = response.json()

    # Extract relevant information
    formatted_address = data.get("logradouro", "")
    neighborhood = data.get("bairro", "")
    city = data.get("localidade", "")
    state = data.get("uf", "")
    cep = data.get("cep", "")
    ddd = data.get("ddd", "")
    latitude = data.get("latitude", "")
    longitude = data.get("longitude", "")

    # Return the extracted information
    return {
        "formatted_address": formatted_address,
        "neighborhood": neighborhood,
        "city": city,
        "state": state,
        "cep": cep,
        "ddd": ddd,
        "latitude": latitude,
        "longitude": longitude
    }

def display_on_map(address_info):
    # Create a folium map centered at the specified latitude and longitude
    map_center = [float(address_info["latitude"]), float(address_info["longitude"])]
    my_map = folium.Map(location=map_center, zoom_start=15)

    # Add a marker for the address
    folium.Marker(
        location=map_center,
        popup=address_info["formatted_address"],
        icon=folium.Icon(color="blue"),
    ).add_to(my_map)

    # Save the map as an HTML file
    my_map.save("address_map.html")

    print(f"Map saved as address_map.html. Open the file in a web browser to view the location.")

root = tk.Tk()
root.title("Buscador de CEP")
root.geometry("500x350")

# Carregue a imagem de fundo (Colocar o endereço de onde está sua imagem)
bg_image = tk.PhotoImage(file="C:\\Users\\Dell\\Downloads\\Aulas_Python\\BuscaCEP\\BuscadorCEP.png")

# Crie um canvas para exibir a imagem de fundo
canvas = tk.Canvas(root, width=500, height=350)
canvas.pack()

# Exiba a imagem no canvas
canvas.create_image(0, 0, anchor="nw", image=bg_image)

# Caixa de texto para digitar o CEP
cep_entry = tk.Entry(root, width=19, bg="#007c8a", relief="flat", font=("Helvetica", 10))
cep_entry.place(x=280, y=78)

# Carregue a imagem do botão (Colocar o endereço de onde está sua imagem do botão)
button_image = tk.PhotoImage(file="C:\\Users\\Dell\\Downloads\\Aulas_Python\\BuscaCEP\\BotaoPeq.png")

# Crie um rótulo para exibir a imagem como botão
custom_button = tk.Button(root, image=button_image, command=get_address_info, bd=0, highlightthickness=0, activebackground="#001c30")
custom_button.place(x=430, y=78)

# Resto do seu código (rótulos para informações sobre o CEP)
resultado_label = tk.Label(root, font=("Helvetica", 11), fg="red", bg="#001c30")
resultado_label.place(x=310, y=105)

endereco_label = tk.Label(root, font=("Helvetica", 10), fg="#d7b317", bg="#001c30")
endereco_label.place(x=35, y=200)

bairro_label = tk.Label(root, font=("Helvetica", 10), fg="#d7b317", bg="#001c30")
bairro_label.place(x=350, y=200)

cidade_label = tk.Label(root, font=("Helvetica", 10), fg="#d7b317", bg="#001c30")
cidade_label.place(x=35, y=260)

estado_label = tk.Label(root, font=("Helvetica", 10), fg="#d7b317", bg="#001c30")
estado_label.place(x=250, y=260)

ddd_label = tk.Label(root, font=("Helvetica", 10), fg="#d7b317", bg="#001c30")
ddd_label.place(x=400, y=260)

cep_label = tk.Label(root, font=("Helvetica", 10), fg="#d7b317", bg="#001c30")
cep_label.place(x=35, y=320)

root.mainloop()

