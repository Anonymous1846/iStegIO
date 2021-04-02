'''
iStegIO is a simple python script/ application which is used to hide text messages or plain text within png images.
It usees LSB Steganography technique to hide the text within the images. Least Significant Bit Steganography method, replaces
the blue bits, with the text bits.
'''
from tkinter import filedialog as f,Tk  
from Crypto.Cipher import AES
from pyfiglet import figlet_format
import binascii
from PIL import Image,ImageColor
from getpass import getpass
from secrets import token_hex
import hashlib
class Encryption:
	def __init__(self):
		self.mode=AES.MODE_CBC #cipher block chain is one of the primary block cipher modes !
	'''
	The below function will create a random key each time
	return: decoded key 16 bytes
	params:None
	'''
	def generate_key(self):
		return token_hex(16)#generate a random key each time !

	'''
	The below function will apply padding for the message as long it is not a multiple of 16
	return: padded message which is divisible by 16(len)
	params:message
	'''
	def padding(self,data):
		while len(data) % 16!=0:
			data=data+" "
		return data
	'''
	The below function will encrypt the plain text into a cipher text !
	return:cipher text 
	param:message(plain text),key obtained from the image'''

	def encrypt_message(self,message,key,iv):
		cipher=AES.new(key.encode(),self.mode,'abcdefqwertyuiop'.encode())
		cipher_text=cipher.encrypt(message)
		return cipher_text.decode()
	'''
	The below function will decrypt the cipher text into a plain text !
	return:plain text
	param:cipher text ,key obtained from the image'''

	def decrypt_message(self,cipher_text,key):
		pass

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
	
	return ImageColor.getcolor(hexcode,"RGB")#using the getcolor method we got the rgb tuple !
'''
We first convert the string message into hexadecimal and then into binary 
params: string message
return: binary representation of the message
'''
def string_to_binary(string):	
	binary=bin(int(binascii.hexlify(string.encode()),16)).replace('0b','')#we have to translate the binary to 01100100010010 
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
	message= binascii.unhexlify('%x' % (int('0b'+ binary ,2))).decode()
	return message
'''	
If end of the hex code is ether 0 or 1, then return the last part of the hexcode
params: hexcode
return: last hex
'''
def decrypt(hexcode):
	if hexcode[-1] in ['0','1']:
		return hexcode[-1]
	else:return None
'''
if the hex value of the color falls within the range of 0-5, then we add the digit(binary !)
params: hexcode and the digit !
return:None if it is out of the range 0-5 otherwise hexcode with appended digits !
'''
def encrypt(hexcode,digit):
	if hexcode[-1] in ('0','1','2','3','4','5'):
		hexcode=hexcode[:-1]+digit
		return hexcode
	else:return None
'''
We'll use all the helper function above to hide the message string within the photo
params: the filename(namely the png photo in which we want to hide the data), message usually a text file or custom message, outputfile file(.png)
return: the encoded png file 
'''
def hide(filename,message,out):
	image =Image.open(filename)
	
	binary=string_to_binary(message)+'1111111111111110'#convert the message to binary and append 15 ones and one zero (delimiter)!
	if image.mode in ('RGBA'):
		image =image.convert('RGBA')
		
		img_data=image.getdata()#getting the data from the image !
		
		enc_data=[]#the text and the image will appended here !
		
		digit = 0
		for i in img_data:#the current bin digit we are working on !
			if (digit < len(binary)):
				#reference made to the rgb_to_hex function to convert the rgb tuple to the hexadecimal and encode to check whether it lies in the 0 to 5 hex range  !
				new_data=encrypt(rgb_to_hex(i[0],i[1],i[2]),binary[digit])
				#if it lies there we get a non None value!
				if new_data is None:
					enc_data.append(i)
				else:
					r,g,b=hex_to_rgb(new_data)
					enc_data.append((r,g,b,255))#using the rgba format !
					digit+=1
			else:
				enc_data.append(i)
		image.putdata(enc_data)
		image.save(out+".png","PNG")
		print('Completed !')
	return "Invalid Format !!"

'''
The below function will decode the message from the png stego object !
It does this by searching for the delimiter 1111111111111110
params:filename(stego object !)
return:the message file .txt
'''
def extract(filename):
	image =Image.open(filename)
	#the binary data, which is to be store, is initlized as null string 
	binary=''
	if image.mode in ('RGBA'):

		image=image.convert('RGBA')
		img_data=image.getdata()

		for i in img_data:
			#here we obtain the digit from which it is added to this image !
			digit = decrypt(rgb_to_hex(i[0],i[1],i[2]))

			if digit is None:
				pass

			else:
				binary=binary+digit
				#checking for the delimiter !
				if (binary[-16:] =='1111111111111110'):
					print('We got it !')
					#now just have to convert the binary to string upto the delimiter !
					return binary_to_string(binary[:-16])
		#else do normal conversion !
		return binary_to_string(binary)

	return "Invalid Image Mode !"

def write_to_file(data):
	output_file_name=f.asksaveasfilename(title='Save your secret message to ',filetypes=[('All Files', '*.*'), 
             			('Text Document', '*.txt')] )
	if '.txt' in output_file_name:
		output_file_name=output_file_name.replace('.txt','')#replace the .txt from the text file if it already exists !
	with open(output_file_name+'.txt','w') as tf:
		tf.write(data)
		print(f'Decoded data saved to {output_file_name} !')
		

#-----------------------------End of the Implementation --------------------------------#

if __name__=='__main__':

	heading = figlet_format('i S t e g I O')
	print(heading)
	print('VERSION 1.0')
	print(*70*('-'))
	encrypt=Encryption()
	
	while True:

		choice=int(input('1)Encode Message\n2)Decode Message\n3)Exit\n>>'))
		if choice==1:
			root=Tk()
			root.withdraw()
			image=f.askopenfilename()
			message=input('Enter the message or type !txt for choosing a text file :')#use the !txt flag for opening the text file other wise we type in the message !
			key=encrypt.generate_key()
			print(key)
			print(encrypt.encrypt_message('Hello',key,'qwertyuiopasdfgh'))	
		elif choice==2:
			pass
		elif choice==3:			
			print('Exiting........!')
			break

		else:
			print('Invalid choice !')
