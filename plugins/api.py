import io
import os.path
import re
import slackbot_settings
from slacker import Slacker
from requests import ReadTimeout


slackapi = Slacker(slackbot_settings.API_TOKEN)

users = {}

def get_user(user_id):
    if user_id not in users:
        response = slackapi.users.info(user_id)
        users[user_id] = response.body["user"]
    return users[user_id]

def get_channel(channel_id):
    response = slackapi.channels.info(channel_id)
    return response.body["channel"]

def get_message(channel_id, ts):
    latest = str(float(ts) + 0.000001)
    oldest = str(float(ts) - 0.000001)
    response = slackapi.channels.history(channel=channel_id, latest=latest, oldest=oldest, count=1)
    if response.body["messages"]:
        return response.body["messages"][0]
    return None

def get_user_mame(user_id):
    emoji = re.compile(r":.+?:")
    user = get_user(user_id)
    return emoji.sub('', user["profile"]["real_name"])

def get_channel_name(channel_id):
    channel = get_channel(channel_id)
    return channel["name"]

def get_channel_tag(channel_id):
    return "<#{0}|{1}>".format(channel_id, get_channel_name(channel_id))

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
    try:
        slackapi.files.post('files.upload', data=data, files=files)
    except ReadTimeout as e:
        message.send("slackの調子が少し悪いみたいですね...")


