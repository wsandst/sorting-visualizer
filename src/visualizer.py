
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtGui import QImage

import random, math

def list_to_bar_image(lst, coloring, padding=0, size=400, color_map = {0: (255, 255, 255), 1: (0, 130, 22), 2: 'orange', 3: 'gold'}) -> QImage:
    image = Image.new('RGB', (size,size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    if (size / len(lst)) < (padding+1): # This padding is not possible
        padding = 0

    skip_index = 1
    # Calculate if skipping optimization is needed
    if (size * 2) < len(lst):
        skip_index = math.floor(len(lst)/size)

    default_color = color_map[coloring[-1]]
    coloring.pop(-1) 

    bar_width = (size / len(lst)) - padding
    y_step_size = size / lst.max
    x = 1

    # Render the numbers as rectangles. Skip non-visible rectangles when element count exceeds pixel size
    for i in range(0, len(lst), skip_index):
        num = lst.getitem_no_count(i)
        draw.rectangle((x,size, x + bar_width*skip_index, size-y_step_size*num), fill= default_color)
        x += bar_width*skip_index + padding

    # Draw custom coloring ontop
    for i, color in coloring.items():
        num = lst.getitem_no_count(i)
        x = i*(bar_width+padding)+1
        draw.rectangle((x,size, x + bar_width * skip_index, size-y_step_size*num), fill= color_map[color])

    return QImage(image.tobytes("raw","RGB"), image.size[0], image.size[1], QImage.Format_RGB888)

