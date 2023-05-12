import sys
from yeelight import Bulb
print(sys.argv[1]) 
bulb = Bulb(sys.argv[1])
bulb.turn_on()
bulb.set_brightness(100)

from PIL import Image, ImageGrab

bulb.start_music(port=0, ip=None)

while True:
    original = ImageGrab.grab(bbox = None)
    reduced = original.convert("P", palette=Image.ADAPTIVE, colors = 4) # convert to web palette (216 colors)
    palette = reduced.getpalette() # get palette as [r,g,b,r,g,b,...]
    palette = [palette[3*n:3*n+3] for n in range(256)] # group 3 by 3 = [[r,g,b],[r,g,b],...]
    color_count = [(n, palette[m]) for n,m in reduced.getcolors()]
    soglia = 40
    while True:
        try:
            m = max(color_count)
        except ValueError:
            m = (None, [255,255,255])
            break
        if any([True if (m[1][0]-i) > soglia else False for i in m[1]]):
            break
        if any([True if (m[1][1]-i) > soglia else False for i in m[1]]):
            break    
        if any([True if (m[1][2]-i) > soglia else False for i in m[1]]):
            break
        color_count.remove(m)
    print(m)
    bulb.set_rgb(m[1][0], m[1][1], m[1][2])


#40 di differenza
