
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtGui import QImage

import random

def list_to_bar_image(lst, size=400) -> QImage:
    image = Image.new('RGB', (size,size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    bar_width = size / len(lst)
    y_step_size = 400 / lst.max
    x = 0
    for num in lst:
        draw.rectangle((x,size, x + bar_width, size-y_step_size*num), fill= 'white')
        x += bar_width

    #font = ImageFont.truetype("assets/ARIALBD.TTF", 30)  

    #draw.text((200,200), str("Test"), font=font)

    # Resize oversized image back to get antialiasing
    image = image.resize((size, size),resample=Image.ANTIALIAS)

    return QImage(image.tobytes("raw","RGB"), image.size[0], image.size[1], QImage.Format_RGB888)