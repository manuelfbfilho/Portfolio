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

# Example usage:
address_or_cep = input("Digite um endereço ou CEP: ")
address_info = get_address_info(address_or_cep)

print("Endereço formatado:", address_info["formatted_address"])
print("Bairro:", address_info["neighborhood"])
print("Cidade:", address_info["city"])
print("Estado:", address_info["state"])
print("CEP:", address_info["cep"])
print("DDD:", address_info["ddd"])
print("Latitude:", address_info["latitude"])
print("Longitude:", address_info["longitude"])

# Display the location on a map
display_on_map(address_info)