
from PIL import Image

image_file_path = "/first_algorithm/images/image_1.png"

base_image = Image.open(image_file_path).convert("RGBA")


