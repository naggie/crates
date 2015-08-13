from PIL import Image, ImageDraw

im = Image.new('RGBA',(256, 256))

draw = ImageDraw.Draw(im)
draw.line((0, 0) + im.size, fill=(0,0,0,128))
draw.line((0, im.size[1], im.size[0], 0), fill=(0,0,0,128))


im.save('placeholder.png', 'PNG')

