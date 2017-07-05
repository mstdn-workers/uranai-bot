from plugins import data, images
import random


class Deck(object):
    __major = []
    __minor = []

    def __init__(self, shuffled=False, imageset=None, backimage=None, keywords=None):
        if not imageset:
            imageset = images.tarot_waite

        if not backimage:
            backimage = images.back

        if not keywords:
            keywords = data.load_keywords()

        self.__major = [
            MajorArcana(n, en, jp, reversed=shuffled and data.true_or_false(), imageset=imageset, backimage=backimage, keywords=keywords[str(n)])
            for n, en, jp in MajorArcana.define()
        ]
        self.__minor = [
            MinorArcana(s, n, reversed=shuffled and data.true_or_false(), imageset=imageset, backimage=backimage)
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

    def pick(self, arcana, count):
        return [self.pick_one_from(arcana) for n in range(count) if len(arcana) > 0]

    def pick_one_from(self, arcana):
        return arcana.pop(0) if len(arcana) > 0 else None

    def pick_by_name(self, arcana, names):
        def no_the(name):
            return name.replace("The ", "")
        def patterns(name):
            return [name] + list(set(
                [ x
                      for n in name.values()
                      for x in [n, n.upper(), n.lower(), no_the(n), no_the(n).upper(), no_the(n).lower()]]
            ))
        cards = [ a for a in arcana for name in names if name in patterns(a.name) ]
        for card in cards:
            arcana.remove(card)
        return cards


class MajorArcana(object):
    __image    = None
    __back     = None
    __name     = None
    __number   = None
    __reversed = False
    __keywords = None

    def __init__(self, number, name, japanese_name=None, reversed=False, imageset=None, backimage=None, keywords=None):
        self.__number   = number
        self.__name     = {"en":name, "jp":japanese_name}
        self.__reversed = reversed

        w, h = 85, 140
        x, y = self.__number % 11 * w, self.__number // 11 * h
        img = imageset.crop((x, y, x+w, y+h))
        self.__image = img.rotate(180) if reversed else img
        self.__back  = backimage

        self.__keywords = keywords

    @property
    def is_major(self):
        return True

    @property
    def suite(self):
        return None

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
    def reversed(self):
        return self.__reversed

    @property
    def image(self):
        return self.__image

    @property
    def back(self):
        return self.__back

    @property
    def info(self):
        return "{0} {1}({2})".format(self.roman, self.name["jp"], "逆位置" if self.reversed else "正位置")

    @property
    def info_rows(self):
        return "{0} {1}\n({2})".format(self.roman, self.name["jp"], "逆位置" if self.reversed else "正位置")

    @property
    def keywords(self):
        if self.__keywords:
            return "、".join(self.__keywords["reversed"]["keywords"] if self.__reversed else self.__keywords["normal"]["keywords"])
        return None

    @property
    def keywords_another_side(self):
        if self.__keywords:
            return "、".join(self.__keywords["reversed"]["keywords"] if not self.__reversed else self.__keywords["normal"]["keywords"])
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
    __reversed = False

    def __init__(self, suit, number_or_name, reversed=False, imageset=None, backimage=None):
        self.__suit = suit

        if isinstance(number_or_name, int) and 0 < number_or_name < 11:
            self.__number = number_or_name

        name = self.__number_to_name(number_or_name)
        self.__name = {"en": name, "jp": self.__to_jp(name) or self.__to_zenkaku(str(number_or_name))}

        self.__reversed = reversed

        w, h = 85, 140
        n = self.__number or 11 + self.courts().index(self.__name["en"])
        x, y = (n - 1) * w, (2 + self.suits().index(self.__suit)) * h
        img = imageset.crop((x, y, x+w, y+h))
        self.__image = img.rotate(180) if reversed else img
        self.__back  = backimage

    @property
    def is_major(self):
        return False

    @property
    def suit(self):
        return self.__suit

    @property
    def name(self):
        return {
            "en": "{0} of {1}".format(self.__name["en"], self.__suit),
            "jp": "{0}の{1}".format(self.__to_jp(self.__suit), self.__name["jp"])
        }

    @property
    def number(self):
        return self.__number or self.__name["en"]

    @property
    def roman(self):
        return data.arabic_to_roman(self.__number)

    @property
    def reversed(self):
        return self.__reversed

    @property
    def image(self):
        return self.__image

    @property
    def back(self):
        return self.__back

    @property
    def info(self):
        return "{0}({1})".format(self.name["jp"], "逆位置" if self.reversed else "正位置")

    @property
    def info_rows(self):
        return "{0}\n({1})".format(self.name["jp"], "逆位置" if self.reversed else "正位置")

    @property
    def keywords(self):
        return None

    @staticmethod
    def __to_jp(name):
        names = {
            "Page"      : "従者",
            "Knight"    : "騎士",
            "Queen"     : "女王",
            "King"      : "王",
            "Ace"       : "エース",
            "Wands"     : "杖",
            "Pentacles" : "金貨",
            "Cups"      : "聖杯",
            "Swords"    : "剣",
        }
        return names.get(name)

    @staticmethod
    def __to_zenkaku(name):
        """
        http://cuio.blog2.fc2.com/blog-entry-2165.html
        """
        t = dict((0x0020 + ch, 0xff00 + ch) for ch in range(0x5f))
        t[0x0020] = 0x3000
        return name.translate(t)

    @staticmethod
    def __number_to_name(number):
        names = {
            1: "Ace", 2: "Two",   3: "Three", 4: "Four",  5: "Five",
            6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"
        }
        return names.get(number) or str(number)

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

