import requests
import slackbot_settings
import io
import os.path
from PIL import Image

def filename_to_filetype(file_name):
    file_name = file_name or 'sample.png'
    root, ext = os.path.splitext(file_name)
    file_type = ext[1:] if ext else 'png'
    return file_type if file_type != 'jpg' else 'jpeg'


def post_image(message, pillow_image, title=None, comment=None, file_name=None):
    output = io.BytesIO()
    pillow_image.save(output, filename_to_filetype(file_name))
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

    canvas = Image.new('RGB', (width, height))
    offset = 0
    for image in image_list:
        canvas.paste(image, (offset, 0))
        offset += image.size[0]
    return canvas