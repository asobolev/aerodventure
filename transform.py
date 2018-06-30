import numpy as np
import os
import colorsys
import math

from PIL import Image


def html_to_rgb(color):
    """
    Converts HTML (e.g. E3DBC3) to RGB triple (e.g. (227, 219, 195))

    :param color:   HTML code as string
    :return:        RGB triple (3 ints)
    """
    if color[0] == '#':
        color = color[1:]

    r, g, b = color[:2], color[2:4], color[4:]
    return int(r, 16), int(g, 16), int(b, 16)


path = '/home/andrey/Pictures/aerodventure/'

orig = Image.open(os.path.join(path, 'original.png'))
data = orig.getdata()

#do_ignore = lambda hue: ignore_hue_range[0] / 255 < hue < ignore_hue_range[1] / 255
step = len(data) / 10
boost = 0.3

# red, yellow, kind of white, light blue
ranges = [(5, 21), (35, 50), (61, 60), (170, 200)]
to_colors = ['ef767a', '456990', 'f49d37', '49beaa']
#shifts = [300, 50, 0, 50]

result = []
for i, pixel in enumerate(data):
    R, G, B, A = [x / 255.0 for x in pixel]
    H, S, V = colorsys.rgb_to_hsv(R, G, B)

    H1 = float(H)
    S1 = float(S)
    V1 = float(V)

    for j, range in enumerate(ranges):
        if range[0]/360. < H < range[1]/360. and S > 0.6:

            Ht, St, Vt = colorsys.rgb_to_hsv(*[x / 255.0 for x in html_to_rgb(to_colors[j])])

            shift_hue = Ht - H  # 0 < hue delta < 1
            shift_sat = St - S  # 0 < saturation delta < 1
            shift_val = Vt - V  # 0 < value delta < 1

            H1 = (H + shift_hue) % 1

            if not (S < 0.02 and V > 0.98):  # if not white
                if shift_sat < 0:  # desaturate
                    S1 = S + S * shift_sat
                else:  # saturate
                    S1 = S + (1 - S) * shift_sat

            if not (S < 0.02 and V > 0.98):  # if not white
                if shift_val < 0:  # darken
                    V1 = V + (boost * math.sin(S * 3.1415) + S) * V * shift_val
                else:  # colorize
                    V1 = V + (1 - V) * S * shift_val

    R1, G1, B1 = colorsys.hsv_to_rgb(H1, S1, V1)
    result.append((int(R1 * 255), int(G1 * 255), int(B1 * 255), int(A * 255)))

    # by saturation
    #if 40/360. < S < 70/360.:
    #    H1 = 60/360.
    #    S1 = 0.98
    #    V1 = 0.98

    if i % step == 0 and i != 0:
        percent = 10 * (i / step)
        print("%d percent done" % percent)

orig.putdata(result)
orig.save(os.path.join(path, 'new.png'))

