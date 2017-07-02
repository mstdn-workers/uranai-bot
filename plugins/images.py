import io
import os.path
import requests
import slackbot_settings
from PIL import Image, ImageDraw, ImageFont


def filename_to_filetype(file_name):
    file_name = file_name or 'sample.png'
    root, ext = os.path.splitext(file_name)
    file_type = ext[1:] if ext else 'png'
    return file_type if file_type != 'jpg' else 'jpeg'


def post(message, pillow_image, title=None, comment=None, file_name=None):
    output = io.BytesIO()
    pillow_image.save(output, filename_to_filetype(file_name),quality=100)
    params = {
        'token'           : slackbot_settings.API_TOKEN,
        'channels'        : message.channel._body['id'],
        'title'           : title,
        'initial_comment' : comment
    }
    file_object = {
        'file' : (file_name, output.getvalue())
    }
    requests.post('https://slack.com/api/files.upload', data=params, files=file_object)

def open_tarot_waite():
    return Image.open('materials/tarot-waite.png')

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
    canvas = Image.new('RGBA', tuple([s+size*2 for s in image.size]), (255, 255, 255, 0))
    canvas.paste(image, (size, size))
    return canvas

def back():
    return Image.open('materials/tarot-back.png')

def blank():
    return Image.new('RGBA', (85,140), (255,255,255,0))

def text_at_center(canvas, text, fontfile='materials/font.otf', fontsize=18):
    image_w, image_h = canvas.size[0] * 4, canvas.size[1] * 4
    image = Image.new('RGBA', (image_w, image_h))
    draw  = ImageDraw.Draw(image)

    draw.font = ImageFont.truetype(fontfile, fontsize * 4)
    lines = text.splitlines()
    ws, hs = [s for s in zip(*[draw.font.getsize(line) for line in lines])]
    text_w, text_h = max(ws), sum(hs)

    for row,line in enumerate(lines):
        position = (image_w - ws[row])/2, (image_h - text_h)/2 + hs[row] * row
        draw.text(position, line, (0, 0, 0, 255))

    canvas.paste(image.resize((image_w//4, image_h//4), Image.ANTIALIAS), (0, 0))
    return canvas




