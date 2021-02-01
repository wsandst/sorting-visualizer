
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtGui import QImage

import random

def list_to_bar_image(lst, coloring, padding=0, size=400, color_map = {0: 'white', 1: 'green', 2: 'orange', 3: 'gold'}) -> QImage:
    image = Image.new('RGB', (size,size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    if (size / len(lst)) < 1:
        padding = 0
    bar_width = (size / len(lst)) - padding - 1
    y_step_size = size / lst.max
    x = 1
    start_skipping = (size * 2) < len(lst)
    skip_index = int(len(lst)/size)
    for i, (num, color) in enumerate(zip(lst, coloring)):
        # Optimization to skip non visible rectangles
        if not start_skipping or (i % skip_index) == 0: 
            draw.rectangle((x,size, x + bar_width, size-y_step_size*num), fill= color_map[color])
        x += bar_width + padding + 1

    return QImage(image.tobytes("raw","RGB"), image.size[0], image.size[1], QImage.Format_RGB888)

