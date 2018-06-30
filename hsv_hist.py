import matplotlib.pyplot as plt
import numpy as np
import os
import colorsys

from PIL import Image


path = '/home/andrey/Pictures/aerodventure/'

orig = Image.open(os.path.join(path, 'original.jpg'))
orig = orig.convert("RGB")
data = np.array(orig.getdata())

fig = plt.figure()
ax = fig.add_subplot(111)

hist = np.zeros(360)


for pixel in data[::50]:
    R = pixel[0]/255.0
    G = pixel[1]/255.0
    B = pixel[2]/255.0

    H, S, V = colorsys.rgb_to_hsv(R, G, B)
    #import ipdb
    #ipdb.set_trace()
    if S > 0:
        hist[int(H * 359.0)] += 1

for hue, val in enumerate(hist):
    R, G, B = colorsys.hsv_to_rgb(hue/360.0, 1, 255)
    ax.scatter(hue, val, s=5, c=(R/255.0, G/255.0, B/255.0))

print("Max at hue %s" % str(hist.argmax()))

plt.show()