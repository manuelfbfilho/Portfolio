import pandas as pd
import robot

# lendo o arquivo Excel
df = pd.read_excel('cadastro_clientes.xlsx')
robot.cadastro_web(df)