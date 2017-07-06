import random


def true_or_false():
    return random.choice([True, False])

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

def number_to_name(number):
    names = {
        1: "Ace", 2: "Two",   3: "Three", 4: "Four",  5: "Five",
        6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"
    }
    return names.get(number) or str(number)

def to_zenkaku(name):
    """
    http://cuio.blog2.fc2.com/blog-entry-2165.html
    """
    t = dict((0x0020 + ch, 0xff00 + ch) for ch in range(0x5f))
    t[0x0020] = 0x3000
    return name.translate(t)