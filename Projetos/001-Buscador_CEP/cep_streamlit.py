import streamlit as st
import requests
import re

def pesquisar_cep():
    entrada = st.text_input("Digite o CEP ou o endereço:")

    if re.match(r"^\d{8}$", entrada):
        # Pesquisa por CEP
        url = f"https://viacep.com.br/ws/{entrada}/json/"
        response = requests.get(url)
        data = response.json()

        if "erro" in data:
            st.write("CEP não encontrado.")
        else:
            st.write(f"Endereço: {data['logradouro']}, {data['bairro']}, {data['localidade']} - {data['uf']}")
    else:
        # Pesquisa por endereço
        re.match(r"^\d{8}$", str(entrada))
        url = f"https://viacep.com.br/ws/{entrada}/json/"
        response = requests.get(url)
        data = response.json()

        if "erro" in data:
            st.write("Endereço não encontrado.")
        else:
            st.write(f"CEP: {data['cep']}")

st.title("Buscador de CEP")
pesquisar_cep()
