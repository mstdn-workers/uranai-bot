import json
from PIL import Image

tarot_back  = Image.open('materials/tarot-back.png')
tarot_blank = Image.new('RGBA', (85, 140), (255, 255, 255, 0))
tarot_waite = Image.open('materials/tarot-waite.png')
canvas_size = (273,182)
bg_color    = (248,248,248,255)

class __major_arcana(object):
    cards = [
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

class __minor_arcana(object):
    suits  = ["Wands", "Pentacles", "Cups", "Swords"]
    courts = ["Page", "Knight", "Queen", "King"]
    pips   = list(range(1,11))
    jp_names = {
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

    @property
    def cards(self):
        return [(suit, number) for suit in self.suits for number in self.pips + self.courts]

class __position(object):
    normal   = {"en": "normal",   "jp": "正位置"}
    reversed = {"en": "reversed", "jp": "逆位置"}

major_arcana = __major_arcana()
minor_arcana = __minor_arcana()
position     = __position()

class __playing_cards(object):
    suits  = ["Spades", "Hearts", "Clubs", "Diamonds"]
    power_of_suit = {"Spades":3, "Hearts" :2, "Diamonds":1, "Clubs":0}
    images = Image.open('materials/playing-cards.png')
    names  = { 1: "Ace", 11: "Jack", 12: "Queen", 13:"King"}
    poker_hands = {
         1: {"en": "High Card", "jp": "ノーペア"},
         2: {"en": "One Pair", "jp": "ワンペア"},
         3: {"en": "Two Pair", "jp": "ツーペア"},
         4: {"en": "Three of a Kind", "jp": "スリーカード"},
         5: {"en": "Straight", "jp": "ストレート"},
         6: {"en": "Flush", "jp": "フラッシュ"},
         7: {"en": "Full House", "jp": "フルハウス"},
         8: {"en": "Four of a Kind", "jp": "フォーカード"},
         9: {"en": "Straight Flush", "jp": "ストレートフラッシュ"},
        10: {"en": "Royal Flush", "jp": "ロイヤルストレートフラッシュ"},
        11: {"en": "Five of a Kind", "jp": "ファイブカード"}
    }

    @property
    def cards(self):
        return [(suit, number) for suit in self.suits for number in range(1,14)]



playing_cards = __playing_cards()

def load(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def load_keywords():
    return load('materials/keywords.json')