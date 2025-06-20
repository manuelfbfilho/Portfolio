import pdfplumber

pdf = pdfplumber.open("sebrae.pdf")

# extrair textos
texto = pdf.pages[13].extract_text()
print(texto)

# extrai apenas a maior tabela da pagina
tabela = pdf.pages[29].extract_table()
tabela

# extrai todas as tabelas da pagina
tabelas = pdf.pages[29].extract_tables()

# primeira tabela
print(tabelas[0])

# acessando cada linha da tabela
for linha in tabelas[0]:
    print(linha)

# segunda tabela
tabelas[1]

# acessando cada linha
for linha in tabelas[1]:
    print(linha)

