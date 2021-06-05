'''
    Author      : Sharath Sunil

    Description : A simple script /console application to hide encrypted text data within images.

    Year        : 2021

    Version     : 1.1

    References:
    1)Teja Swaroop's Github -> https://github.com/teja156/imghide
    2)Edureka Youtube Video -> https://www.youtube.com/watch?v=xepNoHgNj0w
	3)https://medium.com/swlh/lsb-image-steganography-using-python-2bbbee2c69a2
'''

from pyfiglet import figlet_format
from PIL import Image,ImageColor
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from getpass import getpass
from random import choice
import numpy as np
import string

class AESEncryption:

	'''
        Encryption class encapsulates the methods for encrypting and decrypting data.
        mode	: AES_CBC(Cipher Block Chaining)
        IV		: Random 16 bytes string, which will be appended with the data !
		Key		: 256 bit key 
	'''
	def __init__(self):
		self.mode      = AES.MODE_CBC #cipher block chain is one of the primary block cipher modes !
		self.alphabets = string.ascii_letters+string.digits
		self.iv        =''.join(str(choice(self.alphabets)) for x in range(AES.block_size)).encode()


	'''
        The below function will apply padding for the message as long it is not a multiple of 16

        return	: padded message which is divisible by 16(len),bytes 

        params	: message
	'''
	def padding(self,data):
		pad = AES.block_size -len(data) %AES.block_size #calculate the pad then convert to bytes and multiply by pad length !
		return bytes([pad])*pad

	'''
        The below function will encrypt the plain text into a cipher text !

        return	: cipher text (hex)

        param	: message(plain text),key obtained from the image
    '''

	def encrypt_message(self, message:str ,key:str ):	
		key = SHA256.new(key.encode()).digest() #the 256 bit key !
		cipher = AES.new(key,self.mode,self.iv) #defining the AES cipher !
		padded_message = self.padding(message)
		cipher_text = cipher.encrypt(message.encode()+padded_message)
		return (self.iv+cipher_text).hex() #returning both the iv and message, so that we can later extract the iv from the message !
		


	'''
        The below function will decrypt the cipher text into a plain text !

        return	: plain text

        param	: cipher text ,key obtained from the image
    '''

	def decrypt_message(self, cipher_text:str ,key:str ):
		key = SHA256.new(key.encode()).digest()
		cipher_text = bytes.fromhex(cipher_text) #obtaining the bytestream from hex !
		iv = cipher_text[:AES.block_size] #extracting the iv 
		cipher = AES.new(key,self.mode,iv)
		plain_text = cipher.decrypt(cipher_text[AES.block_size:]) #obtaining the plain text !
		pad_val = plain_text[-1]  
		return plain_text[:pad_val].decode().strip() #omitting the pad value by removing the padding from the end !

class Steganography:
	def __init__(self):
		self.delimitter = '#f!@g*&' 										   #the prgm will stop when it encounters the flag !
		self.len_delimitter = len(self.delimitter)
	'''
		The function to encode the encrypted data to the image.
		return	: None 

		params	: image destination and the message 
	'''
	def encode_data(self, image_path:str ,new_path:str , message:str):
		image = Image.open(image_path,'r')
		image_size = image.size
		pix_array = np.array(list(image.getdata())) 				   # getting the numpy array !
		width,height = image_size									   #getting the image width and height !
		channels = 4 if image.mode=='RGBA' else 3
		PIXEL_VALS = pix_array.size//channels
		message += self.delimitter 										   #appending to the message 
		bin_message = ''.join([format(ord(i),'08b') for i in message]) # converting the message and flag to 8 bit binary !
		
		required_pixels = len(bin_message)

		if required_pixels > PIXEL_VALS:
			raise Exception('Not enough data to cover !\nNeed Larger File !!')
		else:
			curr = 0
			for i in range(PIXEL_VALS):
				for j in range(0,3): #three values !
					if curr < required_pixels:
						pix_array[i][j] = int(bin(pix_array[i,j])[2:9]+bin_message[curr],2) # converting to base 2
						curr += 1
			pix_array = pix_array.reshape(height,width,channels) #reshapting to width x height 
			new_image = Image.fromarray(pix_array.astype('uint8'),image.mode) #converting to image from array !
			new_image.save(new_path)
			print('Stego file saved to {}'.format(new_image.filename))
	def decode_data(self, stego_path:str ,new_path:str):
		image = Image.open(stego_path,'r')
		pix_array = np.array(list(image.getdata())) 				   # getting the numpy array !
		channels = 4 if image.mode=='RGBA' else 3
		PIXEL_VALS = pix_array.size//channels
		secret_bits =''
		for i in range(PIXEL_VALS):
			for j in (0,3):
				secret_bits += (bin(pix_array[i][j])[2:][-1])
		secret_bits = [secret_bits[i:i+8] for i in range(0,len(secret_bits),8)] # extracting 8its in groups of 8
		message = ''
		for i in range(len(secret_bits)):
			if message[-self.len_delimitter:]==self.delimitter:
				break
			else:
				message += chr(int(secret_bits[i],2))
		print(self.delimitter)
		print('The secret message is {}'.format(message[:-5])) if self.delimitter in message else print('None !')
			
steg = Steganography()
#print(steg.encode_data('image.png','image1.png','Hey'))
steg.decode_data('image1.png','Ne')
