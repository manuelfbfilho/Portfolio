import pypdf

pdf = pypdf.PdfWriter(clone_from="o_cortico.pdf")

transformacao = pypdf.Transformation()

pdf.pages[0].add_transformation(transformacao.rotate(30))
pdf.pages[1].add_transformation(transformacao.translate(tx=400, ty=500))

pdf.write("PDF Transformações.pdf")