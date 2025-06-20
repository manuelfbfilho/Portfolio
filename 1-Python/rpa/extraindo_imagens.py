import pypdf
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from PIL import Image

# Caminho para o arquivo PDF
pdf_path = "ambev.pdf"

# Converta a primeira página do PDF em uma imagem
imagens = convert_from_path(pdf_path, first_page=0, last_page=1)

# Salve a imagem como um arquivo PNG
for i, imagem in enumerate(imagens):
    imagem.save(f"imagem_{i + 1}.png", "PNG")
    print(f"Imagem {i + 1}.png salva com sucesso.")

# Leia o arquivo PDF
leitor = PdfReader("ambev.pdf")

# Imprima o número de páginas no PDF
print(f"Número de páginas no PDF: {len(leitor.pages)}")

# Extraia imagens da primeira página
for imagem in leitor.pages[0].images:
    # Converta os dados da imagem em um objeto PIL Image
    pil_image = Image.frombytes(imagem.colorspace, imagem.size, imagem.data)
    # Salve a imagem como um arquivo PNG
    pil_image.save(f"imagem_{imagem.name}.png")
    print(f"Imagem {imagem.name}.png salva com sucesso.")

# Certifique-se de que o arquivo "ambev.pdf" existe no mesmo diretório
leitor = pypdf.PdfReader("ambev.pdf")

# Leia o arquivo PDF
leitor = PdfReader("ambev.pdf")

# Imprima o número de páginas no PDF
print(f"Número de páginas no PDF: {len(leitor.pages)}")

# Imprima os dados das imagens na primeira página
for imagem in leitor.pages[0].images:
    print(imagem.data)
    
# Comentei o código dentro do loop para evitar erros adicionais
# for pagina in leitor.pages:
#     for imagem in pagina.images:
#         with open(f'imagens/{imagem.name}', 'wb') as file:
#             file.write(imagem.data)

# Imprima os dados das imagens na primeira página
for imagem in leitor.pages[1].images:
    print(imagem.data)