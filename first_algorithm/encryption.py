
import sys, os

from PIL import Image

"""# get the image and convert it to RGBA
image_file_path = "C:/Users/timot/Python Projects/Steganography/first_algorithm/images/img.png"
base_image = Image.open(image_file_path).convert("RGBA")

# check in which form this script is executed (as a .py or as a .exe)
if getattr(sys, 'frozen', False): # executed as a .exe (compiled with PyInstaller because sys.frozen is added by PyInstaller)
    running_as_exe = True
else: # executed as a .py
    running_as_exe = False"""

# utils for the algorithm
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


def check_image_storage_capacity(message: str, image: Image) -> bool:
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


def create_output_path() -> str:
    pass


# algorithm's main functions
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


def encrypt(message: str, image: Image) -> list[tuple[int, ...]]:
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
    if not check_image_storage_capacity(message, image):
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

        new_image_data.append(new_pixel)

    return new_image_data


def decrypt(image: Image) -> str | None:
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

            if len(decrypted_bits) >= 32: # lenght of the 4 first bytes

                # stop and return if the number of bits decrypted is the same as the number of bits of the message
                if half_byte_index == int(decrypted_bits[:32], 2)*2:

                    # return the message in binary without the message lenght header
                    return decrypted_bits[32:]
    return None


if not running_as_exe:
    print("Running as a python (.py) file here...")
    exit()
else:
    print("Running as an executable (.exe) file here...")

# get all the parameters
if not 3 <= len(sys.argv) <= 4:
    raise SyntaxError("Please enter an appropriate number of arguments (usually 4 for encryption and 3 for decryption")

# * means the argument is optional
# encryption - base_image.png - image_output.png   - message(str)/message.txt
# decryption - base_image.png - message_output.txt

# define the mode parameter
mode = sys.argv[0]

# assert there are the right number of parameters
if not ((mode == "encryption" and len(sys.argv) == 4) or (mode == "decryption" and len(sys.argv) == 3)):
    raise ValueError("Please enter valid parameters")

# define all the last parameters
base_image_path = sys.argv[1]
output_path = sys.argv[2]
if mode == "encryption":
    message_to_encrypt = sys.argv[3]

# check if the image path points to a real file and if the file extension refers to an image file
if not (os.path.exists(base_image_path) and os.path.splitext(base_image_path)[1] in [".png", ".jpg", ".jpeg"]):
    raise NameError(f"The given path either doesn't point to a real file or an image file format supported. Given path : {base_image_path}")

# if the path is correct, get the image as a PIL.Image object
base_image = Image.open(base_image_path).convert("RGBA")

# check the output path already exists
if os.path.exists(output_path):
    raise FileExistsError(f"The output file already exists at this location: {output_path}. Not able to overwrite it.")

# check if the output file is an image if we want an image as an output
if not (mode == "encryption" and os.path.splitext(base_image_path)[1] in [".png", ".jpg", ".jpeg"]):
    raise ValueError(f"The provided output path does not match with the given mode: {os.path.splitext(base_image_path)[1]} are not the output for the {mode} mode...")

# or a text file if we have a message as an output
if not (mode == "decryption" and os.path.splitext(base_image_path)[1] == ".txt"):
    raise ValueError(f"The provided output path does not match with the given mode: {os.path.splitext(base_image_path)[1]} are not the output for the {mode} mode...")


# once all the params have been checked out, start encryption or decryption
if mode == "encryption":

    # encrypt data into the image
    new_image_data = encrypt(message=message_to_encrypt, image=base_image)
    # convert the data into an PIL.Image image
    new_image: Image = recreate_image(base_image.size, new_image_data)
    # save the image with pil
    base_image.save(output_path)

elif mode == "decryption":

    # extract encrypted (hidden) data (in binary) from the image
    extracted_data_bin = decrypt(image=base_image)
    # convert this data from binary to text
    extracted_message = binary_to_string(extracted_data_bin)
    # save the message in a text file
    with open(output_path, "w+") as output_file:
        output_file.write(extracted_message)

else:
    raise ValueError("This mode does not exist. Please input encryption or decryption.")







