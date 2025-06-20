import pypdf

leitor = pypdf.PdfReader("ambev.pdf")

textos = [pagina.extract_text() for pagina in leitor.pages]
texto = ''.join(textos)

print(leitor.pages[0].extract_text())
print(texto)