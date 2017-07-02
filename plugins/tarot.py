from plugins import data, images
import random


class Deck(object):
    __major = []
    __minor = []

    def __init__(self, shuffled=False, imageset=None, backimage=None, keywords=None):
        if not imageset:
            imageset = images.open_tarot_waite()

        if not backimage:
            backimage = images.back()

        if not keywords:
            keywords = data.load_keywords()

        self.__major = [
            MajorArcana(n, en, jp, inverted=shuffled and data.true_or_false(),imageset=imageset, backimage=backimage, keywords=keywords[str(n)])
            for n, en, jp in MajorArcana.define()
        ]
        self.__minor = [
            MinorArcana(s, n, inverted=shuffled and data.true_or_false(), imageset=imageset, backimage=backimage)
            for s, n in MinorArcana.define()
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

    def pick(self, count, minor_arcana=False):
        arcana = self.__minor if minor_arcana else self.__major
        return [self.pick_one_from(arcana) for n in range(count) if len(arcana) > 0]

    def pick_one_from(self, arcana):
        return arcana.pop(0) if len(arcana) > 0 else None


class MajorArcana(object):
    __image    = None
    __back     = None
    __name     = None
    __number   = None
    __inverted = False
    __keywords = None

    def __init__(self, number, name, japanese_name=None, inverted=False, imageset=None, backimage=None, keywords=None):
        self.__number   = number
        self.__name     = {"en":name, "jp":japanese_name}
        self.__inverted = inverted

        w, h = 85, 140
        x, y = self.__number % 11 * w, self.__number // 11 * h
        self.__image = imageset.crop((x, y, x+w, y+h)).rotate(180) if inverted else imageset.crop((x, y, x+w, y+h))
        self.__back  = backimage

        self.__keywords = keywords

    @property
    def name(self):
        return self.__name

    @property
    def number(self):
        return self.__number

    @property
    def roman(self):
        return data.arabic_to_roman(self.__number)

    @property
    def inverted(self):
        return self.__inverted

    @property
    def image(self):
        return self.__image

    @property
    def back(self):
        return self.__back

    @property
    def info(self):
        return "{0} {1}({2})".format(self.roman, self.name["jp"], "逆位置" if self.inverted else "正位置")

    @property
    def keywords(self):
        if self.__keywords:
            return "、".join(self.__keywords["inverted"]["keywords"] if self.__inverted else self.__keywords["normal"]["keywords"])
        return None

    @classmethod
    def define(cls):
        return [
            (0, "The Fool", "愚者"),
            (1, "The Magician", "魔術師"),
            (2, "The High Priestess", "女教皇"),
            (3, "The Empress", "女帝"),
            (4, "The Emperor", "皇帝"),
            (5, "The Hierophant", "教皇"),
            (6, "The Lovers", "恋人"),
            (7, "The Chariot", "戦車"),
            (8, "Strength", "力"),
            (9, "The Hermit", "隠者"),
            (10, "Wheel of Fortune", "運命の輪"),
            (11, "Justice", "正義"),
            (12, "The Hanged Man", "吊された男"),
            (13, "Death", "死神"),
            (14, "Temperance", "節制"),
            (15, "The Devil", "悪魔"),
            (16, "The Tower", "塔"),
            (17, "The Star", "星"),
            (18, "The Moon", "月"),
            (19, "The Sun", "太陽"),
            (20, "Judgement", "審判"),
            (21, "The World", "世界")
        ]

class MinorArcana(object):
    __size     = (85, 140)
    __image    = None
    __back     = None
    __suit   = None
    __name = None
    __number = None
    __inverted = False

    def __init__(self, suit, number_or_name, inverted=False, imageset=None, backimage=None):
        self.__suit = suit

        if isinstance(number_or_name, int) and 0 < number_or_name < 11:
            self.__number = number_or_name

        name = "Ace" if number_or_name == 1 else number_or_name
        self.__name = {"en": name, "jp": self.__to_jp(name)}

        self.__inverted = inverted

        w, h = 85, 140
        n = self.__number or 11 + self.courts().index(self.__name["en"])
        x, y = (n - 1) * w, (2 + self.suits().index(self.__suit)) * h
        self.__image = imageset.crop((x, y, x+w, y+h)).rotate(180) if inverted else imageset.crop((x, y, x+w, y+h))
        self.__back  = backimage

    @property
    def suit(self):
        return self.__suit

    @property
    def name(self):
        return {
            "en": "{0} of {1}".format(self.__name["en"], self.__suit),
            "jp": "{0}の{1}".format(self.__to_jp(self.__suit), self.__to_jp(self.__name["en"]))
        }

    @property
    def number(self):
        return self.__number or self.__name["en"]

    @property
    def inverted(self):
        return self.__inverted

    @property
    def image(self):
        return self.__image

    @property
    def back(self):
        return self.__back

    @property
    def info(self):
        return "{0}({1})".format(self.name["jp"], "逆位置" if self.inverted else "正位置")

    @property
    def keywords(self):
        return None

    @staticmethod
    def __to_jp(name):
        if name == 1: name = "Ace"
        names = {
            "Page"      : "ペイジ",
            "Knight"    : "ナイト",
            "Queen"     : "クイーン",
            "King"      : "キング",
            "Ace"       : "エース",
            "Wands"     : "ワンド",
            "Pentacles" : "ペンタクル",
            "Cups"      : "カップ",
            "Swords"    : "ソード",
        }
        return names.get(name) or name

    @classmethod
    def define(cls):
        return [(suit, number) for suit in cls.suits() for number in cls.pips() + cls.courts()]

    @classmethod
    def suits(cls):
        return ["Wands", "Pentacles", "Cups", "Swords"]

    @classmethod
    def pips(cls):
        return list(range(1,11))

    @classmethod
    def courts(cls):
        return ["Page", "Knight", "Queen", "King"]

