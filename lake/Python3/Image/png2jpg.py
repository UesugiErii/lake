# Use Python3 convert png to jpg

from PIL import Image

im = Image.open("1.png")
rgb_im = im.convert('RGB')
rgb_im.save('DBSCAN.jpg')
