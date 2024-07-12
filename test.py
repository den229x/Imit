import png

i = png.PNG_img("pngwing.com.png")

print(i.info())

i.rresize(100, 100)

print(i.info())
