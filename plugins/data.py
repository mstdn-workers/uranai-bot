import json
import random


def load(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def true_or_false():
    return random.choice([True, False])

def load_keywords():
    return load('materials/keywords.json')