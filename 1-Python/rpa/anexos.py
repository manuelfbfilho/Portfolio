import pypdf

pdf = pypdf.PdfWriter(clone_from="o_cortico.pdf")

with open("coxinha.jpg", "rb") as file:
    arquivo = file.read()

pdf.add_attachment('coxinha.jpg', arquivo)

pdf.write("o_cortico_anexo.pdf")

# extraindo anexos de um PDF
leitor = pypdf.PdfReader("o_cortico_anexo.pdf")

for anexo in leitor.attachments:
    arquivo = leitor.attachments[anexo][0]
    with open(f'anexos/{anexo}', 'wb') as file:
        file.write(arquivo)

    
