#!/usr/bin/env python
from PIL import Image, ImageDraw

colour = (0,0,0,128)

im = Image.new('RGBA',(256, 256))

draw = ImageDraw.Draw(im)
draw.line((0, 0) + im.size, fill=colour)
draw.line((0, im.size[1], im.size[0], 0), fill=colour)

draw.rectangle((0,0,im.size[0]-1,im.size[1]-1), fill=None, outline=colour)


im.save('placeholder.png', 'PNG')

