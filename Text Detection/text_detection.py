import pdf2image
from PIL import Image
import pytesseract
import os

from  pdf2image import convert_from_path
pages = convert_from_path("text.pdf")

data = ''

for page in pages:
    name = "out.jpg"
    page.save(name, 'JPEG')
    data += '\n\nPageBreak\n\n' + pytesseract.image_to_string(Image.open('out.jpg'), lang='eng')
    os.remove(name)

print(pytesseract.image_to_string(Image.open('hand.png'), lang='eng'))
