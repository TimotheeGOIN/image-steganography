
from PIL import Image

image_file_path = "C:/Users/timot/Python Projects/Steganography/images/image_1.png"

base_image = Image.open(image_file_path).convert("RGBA")


