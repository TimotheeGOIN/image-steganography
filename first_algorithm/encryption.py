
from PIL import Image

# get the image and convert it to RGBA
image_file_path = "C:/Users/timot/Python Projects/Steganography/first_algorithm/images/img.png"
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


def recreate_image(size: tuple[int, int], image_data: list[tuple[int, ...]]) -> Image:
    """
    This function reconstructs a Pillow Image with a list of pixels (tuples of integers).
    :param size: The size of the image.
    :param image_data: The list of pixels (list of tuples of integers)
    :return: An image as a PIL.Image object
    """

    new_image = Image.new("RGBA", size)

    for y in range(size[1]):
        for x in range(size[0]):

            i = y*size[0] + x
            new_image.putpixel((x, y), tuple(image_data[i]))

    return new_image


def get_closest(actual_number: int, second_digit_parity: int, third_digit: int) -> int:
    """
    This function takes in a number and outputs the closest number, to the given one, that has its second digit parity and
    third digit value the same as provided.
    :param actual_number: An integer, the normal number we want the closest to
    :param second_digit_parity: Parity of the second digit number. Either 0 (even) or 1 (odd)
    :param third_digit: Third digit value
    :return: An integer
    """
    print(actual_number, second_digit_parity, third_digit)

    actual_number = str(actual_number).zfill(3)

    if int(actual_number[1]) % 2 == second_digit_parity:
        closest_number = actual_number[:2] + str(third_digit)

    elif int(actual_number[2]) >= 5:
        closest_number = str(actual_number[0]) + str(int(actual_number[1]) + 1) + str(third_digit)

    elif int(actual_number[2]) <= 4:
        closest_number = str(actual_number[0]) + str(int(actual_number[1]) - 1) + str(third_digit)

    print(closest_number)
    return int(closest_number)


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

    half_byte_index = 0
    current_message_byte = message_bytes[0]

    new_image_data = []

    # we cycle through each tuple and each byte (excluding the alpha byte of each pixel)
    for pixel in image_data:

        new_pixel = []

        for color_byte in pixel:
            # not using the alpha byte (the 4th value in the pixel)
            if color_byte == pixel[3]:
                new_pixel.append(color_byte)
                continue # skip

            # the half_byte_index cycles for each 4 bits in the message (in bytes),
            # so every 2 steps, we get to the next byte in the message
            current_message_byte = message_bytes[half_byte_index//2]

            # the 4 bits of the byte we work on depend on the parity of the index
            parity_index = 4*(half_byte_index%2)
            current_half_byte = current_message_byte[parity_index:4+parity_index]

            # now, we convert the current half-byte in decimal
            decimal_half_byte = int(current_half_byte, 2)

            # determine the parity of this number (0: even, 1: odd)
            decimal_half_byte_parity = decimal_half_byte % 2

            cut_decimal_half_byte = decimal_half_byte - decimal_half_byte_parity

            # modifying the color bite to hide data in it
            new_color_byte = get_closest(int(color_byte), decimal_half_byte_parity, cut_decimal_half_byte//2)

            new_pixel.append(new_color_byte)

        new_image_data.append(new_pixel)

    return new_image_data

a = encrypt("bonjour", base_image)

print(a)

ni = recreate_image(base_image.size, a)
print("eeeeeeeeeeeeeeeeeee")

base_image.show()
ni.show()

print("oui")






