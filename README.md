# My Image Steganography 

This repo is where I'll put my steganography algorithm(s). 
The goals are to learn about steganography and to create an example algorithm quite simple. 

The idea is not the have the fastest or most optimized algorithm but just to try, search and do it by myself, that's why I'm doing it in python. So the code code may not be the clearest and the most efficient neither. 

- There will be more than one algorithm so, each one will have its own directory contaning the algorithm itself as a python file and a README file detailing how this algo works and its specifications.
- The 'executables' directory contains all the differents steganography algorithm as executable (.exe) files. Eventually with a README file detailling use of them.
- The 'steganography_manager' python file gathers all the differents algorithms in one graphical interface. This manager's goal is to make those algorithms easier to use. For example, we only have to select an image, a message to encypt in an the algorithm of my choice then a new image is created.


### Progression :

- First algorithm  : 100%
- Second algorithm : 0%
- Manager          : 0%


## Usage details

The algorithm as .exe files alone are meant to be used in a **command line console** (that is why the graphical manager is useful).
So, all the following usage details for those algorithms work preferably in a in-line command console.

Note that giving **relative** paths as parameters may work BUT **absolute** paths are more preferable.


### The manager :

...


### First algorithm (as a .exe file):

This algorithm handles both encryption and decryption, and is pretty straight forward to use. 

This executable takes in 3 or 4 parameters depending on the choosen mode, but this is basically : `algorithm.exe  mode  base_image  output  message` 

- The `mode` is either `"encryption"` or `"decryption"`. I think this parameters is pretty straight forward, it defines which mode of the algorithm you want to use. `encryption` is for encrypt data into an image and `decryption` to extract the data hidden in an image (obviously data that was encrypted with the same algorithm).
- The `base_image` is the image you want to either **encrypt data in** (with encryption mode) or **extract hidden data out** (with decryption mode).
- The `output` is either (encryption mode) a **new image** with the hidden message encrypted in it OR (decryption mode) a **text file** containing the encrypted message hidden in the given base_image.
- Finally, the `message`, **ONLY** with the `encryption` mode. This is the message you want to encrypt in the given base_image.



