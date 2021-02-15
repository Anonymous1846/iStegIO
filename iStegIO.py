'''
iStegIO is a simple python script/ application which is used to hide text messages or plain text within png images.
It usees LSB Steganography technique to hide the text within the images. Least Significant Bit Steganography method, replaces
the blue bits, with the text bits.
'''

import binascii
from PIL import Image,ImageColor
'''
The below function will take three int arguements and gives hex code for the corresponding color !
params:r,g,b color code (int)
return: hex code for color
'''
def rgb_to_hex(r,g,b):
	return '#{:02x}{:02x}{:02x}'.format(r,g,b)
'''
The below function will take a hex code and gives a tuple containing the rgb values(three len)
params:hex code for color !
return: rgb tuple
'''
def hex_to_rgb(hexcode):
	#using the getcolor method we got the rgb tuple !
	return ImageColor.getcolor(hexcode,"RGB")
'''
We first convert the string message into hexadecimal and then into binary 
params: string message
return: binary representation of the message
'''
def string_to_binary(string):
	#the output will be 0b01100100010010
	#we have to translate the binary to 01100100010010 
	binary=bin(int(binascii.hexlify(string.encode()),16)).replace('0b','')
	return binary
'''
The below funcition will convert the binary format into corresponding byte strem message 
params: binary
return : byte stream message !
'''
def binary_to_string(binary):
	# we first convert the binary to hex and then into string !
	#each hex bit is translated into int base 2 and then to string
	#we get the byte stream of the message !
	return binascii.unhexlify('%x' % int('0b'+binary,2))

def hide(filename,message):
	pass
def extract(filename):
	pass
