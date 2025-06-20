import pypdf

# lendo o arquivo PDF
arquivo_pdf = pypdf.PdfReader("o_cortico.pdf")

# Escrever um PDF
pdf_destino = pypdf.PdfWriter()

# Número de páginas do PDF
print(len(arquivo_pdf.pages))
print(arquivo_pdf.pages[0])

# percorrendo as páginas
for pagina in arquivo_pdf.pages:
    print(pagina)

# metadados de um PDF
print(arquivo_pdf.metadata)

# Extraindo uma página do PDF
pagina01 = arquivo_pdf.pages[0]
pdf_destino.add_page(pagina01)
pdf_destino.write("Pagina-01.pdf")

# Extraindo diversas páginas
paginas = [9, 14, 19]
for pagina in paginas:
    pdf_destino.add_page(arquivo_pdf.pages[paginas])

pdf_destino.write("Paginas-extraidas.pdf")
