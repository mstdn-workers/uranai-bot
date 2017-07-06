from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from plugins import resources, tarot


def concat(image_list):
    widths, heights = zip(*( img.size for img in image_list))
    width  = sum(widths)
    height = max(heights)

    canvas = Image.new('RGBA', (width, height), (255,255,255,0))
    offset = 0
    for image in image_list:
        canvas.paste(image, (offset, 0))
        offset += image.size[0]
    return canvas

def margin(image, size):
    canvas = Image.new('RGBA', tuple([ o + m * 2 for o, m in zip(image.size, size) ]), (255, 255, 255, 0))
    canvas.paste(image, size)
    return canvas

def set_size(image, size):
    canvas = Image.new('RGBA', size, (255, 255, 255, 0))
    canvas.paste(image, tuple([ (c - o) // 2 for o, c in zip(image.size, size) ]))
    return canvas

def bgcolor(image, color):
    canvas = Image.new('RGBA', image.size, color)
    canvas = Image.alpha_composite(canvas, image)
    return canvas

def text_at_center(canvas, text, fontfile='materials/font.otf', fontsize=18):
    image_w, image_h = canvas.size[0] * 4, canvas.size[1] * 4
    image = Image.new('RGBA', (image_w, image_h), (255,255,255,0))
    draw  = ImageDraw.Draw(image)

    draw.font = ImageFont.truetype(fontfile, fontsize * 4)
    lines = text.splitlines()
    ws, hs = [s for s in zip(*[draw.font.getsize(line) for line in lines])]
    text_w, text_h = max(ws), sum(hs)

    for row,line in enumerate(lines):
        position = (image_w - ws[row])/2, (image_h - text_h)/2 + hs[row] * row
        draw.text(position, line, (0, 0, 0, 255))

    img = image.resize((image_w//4, image_h//4), Image.ANTIALIAS)
    canvas.paste(img, (0,0))
    return canvas


def dropshadow(image, border=5):
    img = ImageOps.invert(image.split()[3]).convert("RGBA")
    img = margin(img, (border, border))
    for n in range(3):
        img = img.filter(ImageFilter.BLUR)
    img = Image.alpha_composite(img, margin(image, (border,border)))
    return img

def create_single_tarot_image(card, text=None):
    fontsize = 18 if isinstance(card, tarot.MinorArcana) else 16
    image = concat([resources.tarot_blank, resources.tarot_blank])
    image = text_at_center(image, text or card.info_rows, fontsize=fontsize)
    image = set_size(image, (160, 150))
    image = concat([dropshadow(card.image), image])
    image = bgcolor(set_size(image, resources.canvas_size), resources.bg_color)
    return image

def create_triple_tarot_image(cards):
    image = dropshadow(concat([card.image for card in cards]))
    image = bgcolor(set_size(image, resources.canvas_size), resources.bg_color)
    return image


