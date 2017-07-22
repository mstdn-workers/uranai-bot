import os.path


def read_token():
    token_file = ".token"
    token = ""
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            token = f.read()
    return token.strip()

API_TOKEN = read_token()
DEFAULT_REPLY = "tarot で占ってさし上げるわ"
ERRORS_TO = 'uranai-bot-test'
PLUGINS = ['plugins']

CHANNEL_GENERAL = "C54RD0EPK"
CHANNEL_TAROT   = "C5Z31THK4"
CHANNEL_POKER   = "C5Y9W8SBA"
CAHNNEL_TEST    = "G661VTB45"

