import pypdf
from pypdf.annotations import FreeText, Text

pdf = pypdf.PdfWriter(clone_from='o_cortico.pdf')

texto_livre = FreeText(text="Isso é um texto livre!", rect=(200, 200, 400, 400))
pdf.add_annotation(0, texto_livre)

anotacao = Text(text="Isso é uma anotação!", rect=(200, 200, 400, 400))
pdf.add_annotation(1, anotacao)

pdf.write("o_cortico_anotacao.pdf")

# verificando se existem anotações
leitor = pypdf.PdfReader("o_cortico_anotacao.pdf")
pagina1 = leitor.pages[0]

for i, pagina in enumerate(leitor.pages, start=1):
    if '/Annots' in pagina:
        for anotacao in pagina['/Annots']:
            dados_anotacao = anotacao.get_object()
            print(f"Página: {i}")
            print(f"Tipo: {dados_anotacao['/Subtype']}")
            print(f"Conteúdo: {dados_anotacao['/Contents']}\n")