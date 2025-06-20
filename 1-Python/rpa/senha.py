import pypdf

pdf = pypdf.PdfWriter(clone_from="o_cortico.pdf")

# proteger o PDF com senha
pdf.encrypt("112233")

pdf.write("o_cortico_senha.pdf")

# lendo arquivos PDF com senha
leitor = pypdf.PdfReader("o_cortico_senha.pdf")

# inserindo a senha
leitor.decrypt("112233")

leitor.pages[0]