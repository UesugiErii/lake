# convert pdf into a whole picture

# Will overwrite *.png(like 1.png, 2.png...) in the current directory
# vertical

from pdf2image import convert_from_path
import os
from PIL import Image

file_path = 'path.pdf'

pages = convert_from_path(file_path, dpi=300)

# for page in pages:
#     page.save('out.jpg', 'JPEG')

# pdf one page into one image
for i, page in enumerate(pages):
    page.save('{}.png'.format(i), 'PNG')

im = Image.open('0.png')

# image size
w, h = im.size

# Create blank image
result = Image.new(im.mode, (w, h * len(pages)))

# Stitch images and delete temporary images
for i in range(len(pages)):
    fn = '{}.png'.format(i)
    im = Image.open(fn)
    result.paste(im, box=(0, i * h))  # vertical
    os.remove(fn)

result.save('res.png')
