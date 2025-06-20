import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import folium
from folium.plugins import HeatMap
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set style for better visualizations
plt.style.use('seaborn')
sns.set_palette("husl")

# URLs for the datasets
urls = {
    'loja1': "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_1.csv",
    'loja2': "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_2.csv",
    'loja3': "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_3.csv",
    'loja4': "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_4.csv"
}

# Load all datasets
lojas = {}
for loja, url in urls.items():
    lojas[loja] = pd.read_csv(url)
    # Convert date column to datetime
    lojas[loja]['Data da Compra'] = pd.to_datetime(lojas[loja]['Data da Compra'], format='%d/%m/%Y')

# Function to calculate total revenue
def calculate_revenue(df):
    return df['Preço'].sum()

# Function to calculate average rating
def calculate_avg_rating(df):
    return df['Avaliação da compra'].mean()

# Function to calculate average shipping cost
def calculate_avg_shipping(df):
    return df['Frete'].mean()

# Function to get top categories
def get_top_categories(df, n=5):
    return df['Categoria do Produto'].value_counts().head(n)

# Function to get top products
def get_top_products(df, n=5):
    return df['Produto'].value_counts().head(n)

# Function to create revenue by payment type analysis
def analyze_payment_types(df):
    payment_analysis = df.groupby('Tipo de pagamento').agg({
        'Preço': 'sum',
        'Avaliação da compra': 'mean'
    }).reset_index()
    payment_analysis['Percentual'] = (payment_analysis['Preço'] / payment_analysis['Preço'].sum()) * 100
    return payment_analysis

# Function to create ABC analysis
def create_abc_analysis(df):
    products = df.groupby('Produto').agg({
        'Preço': 'sum',
        'Quantidade de parcelas': 'count'
    }).reset_index()
    
    products['Percentual'] = (products['Preço'] / products['Preço'].sum()) * 100
    products = products.sort_values('Percentual', ascending=False)
    products['Cumulative_Percent'] = products['Percentual'].cumsum()
    
    products['Class'] = np.where(products['Cumulative_Percent'] <= 80, 'A',
                               np.where(products['Cumulative_Percent'] <= 95, 'B', 'C'))
    return products

# Function to analyze top sellers
def analyze_top_sellers(df, n=3):
    sellers = df.groupby('Vendedor').agg({
        'Preço': 'sum',
        'Avaliação da compra': 'mean',
        'Produto': 'count'
    }).reset_index()
    
    sellers = sellers.sort_values('Preço', ascending=False).head(n)
    sellers['Percentual'] = (sellers['Preço'] / sellers['Preço'].sum()) * 100
    
    # Get top 3 products for each seller
    for seller in sellers['Vendedor']:
        seller_products = df[df['Vendedor'] == seller]['Produto'].value_counts().head(3)
        sellers.loc[sellers['Vendedor'] == seller, 'Top_Products'] = ', '.join(seller_products.index)
    
    return sellers

# Function to create geographical analysis
def create_geographical_analysis(df, loja_name):
    # Create a map centered on Brazil
    m = folium.Map(location=[-15.77972, -47.92972], zoom_start=4)
    
    # Add heatmap
    heat_data = [[row['lat'], row['lon'], row['Preço']] for index, row in df.iterrows()]
    HeatMap(heat_data).add_to(m)
    
    # Save map
    m.save(f'geographical_analysis_{loja_name}.html')
    
    # Calculate regional distribution
    regional_dist = df.groupby('Local da compra').agg({
        'Preço': 'sum',
        'Avaliação da compra': 'mean'
    }).reset_index()
    
    return regional_dist

# Function to create dashboard
def create_dashboard():
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Faturamento por Loja', 
                       'Média de Avaliação por Loja',
                       'Frete Médio por Loja',
                       'Distribuição de Categorias')
    )
    
    # Add traces
    fig.add_trace(
        go.Bar(x=list(lojas.keys()),
               y=[calculate_revenue(df) for df in lojas.values()]),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=list(lojas.keys()),
               y=[calculate_avg_rating(df) for df in lojas.values()]),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Bar(x=list(lojas.keys()),
               y=[calculate_avg_shipping(df) for df in lojas.values()]),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(height=800, width=1200, title_text="Dashboard Allure Store")
    fig.show()

# Main analysis function
def main():
    # Create dashboard
    create_dashboard()
    
    # Perform detailed analysis for each store
    for loja_name, df in lojas.items():
        print(f"\nAnálise detalhada para {loja_name}:")
        print(f"Faturamento total: R${calculate_revenue(df):,.2f}")
        print(f"Média de avaliação: {calculate_avg_rating(df):.2f}")
        print(f"Frete médio: R${calculate_avg_shipping(df):.2f}")
        
        print("\nTop 5 categorias:")
        print(get_top_categories(df))
        
        print("\nTop 5 produtos:")
        print(get_top_products(df))
        
        print("\nAnálise de pagamentos:")
        print(analyze_payment_types(df))
        
        print("\nAnálise ABC:")
        print(create_abc_analysis(df))
        
        print("\nTop 3 vendedores:")
        print(analyze_top_sellers(df))
        
        # Create geographical analysis
        create_geographical_analysis(df, loja_name)

if __name__ == "__main__":
    main() 