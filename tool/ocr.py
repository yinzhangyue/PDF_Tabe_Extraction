import pytesseract
from PIL import Image
text = pytesseract.image_to_string(Image.open("0.png"))
print(text)
