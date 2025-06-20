from openpyxl import Workbook
from openpyxl.drawing.image import Image

wb = Workbook()
sheet = wb.active

img = Image("logo.png")
sheet.add_image(img, "A1")

wb.save("Inserindo imagem.xlsx")

