# The First Algorithm
This folder is dedicated to the fisrt steganography algorithm, this one will be fully described, explained and open source.
This markdown file (will) contain(s) a detailed explanation of how this algorithm works.

The idea of this one algo is not to be the most efficient in the way it stores data in an image, but to be a encrypted way to store data.
So, technically, the data stored in the images by this algo will be encrypted even though this algorithm is public. It serves as a demonstration.

- Here, I'll be focusing on the RGB(A) format of an image. This algorithm wont affect the alpha value, so we can assimilate every image format to RGB, as [(255,255,255), (...), ...]

- The goal is to store data (here bits) in an image without making any human-visible difference. Here I'll focus on only one byte in decimal, a value between 0 and 255.

So, first, we can right away say that modifying the first digit of any R, G or B value is here an inconsistent option.
Modifiying one of these can create a too big gap (at least 100) between the original value and the new one, an this can clearly be visible on the image by human eye. BUT, we can still observe and use this first digit without alter it.

With that said, I think shifting the second digit (to the inferior or superior one) can be possible because in the worst case it's a 19-gap. Moreover, by doing things right we can reduce this gap consistently to a 6-gap maximum, and save all the 0 to 9 digits for the third (units) digit.


## Let's describe and explain that algorithm :

- Notice that this algo works with 1 byte of the image at a time (not one pixel). So an image will be treated as a list of bytes (in decimal) rather than a list of pixels. In 1 bytes of an image, half a byte (4 bits) can be stored, hidden.
- Note that the first 4 bytes encrypted in an image specify the lenght of the encrypted message (including these 4 bytes).

In this algo, the first digit of all bytes is pretty useless.

### This byte (pixel R, G or B value) holds two hidden values.

The first one is the units (third) digit of this byte in decimal that we multiply by 2. So we can have all **even** numbers between 0 and 18 inclusive.

Then we get the parity of the second digit of the byte in decimal. If it's even, we do nothing, but if it's odd, we add 1 to the previous calculated number.

- With that, we can have **all** numbers between 0 and 19 inclusive. But we will actually use numbers between 0 and 15.

### Now, computing those numbers to get the hidden 4 bits.

- Now we have, let's say the position number as `pos_number = third_digit * 2 + second_digit % 2` in python.

This number could be directly converted into 4 bits but let's add a bit of a complexity (really simple ^^). So we flip the bits right to left.
For example, 1101 becomes 1011. Then we reverse the bits so 1011 becomes 0100.

- And THIS is the final hidden value (in this example 0100) in this byte.

## Conclusion and performances :

This algorithm can store 4 hidden bits in each byte of an image. This algorithm manipulates only the R, G and B value of the pixels so, in an image of size width by height, we can roughly store `width*height*3*4` bits of data.
Which is for a FHD (1920x1080) image a total of `1920*1080*3*4` = **24 883 200 bits** or **3 110 400 bytes** (~ 3MB of raw data)







