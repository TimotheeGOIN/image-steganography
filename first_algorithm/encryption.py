
from PIL import Image

# get the image and convert it to RGBA
image_file_path = "C:/Users/timot/Python Projects/Steganography/first_algorithm/images/small_image.png"
base_image = Image.open(image_file_path).convert("RGBA")


def string_to_binary(text: str) -> list[str]:
    """
    This function converts a string to its binary representation
    :param text: The string that will be converted
    :return: The converted text in binary in a list
    """

    # returns empty string if provided text is empty
    if text == "":
        return []

    # convert each character to binary (8-bit format)
    bytes_list = [format(ord(char), '08b') for char in text]
    return bytes_list


def check_storage(message: str, image: Image) -> bool:
    """
    This function checks if the provided image is big enough to contain the message when encrypted. Returns a boolean
    depending on whether there is enough space or not.
    :param message: The message (a string) we want to check if it fits in the image.
    :param image: The image we want to check if it could hold the encrypted message.
    :return: A boolean - True if the message fits in the image, False if not.
    """

    # calculate the amount of data we can store in the image (details on the GitHub)
    bit_image_holding_size = image.width * image.height * 3 * 4
    byte_image_holding_size = bit_image_holding_size / 8

    # convert the message in binary and get its size
    message_size = len(string_to_binary(message))

    # compare and see if the message fits in the image
    if message_size <= byte_image_holding_size:
        return True
    else:
        return False


def encrypt(message: str, image: Image) -> Image:
    """
    This function takes in the data of an image (here a list of pixels) and encrypts the given message in this image data
    with the first algorithm. This one is fully detailed on the GitHub project.
    :param message: In a string, the message/data we want to encrypt in an image.
    :param image: The image in which we will encrypt the message in. This image must be given as a PIL.Image object.
    :return: Returns an image as a PIL.Image object containing the message given encrypted.
    """

    # get all the pixels in the image in a list
    image_data = list(image.getdata())

    # convert the message in bytes
    message_bytes = string_to_binary(message)

    # check if the image is big enough to contain the message
    if not check_storage(message, image):
        raise Exception("The message is too big to be encrypted in the given image.")

    current_byte = message_bytes[0]

    # we cycle through each tuple and each byte (excluding the alpha byte of each pixel)
    for pixel in image_data:
        for byte in pixel:
            # not using the alpha byte (the 4th value in the pixel)
            if byte == pixel[3]:
                continue # skip









