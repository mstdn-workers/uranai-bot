from datetime import datetime, timedelta
import os, os.path
import json

__cache = {
    "uranai": [],
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


def save_cache(key, data):
    if not os.path.exists("cache"):
        os.makedirs("cache")
    with open("cache/" + key, 'w') as f:
        json.dump(data, f, ensure_ascii=False)

def load_cache(key):
    if not os.path.exists("cache/" + key) :
        return []
    with open("cache/" + key, 'r') as f:
        data = json.load(f)
    return data

def only_today(data, message):
    now  = datetime.fromtimestamp(float(message.body["ts"]))
    zero = datetime(now.year, now.month, now.day, 0, 0, 0)
    return [d for d in data if datetime.fromtimestamp(float(d["ts"])) >= zero]

def add_ranking(key, message, point, data):
    cache = only_today(load_cache(key), message)
    users_data = [d for d in cache if d["user"] == message.body["user"]]
    if users_data and users_data[0]["point"] > point:
        return
    cache = [d for d in cache if d["user"] != message.body["user"]]
    cache.append({"user": message.body["user"], "point": point, "ts": message.body["ts"], "data": data})
    save_cache(key, cache)

def get_ranking(key, message):
    return only_today(load_cache(key), message)

