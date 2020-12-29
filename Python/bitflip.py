import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
from binascii import unhexlify

key = get_random_bytes(16)
iv = get_random_bytes(16)


def encrypt_data(data):
	padded = pad(data.encode(),16,style='pkcs7')
	cipher = AES.new(key, AES.MODE_CBC,iv)
	enc = cipher.encrypt(padded)
	return enc.hex()

def decrypt_data(data):
	cipher = AES.new(key, AES.MODE_CBC,iv)
	padded = cipher.decrypt( unhexlify(data))
	print(padded)
	if b'y0ush4LIn0Tp45S' in unpad(padded,16,style='pkcs7'):
		return 1
	else:
		return 0

def main():
	msg = input("Your plaintext:")
	try:
		assert('y0ush4LIn0Tp45S' not in msg)
	except AssertionError:
		print('Not like this ...')
		raise
	print("Your ciphertext:" + encrypt_data(msg) + "\n")
	enc_msg = input("Enter ciphertext: ")
	try:
		check = decrypt_data(enc_msg)
		if check:
			print(" (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ Congratulations ! ٩(◕‿◕)۶")
		else:
			print(" ┐( ˘_˘ )┌ Try again ...  ᕕ( ᐛ )ᕗ")
	except Exception as e:
		print(e)
	
if __name__ == '__main__':
	while(True):
		try:
			main()
		except:
			pass
		m = input("quit (y/n):")
		if m == 'y':
			break