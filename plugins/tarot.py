from abc import *

import plugins.resources
from plugins import tools, resources
import random


class Deck(object):
    __major = []
    __minor = []

    def __init__(self, shuffled=False, lang="jp",
                 imageset=resources.tarot_waite, backimage=resources.tarot_back, keywords=plugins.resources.load_keywords()):

        self.__major = [
            MajorArcana(n, en, jp, shuffled and tools.true_or_false(), imageset, backimage, keywords[str(n)], lang)
            for n, en, jp in resources.major_arcana.cards
        ]
        self.__minor = [
            MinorArcana(s, n, shuffled and tools.true_or_false(), imageset, backimage, None, lang)
            for s, n in resources.minor_arcana.cards
        ]
        if shuffled:
            random.shuffle(self.__major)
            random.shuffle(self.__minor)

    @property
    def major_arcanas(self):
        return self.__major

    @property
    def minor_arcanas(self):
        return self.__minor

    def draw_cards(self, arcana, count):
        return [self.draw_one(arcana) for n in range(count) if len(arcana) > 0]

    def draw_one(self, arcana):
        return arcana.pop(0) if len(arcana) > 0 else None

    def pick_by_names(self, arcana, names):
        def no_the(name):
            return name.replace("The ", "")
        def patterns(name):
            return [name] + list(set(
                [ x for n in name.values()
                    for x in [n, n.upper(), n.lower(), no_the(n), no_the(n).upper(), no_the(n).lower()]]))
        cards = [ a for a in arcana for name in names if name in patterns(a.name) ]
        for card in cards:
            arcana.remove(card)
        return cards

class Tarot(object, metaclass=ABCMeta):
    image_size = 85, 140
    __image      = None
    __back_image = None
    __name       = None
    __suit       = None
    __number     = None
    __reversed   = None
    __keywords   = None
    __lang       = None

    def __init__(self, name, suit, number, reversed, image, back_image, keywords, lang):
        self.__name       = name
        self.__suit       = suit
        self.__number     = number
        self.__reversed   = reversed
        self.__image      = image
        self.__back_image = back_image
        self.__keywords   = keywords
        self.__lang       = lang

    @property
    def lang(self):
        return self.__lang

    @property
    def name(self):
        return self.__name

    @property
    def suit(self):
        return self.__suit

    @property
    def number(self):
        return self.__number

    @property
    def roman(self):
        return tools.arabic_to_roman(self.number)

    @property
    def reversed(self):
        return self.__reversed

    @property
    def keywords(self):
        return self.get_keywords(self.__reversed)

    def get_keywords(self, reversed):
        if self.__keywords:
            return "、".join(
                self.__keywords["reversed"]["keywords"] if reversed else self.__keywords["normal"]["keywords"])
        return None

    @property
    def image(self):
        return self.__image

    @property
    def back(self):
        return self.__back_image

    @property
    def info(self):
        return self.get_info("")

    @property
    def info_rows(self):
        return self.get_info("\n")

    @property
    def position(self):
        return resources.position.reversed[self.lang] if self.reversed else resources.position.normal[self.lang]

    def get_info(self, delimiter):
        return "{0}{2}({1})".format(self.display_name, self.position, delimiter)

    @property
    @abstractmethod
    def display_name(self):
        raise NotImplementedError

class MajorArcana(Tarot):

    def __init__(self, number, name, japanese_name, reversed, imageset, backimage, keywords, lang):
        w, h = super().image_size
        x, y = number % 11 * w, number // 11 * h
        img = imageset.crop((x, y, x+w, y+h))
        img = img.rotate(180) if reversed else img
        super().__init__({"en":name, "jp":japanese_name}, None, number, reversed, img, backimage, keywords, lang)

    @property
    def display_name(self):
        return "{0} {1}".format(self.roman, self.name[self.lang])


class MinorArcana(Tarot):

    def __init__(self, suit, number_or_name, reversed, imageset, backimage, keywords, lang):
        number = number_or_name if isinstance(number_or_name, int) and 0 < number_or_name < 11 else None
        __name = tools.number_to_name(number_or_name)
        name = {
            "en": "{0} of {1}".format(__name, suit),
            "jp": "{0}の{1}".format(
                resources.minor_arcana.jp_names.get(suit),
                resources.minor_arcana.jp_names.get(__name) or tools.to_zenkaku(str(number_or_name)))
        }
        n    = number or 11 + resources.minor_arcana.courts.index(__name)
        w, h = super().image_size
        x, y = (n - 1) * w, (2 + resources.minor_arcana.suits.index(suit)) * h
        img = imageset.crop((x, y, x+w, y+h))
        img = img.rotate(180) if reversed else img
        super().__init__(name, suit, number, reversed, img, backimage, keywords, lang)

    @property
    def display_name(self):
        return self.name[self.lang]

