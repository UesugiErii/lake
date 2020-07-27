# Use Python3 compress jpg image

# if you want to compress png image, you should first covert png to jpg

from PIL import Image

foo = Image.open("1.jpg")

foo = foo.resize(foo.size, Image.ANTIALIAS)  # change size or not

quality = 50
foo.save("1_{}.jpg".format(quality), optimize=True, quality=quality)
