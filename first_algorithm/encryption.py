from email import message_from_file
from operator import index

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


def binary_to_string(binary_str: str) -> str:
    """
    Converts binary value (in a string) to a string. The provided binary value must be cleared (only bits), without
    notations like 0bXXXXXXXX, only XXXXXXXX as 0's and 1's
    :param binary_str: The binary value we want to convert into a string.
    :return: A string, the binary value converted.
    """

    # ensure the binary value comes in bytes
    if len(binary_str) % 8 != 0:
        raise ValueError("Binary string length must be a multiple of 8.")

    converted_string = ""

    for i in range(0, len(binary_str), 8):

        byte = binary_str[i:i+8]
        converted_string += chr(int(byte, 2))

    return converted_string


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


def recreate_image(size: tuple[int, int], image_data: list[tuple[int, ...]], debug_prints: bool=False) -> Image:
    """
    This function reconstructs a Pillow Image with a list of pixels (tuples of integers).
    :param size: The size of the image.
    :param image_data: The list of pixels (list of tuples of integers)
    :return: An image as a PIL.Image object
    """

    new_image = Image.new("RGBA", size)

    if debug_prints: print("Starting image reconstitution...")

    for y in range(size[1]):
        for x in range(size[0]):

            i = y*size[0] + x
            new_image.putpixel((x, y), tuple(image_data[i]))

        if debug_prints: print(f"Row {y+1}/{size[1]} reconstituted.")

    return new_image


def get_closest(current_number: int, second_digit_parity: int, third_digit: int) -> int:
    """
    This function takes in a number and outputs the closest number, to the given one, that has its second digit parity and
    third digit value the same as provided.
    :param current_number: An integer, the normal number we want the closest to
    :param second_digit_parity: Parity of the second digit number. Either 0 (even) or 1 (odd)
    :param third_digit: Third digit value
    :return: An integer
    """

    # the first element of the candidate list
    base_candidate = third_digit + 10 * second_digit_parity

    # all valid candidates are offset by 20
    candidates = []

    for k in range(13): # we only need to check 13 candidates because 20*13 = 260 > 255, so we are sure to have covered all possible candidates in the range [0,255]
        if 0 <= (base_candidate + 20 * k) <= 255:
            candidates.append(base_candidate + 20 * k)

    # we get the absolute of the difference between the current number, and the candidate for each candidate
    # the smallest gap indicates which candidate is the closest of the actual
    gaps_list = [abs(current_number-candidate) for candidate in candidates]

    # we use the lowest gap index in this list to get the closest candidate in the candidate list (because there are as many numbers in these 2 lists)
    smallest_gap_index = gaps_list.index(min(gaps_list))

    return candidates[smallest_gap_index]


def encrypt(message: str, image: Image, debug_prints: bool=False) -> list[tuple[int, ...]]:
    """
    This function takes in the data of an image (here a list of pixels) and encrypts the given message in this image data
    with the first algorithm. This one is fully detailed on the GitHub project.
    :param message: In a string, the message/data we want to encrypt in an image.
    :param image: The image in which we will encrypt the message in. This image must be given as a PIL.Image object.
    :return: Returns an image as a PIL.Image object containing the message given encrypted.
    """

    # get all the pixels in the image in a list
    image_data = list(image.get_flattened_data())

    # convert the message in bytes
    message_bytes = string_to_binary(message)

    # compute the lenght of the message in bytes (plus the 4 bytes for the lenght of the message itself)
    message_lenght = bin(len(message_bytes) + 4)[2:].zfill(32)

    # convert the 32 bits (4 bytes) from a single string to 4 separated strings in a list
    message_lenght_in_bytes = [message_lenght[i:i+8] for i in range(0, len(message_lenght), 8)]

    # concatenate the lists to get the final message including the message lenght + the message
    message_bytes = message_lenght_in_bytes + message_bytes

    # check if the image is big enough to contain the message
    if not check_storage(message, image):
        raise Exception("The message is too big to be encrypted in the given image.")

    half_byte_index = 0
    current_message_byte = message_bytes[0]

    new_image_data = []

    if debug_prints: print("Starting encryption...")

    # we cycle through each tuple and each byte (excluding the alpha byte of each pixel)
    for pixel in image_data:

        new_pixel = []

        for color_byte in pixel:
            # not using the alpha byte (the 4th value in the pixel)
            if color_byte == pixel[3]:
                new_pixel.append(color_byte)
                continue # skip

            # when the entier message is encrypted, an IndexError will be thrown
            try:

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

                half_byte_index += 1

            # catch this error means the message has been fully encrypted, now we just copy the pixels as they were in the new image
            except IndexError:
                new_pixel.append(color_byte)

        if debug_prints: print(f"{(half_byte_index/2)*100/int(message_lenght, 2):.2f}% of the message encrypted")

        new_image_data.append(new_pixel)

    return new_image_data


def decrypt(image: Image, debug_prints: bool=False) -> str | None:
    """
    This function takes in an Image and decrypts the hidden message in it with this first algorithm.
    :param image: The image (as PIL.Image object) we will extract the hidden data.
    :return: The hidden data in this images in binary as a string.
    """

    # get all the pixels in the image in a list
    image_data = list(image.get_flattened_data())

    # set the decrypted bits
    decrypted_bits = ""

    half_byte_index = 0

    # we cycle through each tuple and each byte (excluding the alpha byte of each pixel)
    for pixel in image_data:
        for color_byte in pixel:

            # not using the alpha byte (the 4th value in the pixel)
            if color_byte == pixel[3]:
                continue  # skip

            half_byte_index += 1

            # ensure the byte (in decimal) is a 3-character long string
            color_byte = str(color_byte).zfill(3)

            second_digit_parity = int(color_byte[1]) % 2
            third_digit = int(color_byte[2]) * 2

            half_byte_bin = bin(third_digit+second_digit_parity)
            # get rid of the 0bXXXX notation and ensure that its 4 chars long
            half_byte_bin = half_byte_bin[2:].zfill(4)

            decrypted_bits += half_byte_bin

            #if debug_prints: print(f"{half_byte_index*100 / (int(decrypted_bits[:32], 2)*2 + 1):.2f}% of the message decrypted")



            if len(decrypted_bits) >= 32: # lenght of the 4 first bytes

                #if debug_prints: print(f"{half_byte_index*25 / int(decrypted_bits[:32], 2)*2:.2f}% decrypted")

                # stop and return if the number of bits decrypted is the same as the number of bits of the message
                if half_byte_index == int(decrypted_bits[:32], 2)*2:

                    # return the message in binary without the message lenght header
                    return decrypted_bits[32:]
    return None


"""image_file_path = "C:/Users/timot/Python Projects/Steganography/first_algorithm/images/fhd_image_2.png"
base_image = Image.open(image_file_path).convert("RGBA")

message = "Ceci est un exemple de texte simple qui sera répété pour atteindre la taille demandée. "

new_image_data = encrypt(message, base_image)
print(new_image_data)

new_image = recreate_image(base_image.size, new_image_data)

base_image.show()
new_image.show()

# verify the hidden data
decrypted = decrypt(new_image, debug_prints=True)

print(f"{decrypted = }")
print(f"{string_to_binary(message) = }")

print(f"{binary_to_string(decrypted) = }")"""



image_file_path = "C:/Users/timot/Python Projects/Steganography/first_algorithm/images/fhd_image_2.png"
base_image = Image.open(image_file_path).convert("RGBA")

message = "Ceci est un exemple de texte simple qui sera répété pour atteindre la taille demandée. "
with open("C:/Users/timot/Python Projects/Steganography/big_text.txt", "r") as file:
    message = file.read()

new_image_data = encrypt(message, base_image)
print(new_image_data)

new_image = recreate_image(base_image.size, new_image_data)

base_image.show()
new_image.show()

# verify the hidden data
decrypted = decrypt(new_image, debug_prints=True)

decrypted_string = binary_to_string(decrypted)

print(f"{len(decrypted_string) = }")

with open("C:/Users/timot/Python Projects/Steganography/hidden_message.txt", "w") as f:

    f.write(decrypted_string)

"""print(f"{decrypted = }")
print(f"{string_to_binary(message) = }")

print(f"{binary_to_string(decrypted) = }")"""





