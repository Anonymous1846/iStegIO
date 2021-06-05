'''
    Author      : Sharath Sunil

    Description : A simple script /console application to hide encrypted text data within images.

    Year        : 2021

    Version     : 1.1

    References:
    1)Teja Swaroop's Github -> https://github.com/teja156/imghide
    2)Edureka Youtube Video -> https://www.youtube.com/watch?v=xepNoHgNj0w
'''

from pyfiglet import figlet_format
from PIL import Image,ImageColor
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from getpass import getpass
from random import choice
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
	
	def getData(data):
		bin_list=[]
		for i in data:
			bin_list.append(format(i,ord('08b')))
		print(bin_list)

steg = Steganography()
steg.getData()
