import io
import os.path
import re
import requests
import slackbot_settings


def get_username(user_id):
    emoji = re.compile(r":.+?:")
    params = {
        'token' : slackbot_settings.API_TOKEN,
        'user'  : user_id
    }
    res  = requests.post('https://slack.com/api/users.profile.get', data=params)
    user = res.json()["profile"]
    first, last = user["first_name"], user["last_name"]
    last = emoji.sub('', last)
    return " ".join([first, last]) if last else first


def post_image(message, pillow_image, title=None, comment=None, file_name=None):
    output = io.BytesIO()
    pillow_image.save(output, filename_to_filetype(file_name), quality=100)
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


def filename_to_filetype(file_name):
    file_name = file_name or 'sample.png'
    root, ext = os.path.splitext(file_name)
    file_type = ext[1:] if ext else 'png'
    return file_type if file_type != 'jpg' else 'jpeg'