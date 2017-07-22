import io
import os.path
import re
import requests
import slackbot_settings
from slacker import Slacker

slackapi = Slacker(slackbot_settings.API_TOKEN)

def get_user(user_id):
    response = slackapi.users.info(user_id)
    return response.body["user"]

def get_channel(channel_id):
    response = slackapi.channels.info(channel_id)
    return response.body["channel"]

def get_user_mame(user_id):
    emoji = re.compile(r":.+?:")
    user = get_user(user_id)
    return emoji.sub('', user["profile"]["real_name"])

def get_channel_name(channel_id):
    channel = get_channel(channel_id)
    return channel["name"]

def post_image(message, pillow_image, title=None, comment=None, file_name=None):
    def filename_to_filetype(file_name):
        root, ext = os.path.splitext(file_name or 'sample.png')
        file_type = ext[1:] if ext else 'png'
        return file_type if file_type != 'jpg' else 'jpeg'

    output  = io.BytesIO()
    pillow_image.save(output, filename_to_filetype(file_name), quality=100)
    data = {
        'filename': file_name,
        'title': title,
        'initial_comment': comment,
        'channels': message.body['channel']
    }
    files = {
        "file": output.getvalue()
    }
    slackapi.files.post('files.upload', data=data, files=files)

