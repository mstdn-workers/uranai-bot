from datetime import datetime, timedelta

__cache = {
    "uranai": []
}


def delete_old(key, message, **kwargs):
    threshold = datetime.now() + timedelta(**kwargs)
    __cache[key] = [c for c in __cache[key] if datetime.fromtimestamp(float(c["ts"])) > threshold]

def add(key, message, data):
    delete_old(key, message, minutes=-5)
    __cache[key].append({ "user": message.body["user"], "ts": message.body["ts"], "data": data })

def get(key, message):
    delete_old(key, message, minutes=-5)
    data = [c for c in __cache[key] if c["user"] == message.body["user"]]
    if data:
        __cache[key].remove(data[0])
        return data[0]["data"]
    return None
