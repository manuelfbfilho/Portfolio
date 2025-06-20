from openpyxl import load_workbook
from openpyxl.utils import FORMULAE

wb = load_workbook("Fórmulas.xlsx")
sheet = wb["Vendas"]

# criando o cabeçalho da coluna E
sheet["E1"] = "Valor total"

for linha in range(2, 12):
    sheet[f"E{linha}"] = f"=C{linha}*D{linha}"

# verificando todas as fórmulas disponíveis
for i in FORMULAE:
    print(i)

# utilizando uma fórmula pronta
sheet["E12"] = "=SUM(E2:E11)"

# salvando o arquivo
wb.save("Fórmulas.xlsx")

