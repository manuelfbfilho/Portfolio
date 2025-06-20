
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import folium_static
import numpy as np
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

import tkinter as tk
import requests
import re
from PIL import Image, ImageTk

# Configuração da página

# Estilo CSS personalizado

# URLs dos datasets
urls = {
    'loja1': "BD/loja_1.csv",
    'loja2': "BD/loja_2.csv",
    'loja3': "BD/loja_3.csv",
    'loja4': "BD/loja_4.csv"
}



# Configuração da janela principal
root = tk.Tk()
root.geometry("500x350")
root.overrideredirect(True)  # Remove a borda padrão da janela

# Definir uma cor de fundo transparente
bg_color = "#000001"
root.wm_attributes("-transparentcolor", bg_color)

# Criar um canvas para a interface arredondada
canvas = tk.Canvas(root, width=500, height=350, bg=bg_color, highlightthickness=0)
canvas.pack()

# Criar uma imagem com cantos arredondados para fundo
radius = 40
image = Image.new("RGBA", (500, 350), (0, 0, 0, 0))
mask = Image.new("L", (500, 350), 0)

for x in range(500):
    for y in range(350):
        if (
            (x < radius and y < radius and (x - radius) ** 2 + (y - radius) ** 2 > radius**2) or
            (x >= 500 - radius and y < radius and (x - (500 - radius)) ** 2 + (y - radius) ** 2 > radius**2) or
            (x < radius and y >= 350 - radius and (x - radius) ** 2 + (y - (350 - radius)) ** 2 > radius**2) or
            (x >= 500 - radius and y >= 350 - radius and (x - (500 - radius)) ** 2 + (y - (350 - radius)) ** 2 > radius**2)
        ):
            mask.putpixel((x, y), 0)
        else:
            mask.putpixel((x, y), 255)

# Carregar a imagem de fundo e aplicar a máscara arredondada
bg_image = Image.open("C:\\Users\\Dell\\Downloads\\Projetos\\BuscaCEP\\BuscadorCEP.png").convert("RGBA")
bg_image = bg_image.resize((500, 350))
bg_image.putalpha(mask)

bg_photo = ImageTk.PhotoImage(bg_image)

# Exibir a imagem no canvas
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# Permitir arrastar a janela ao pressionar o botão esquerdo do mouse
def move_window(event):
    root.geometry(f"+{event.x_root}+{event.y_root}")

canvas.bind("<B1-Motion>", move_window)

# Função para fechar a janela
def fechar_ao_clicar_fora(event):
    root.destroy()  # Fecha a janela

root.bind("<FocusOut>", fechar_ao_clicar_fora)

'''
# Funções de análise
def analise_vendas(lojas):
    # Calcular a soma de vendas por loja
    vendas_totais = {loja: df['Valor Total'].sum() for loja, df in lojas.items()}
    
    # Criar gráfico de barras
    fig = px.bar(x=list(vendas_totais.keys()), y=list(vendas_totais.values()), labels={'x': 'Loja', 'y': 'Vendas Totais'}, title='Vendas Totais por Loja')
    plotly_chart(fig)

# Recomendação final para decisão de fechamento de loja
def recomendacao_final(lojas):
    # Calcular a média de vendas por loja
    media_vendas = {loja: df['Valor Total'].mean() for loja, df in lojas.items()}
    
    # Encontrar a loja com a menor média de vendas
    loja_fechar = min(media_vendas, key=media_vendas.get)
    
    # Exibir a recomendação
    print(f"A recomendação é fechar a {loja_fechar} com uma média de vendas de R$ {media_vendas[loja_fechar]:.2f}.")
'''

