from datetime import datetime, timedelta

__cache = {
    "uranai": []
}


def delete_old(key, message, **kwargs):
    threshold = datetime.fromtimestamp(float(message.body["ts"])) + timedelta(**kwargs)
    __cache[key] = [c for c in __cache[key] if datetime.fromtimestamp(float(c["ts"])) > threshold]

def delete_user(key, message):
    __cache[key] = [c for c in __cache[key] if c["user"] != message.body["user"] ]

def add(key, message, data):
    delete_old(key, message, minutes=-5)
    __cache[key].append({ "user": message.body["user"], "ts": message.body["ts"], "data": data })

def get(key, message):
    delete_old(key, message, minutes=-5)
    data = [c for c in __cache[key] if c["user"] == message.body["user"]]
    if data:
        delete_user(key, message)
        return data[0]["data"]
    return None
