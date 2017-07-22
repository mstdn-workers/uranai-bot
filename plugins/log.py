import os.path
from datetime import datetime
from plugins import api, mode

def write(message):
    if not mode.debug:
        return

    log = [
        "{0:%Y-%m-%d %H:%M:%S}".format(datetime.fromtimestamp(float(message.body["ts"]))),
        message.body["channel"],
        "[{0}]: {1}".format(api.get_user_mame(message.body["user"]), message.body["text"])
    ]
    if not os.path.exists("logs"):
        os.makedirs("logs")
    with open("logs/message.log", 'a') as f:
        f.write("\t".join(log) + "\n")

