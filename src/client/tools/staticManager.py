from os import listdir
from easydict import EasyDict as edict

base = "client/static/assets"
assetsPath = edict({
	file.split(".")[0]: f"{base}/{file}" for file in listdir(base)
})

base = "client/static/gifs"
gifsPath = edict({
	file.split(".")[0]: f"{base}/{file}" for file in listdir(base)
})

base = "client/static/fonts"
fontsPath = edict({
	file.split(".")[0]: f"{base}/{file}" for file in listdir(base)
})

base = "client/static/styles"
styles = edict({
	file.split(".")[0]: open(f"{base}/{file}").read() for file in listdir(base)
})