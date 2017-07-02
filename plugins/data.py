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

def arabic_to_roman(arabic):
    """
    Reference: https://stackoverflow.com/questions/33486183/convert-from-numbers-to-roman-notation
    """
    if not isinstance(arabic, int):
        return None
    if arabic == 0:
        return "O"
    conv = [[1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'],
            [ 100, 'C'], [ 90, 'XC'], [ 50, 'L'], [ 40, 'XL'],
            [  10, 'X'], [  9, 'IX'], [  5, 'V'], [  4, 'IV'],
            [   1, 'I']]
    result = ''
    for denom, roman_digit in conv:
        result += roman_digit*(arabic//denom)
        arabic %= denom
    return result
