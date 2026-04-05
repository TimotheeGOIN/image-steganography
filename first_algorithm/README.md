# The First Algorithm
This folder is dedicated to the fisrt steganography algorithm, this one will be fully described, explained and open source.
This markdown file (will) contain(s) a detailed explanation of how this algorithm works.

The idea of this one algo is not to be the most efficient in the way it stores data in an image, but to be a encrypted way to store data.
So, technically, the data stored in the images by this algo will be encrypted even though this algorithm is public. It serves as a demonstration.

- Here, I'll be focusing on the RGB(A) format of an image. This algorithm wont affect the alpha value, so we can assimilate every image format to RGB, like (255,255,255), (...), ...

- First the goal is to store data (here bits) in an image without making any human-visible difference. So, we can right away say that modifying the first digit of any R, G or B value is not a consistent option.
Modifiying one of these can create a too big gap between the original value and the new one, an this can clearly be visible on the image by human eye.
