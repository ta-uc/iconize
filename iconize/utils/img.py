from PIL import Image, ImageDraw, ImageFont
import unicodedata

import os
dirc = os.path.dirname(os.path.abspath(__file__))
s = (1024, 1024)
c = (255, 255, 255, 0)
f = ImageFont.truetype(dirc+'/font/NotoSansMonoCJKjp-Bold.otf', 460)
m = 'RGBA'
x = 55
y = -110

def strByteCount(text):
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            return 2
        else:
            return 1


def createImg(txt, size=512, color=(0, 0, 0, 255)):
    slist = list(txt)
    byte = 0
    for i in range(len(txt)):
        byte += strByteCount(slist[i])
        if byte > 8:
            slist = slist[:i+1]
            break
        if byte == 4 or (byte == 3 and len(txt) > 3 and strByteCount(slist[i+1]) == 2):
            slist.insert(i+1, "\n")
    new_txt = ''.join(slist)
    img = Image.new(m, s, c)
    draw = ImageDraw.Draw(img)
    if color == "#FFF":
        draw.text((x-7, y), new_txt, spacing=-40, fill=(0,0,0), font=f)
        draw.text((x+7, y), new_txt, spacing=-40, fill=(0,0,0), font=f)
        draw.text((x, y-7), new_txt, spacing=-40, fill=(0,0,0), font=f)
        draw.text((x, y+7), new_txt, spacing=-40, fill=(0,0,0), font=f)
        draw.text((x-7, y-7), new_txt, spacing=-40, fill=(0,0,0), font=f)
        draw.text((x+7, y-7), new_txt, spacing=-40, fill=(0,0,0), font=f)
        draw.text((x-7, y+7), new_txt, spacing=-40, fill=(0,0,0), font=f)
        draw.text((x+7, y+7), new_txt, spacing=-40, fill=(0,0,0), font=f)
    draw.text((x, y), new_txt, spacing=-40, fill=color, font=f)
    # draw.multiline_text((55, -110), new_txt, spacing=-40, fill=color, font=f)
    resizedimg = img.resize((size, size), Image.ANTIALIAS)
    return resizedimg


def make512(img):
    icon = Image.open(img)
    icon512 = icon.resize((512, 512), Image.ANTIALIAS)
    return icon512


if __name__ == "__main__":
    img = createImg('あいうえおかき', size=512, color="#123456")
    img.show()
