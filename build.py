import os, shutil
from distutils.dir_util import copy_tree

def tryer(doIt):
	try:
		doIt()
	except:
		pass

os.mkdir("./HGiger")
os.mkdir("./HGiger/client")
os.mkdir("./HGiger/client/static")
copy_tree("./client/static", "./HGiger/client/static")
os.mkdir("./HGiger/db")
copy_tree("./db", "./HGiger/db")
os.mkdir("./HGiger/modules")
os.mkdir("./HGiger/modules/hgigerbot")
shutil.copyfile("./modules/hgigerbot/config.json", "./HGiger/modules/hgigerbot/config.json")
tryer(lambda: shutil.move("./dist/main.exe", "./HGiger/main.exe"))
tryer(lambda: os.rename("./HGiger/main.exe", "./HGiger/HGiger.exe"))
tryer(lambda: shutil.rmtree("./build"))
tryer(lambda: os.rmdir("./dist"))
tryer(lambda: os.remove("./main.spec"))
tryer(lambda: shutil.rmtree("./__pycache__"))