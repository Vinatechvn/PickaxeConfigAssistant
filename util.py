import random
import os
def mkdir(path):
	try:
		os.mkdir(path)
	except:
		pass

def random_string(size, chars="abcdef"):
	return ''.join(random.choice(chars) for x in range(size))



#
#	Read a file
def read_file(file_path):
	with open(file_path, "r") as f:
		return f.read()
#
#	Write a file
def write_file(file_path, content):
	with open(file_path, "w") as f:
		f.write(content)
		return True
