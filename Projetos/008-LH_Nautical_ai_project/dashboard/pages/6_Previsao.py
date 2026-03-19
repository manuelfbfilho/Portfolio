import streamlit as st
import plotly.graph_objects as go
from utils.data_loader import carregar_dados
from utils.filters import aplicar_filtros
from utils.forecasting import previsao_baseline

st.title("🤖 Previsão de Demanda")

st.markdown("""
### 📌 Como funciona o modelo

Este modelo utiliza **média móvel de 7 dias**:

- Considera apenas dados passados (sem data leakage)
- A cada dia previsto:
  - calcula a média dos últimos 7 dias
  - usa o valor previsto para continuar a previsão

👉 É um modelo baseline simples, usado como referência inicial.
""")

df = aplicar_filtros(carregar_dados())

produto = st.selectbox("Produto", df['name'].unique())

df_p = df[df['name']==produto]

serie = df_p.groupby('sale_date')['qtd'].sum()

if len(serie) < 7:
    st.warning("Dados insuficientes para previsão (mínimo 7 dias).")
    st.stop()

prev = previsao_baseline(serie.values)

fig = go.Figure()
fig.add_trace(go.Scatter(y=serie.values,name="Real"))
fig.add_trace(go.Scatter(y=prev,name="Previsto"))

st.plotly_chart(fig)