
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtGui import QImage

import random

def list_to_bar_image(lst, coloring, color_map = {0: 'white', 1: 'green', 2: 'orange'}, padding=0, size=400) -> QImage:
    image = Image.new('RGB', (size,size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    bar_width = (size / len(lst)) - padding - 1
    y_step_size = 400 / lst.max
    x = 1
    for num, color in zip(lst, coloring):
        draw.rectangle((x,size, x + bar_width, size-y_step_size*num), fill= color_map[color])
        x += bar_width + padding + 1

    return QImage(image.tobytes("raw","RGB"), image.size[0], image.size[1], QImage.Format_RGB888)

