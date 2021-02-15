'''
iStegIO is a simple python script/ application which is used to hide text messages or plain text within png images.
It usees LSB Steganography technique to hide the text within the images. Least Significant Bit Steganography method, replaces
the blue bits, with the text bits.
'''
from tkinter import filedialog as f
from pyfiglet import figlet_format
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
	return binascii.unhexlify('%x' % (int('0b'+binary,2)))
'''
If end of the hex code is ether 0 or 1, then return the last part of the hexcode
params: hexcode
return: last hex
'''
def decrypt(hexcode):
	if hexcode[-1] in [0,1]:
		return hexcode[-1]
	else:return None
def encrypt(hexcode,digit):
	if hexcode[-1] in ['0','1','2','3','4','5']:
		hexcode=hexcode[:-1]+digit
		return hexcode
	else:return None
'''
We'll use all the helper function above to hide the message string within the photo
'''
def hide(filename,message,out):
	image =Image.open(filename)
	#convert the message to binary and append 15 ones and one zero !
	binary=string_to_binary(message)+'1111111111111110'
	if image.mode in ('RGBA'):
		image =image.convert('RGBA')
		#getting the data from the image !
		img_data=image.getdata()
		#the text and the image will appended here !
		enc_data=[]
		#the current bin digit we are working on !
		digit = 0
		for i in img_data:
			if (digit < len(binary)):
				#reference made to the rgb_to_hex function to convert the rgb tuple to the hexadecimal and encode to check whether it lies in the 0 to 5 hex range  !
				new_data=encrypt(rgb_to_hex(i[0],i[1],i[2]),binary[digit])
				#if it lies there we get a non None value!
				if new_data is None:
					enc_data.append(new_data)
				else:
					r,g,b=hex_to_rgb(new_data)
					#using the rgba format !
					enc_data.append((r,g,b,255))
					digit+=1
			else:
				enc_data.append(i)
		image.putdata(enc_data)
		image.save(out+".png","PNG")
		print('Completed !')
	return "Invalid Format !!"
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
				binary+=digit
				#checking for the delimiter !
				if binary[-16:] =='1111111111111110':
					print('We got it !')
					#now just have to convert the binary to string upto the delimiter !
					return binary_to_string(binary[:-16])
		#else do normal conversion !
		return binary_to_string(binary)
	return "Invalid Image Mode !"

#-----------------------------End of the Implementation --------------------------------#

if __name__=='__main__':
	heading = figlet_format('i S t e g I O')
	print(heading)
	print('VERSION 1.0')
	print(*65*('-'))
	while True:
		choice = int(input('1)Encrypt\n2)Decrypt\n3)Exit'))
		if choice == 1:
			image = f.askopenfile()
			mess=input('Enter the message !')
			out=input('Output File name')
			hide(image,mess,out)
		elif choice == 2:
#			image =f.askopenfilename()
#			extract(image)
			print(binary_to_string('10101010101010'))
		elif choice == 3:
			print('Exiting.........')
			break
		else:print('Invalid !')
