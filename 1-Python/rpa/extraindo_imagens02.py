import pypdf

leitor = pypdf.PdfReader("ambev.pdf")

for pagina in leitor.pages:
    for imagem in pagina.images:
        with open(f'imagens/{imagem.name}', 'wb') as file:
            file.write(imagem.data)