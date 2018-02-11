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
#
#	Delete a directory and all of its contents
def remove_directory(directory_path):
	for file in os.listdir(directory_path):
		file_path = os.path.join(directory_path, file)
		if os.path.isfile(file_path):
			os.remove(file_path)
			#print(file_path)
	os.rmdir(directory_path)
	#print(directory_path)
