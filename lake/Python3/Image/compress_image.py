# Use Python3 compress jpg image

# if you want to compress png image, you should first covert png to jpg

from PIL import Image

foo = Image.open("2.jpg")

foo = foo.resize(foo.size, Image.ANTIALIAS)  # change size or not

foo.save("3.jpg", optimize=True, quality=70)
