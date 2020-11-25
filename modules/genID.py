import string, random

def genID(length):
	return ''.join(random.choice(string.ascii_letters + string.punctuation + string.digits) for i in range(length))