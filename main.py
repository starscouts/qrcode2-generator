from PIL import Image
import sys
from math import ceil
from textwrap import wrap


img = Image.open("./base.png")
img_pixels = img.load()
text = sys.argv[1]

colors = {
    '000': (0, 0, 0),
    '001': (255, 255, 255),
    '010': (255, 0, 0),
    '011': (255, 255, 0),
    '100': (0, 0, 255),
    '101': (0, 255, 0),
    '110': (0, 255, 255),
    '111': (255, 0, 255)
}

print(f"Encoding \"{text}\"")

binary = ''.join(format(ord(x), 'b') for x in text)

if len(binary) % 3 == 1:
    binary = "00" + binary

if len(binary) % 3 == 2:
    binary = "0" + binary

print(f"  --> {len(binary)} bits")
print(f"      {ceil(len(binary) / 4)} bytes")
print(f"      {ceil(len(binary) / 3)} pixels")

if ceil(len(binary) / 4) > 700:
    print(f"  --> <!> Sorry, the input data is too long, it needs to be 700 bytes or less")
    sys.exit()
else:
    print(f"  --> Using {round((ceil(len(binary) / 4) / 702) * 100)}% of space")
    print(f"      Using {round(((702 - ceil(len(binary) / 4)) / 702) * 100)}% error correction")

chunks = wrap(binary, 3)
pixels = []

for chunk in chunks:
    pixels.append(colors[chunk])

pixels_full = []
pixels_full += pixels

while len(pixels_full) + len(pixels) + 3 < 1872:
    pixels_full += [(255, 0, 255), (255, 0, 255), (255, 0, 255)]
    pixels_full += pixels

x = 3
y = 3

for pixel in pixels_full:
    while (x >= 21 and y >= 21) and (x < 29 and y < 29):
        x += 1
        if x == 47:
            x = 3
            y += 1

    img_pixels[x, y] = pixel
    x += 1

    if x == 47:
        x = 3
        y += 1


img.save("output.png", format="png")
print("Saved to output.png")