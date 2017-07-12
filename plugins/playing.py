from plugins import resources, tools
from collections import Counter
import random


class Deck(object):

    def __init__(self, shuffled=False, use_joker=2, imageset=resources.playing_cards.images):
        back_color = random.choice(["black", "red", "red", "red", "red"])
        deck = [Card(suit, number, imageset, back_color) for suit, number in resources.playing_cards.cards]

        if use_joker and use_joker == 1:
            deck = deck + [Card(None, random.choice([1, 2]), imageset, back_color)]
        elif use_joker:
            deck = deck + [Card(None,1, imageset, back_color), Card(None,2, imageset, back_color)]

        if shuffled:
            random.shuffle(deck)

        self.__deck = deck

    def draw_cards(self, count):
        return [self.draw_one() for n in range(count) if len(self.__deck) > 0]

    def draw_one(self):
        return self.__deck.pop(0) if len(self.__deck) > 0 else None

    def pick_one(self, suit, number):
        cards = [ card for card in self.__deck if card.suit == suit and card.number == number]
        if cards:
            return cards[0]
        return None

    def pick_joker(self):
        cards = [card for card in self.__deck if card.is_joker]
        if cards:
            return random.choice(cards)
        return None

    @property
    def cards(self):
        return self.__deck


    @classmethod
    def sort(cls, cards):
        def key(card):
            n = card.number if not card.is_joker else 14
            s = resources.playing_cards.suits.index(card.suit) if not card.is_joker else 4
            return "{0:2d}{1}".format(n, s)
        return sorted(cards, key=key)

class Card(object):
    image_size = 80, 120

    def __init__(self, suit, number, imageset, back_color):
        self.__suit     = suit
        self.__number   = number if suit else None
        self.__is_joker = suit is None

        w, h   = self.image_size
        x, y   = (number - 1) * w, (resources.playing_cards.suits.index(self.__suit) if not self.__is_joker else 4) * h
        self.__image = imageset.crop((x, y, x+w, y+h))

        bx, by = (2 if back_color == "black" else 3) * w, 4 * h
        self.__back  = imageset.crop((bx, by, bx+w, by+h))

    @property
    def is_joker(self):
        return self.__is_joker

    @property
    def suit(self):
        return self.__suit

    @property
    def number(self):
        return self.__number

    @property
    def name(self):
        if self.is_joker:
            return "Joker"
        else:
            name = resources.playing_cards.names.get(self.number, tools.number_to_name(self.number))
            return "{0} of {1}".format(name, self.__suit)

    @property
    def image(self):
        return self.__image

    def __eq__(self, other):
        return self.number == other.number

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if self.is_joker:
            return not other.is_joker
        if other.is_joker:
            return False
        return self.number > other.number

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __lt__(self, other):
        return not self.__ge__(other)

    def __le__(self, other):
        return not self.__gt__(other)

    def __str__(self):
        return self.name


class PokerHand(object):

    @classmethod
    def open(cls, cards):
        if len(cards) != 5:
            raise ValueError
        return resources.playing_cards.poker_hands[cls.__check_hand(cards)[0]]["jp"]

    @classmethod
    def __check_hand(cls, cards):
        if any([card.is_joker for card in cards]):
            numbers = [card for card in cards if not card.is_joker]
            jokers = [card for card in cards if card.is_joker]
            return cls.__check_hands_with_jokers(numbers, jokers)

        else:
            return cls.__check_hands_without_joker(cards)

    @classmethod
    def __check_hands_with_jokers(cls, cards, jokers):
        if len(jokers) == 1:
            pair_set = cls.pairs(cards)
            pairs = [c for n, c in pair_set]
            if pairs[0] == 4:
                return 11, pair_set
            magic_cards = Deck(shuffled=False, use_joker=False).cards
            m = max([ cls.__check_hands_without_joker(cards + [j]) for j in magic_cards], key=lambda s:s[0])
            return m
        else:
            jokers.pop()
            magic_cards = Deck(shuffled=False, use_joker=False).cards
            return max([ cls.__check_hands_with_jokers(cards + [j], jokers) for j in magic_cards], key=lambda s:s[0])


    @classmethod
    def __check_hands_without_joker(cls, cards):
        ligh_straight = cls.is_high_straight(cards)
        straight = cls.is_straight(cards)
        flush    = cls.is_flush(cards)
        pair_set = cls.pairs(cards)
        pairs    = [c for n,c in pair_set]
        if ligh_straight and flush:
            return 10, pair_set
        if straight and flush:
            return  9, pair_set
        if pairs[0] == 4:
            return  8, pair_set
        if pairs[0] == 3 and len(pairs) == 2:
            return  7, pair_set
        if flush:
            return  6, pair_set
        if straight:
            return  5, pair_set
        if pairs[0] == 3:
            return  4, pair_set
        if pairs[0] == 2 and len(pairs) == 3:
            return  3, pair_set
        if pairs[0] == 2:
            return  2, pair_set
        return 1, pair_set

    @classmethod
    def pairs(cls, cards):
        return Counter([card.number for card in cards]).most_common()

    @classmethod
    def is_flush(cls, cards):
        cnt = Counter([card.suit for card in cards])
        n, c = cnt.most_common()[0]
        return c == len(cards)

    @classmethod
    def is_straight(cls, cards):
        ns = [card.number for card in cards]
        if all([ (min(ns)+i) in ns for i in range(1,5) ]):
            return True
        return cls.is_high_straight(cards)

    @classmethod
    def is_high_straight(cls, cards):
        ns = [card.number for card in cards]
        if min(ns) == 1:
            rem = [n for n in ns if n != 1]
            return all([ (min(rem)+i) in rem for i in range(1,4) ]) and min(rem) == 10
        return False

    @classmethod
    def create_point(cls, cards):
        point, pair_set = cls.__check_hand(cards)
        numbers = [ n for n,c in sorted(pair_set, key=lambda p: p[1]*100 + (14 if p[0] == 1 else p[0]), reverse=True)]
        for n in range(5):
            p = numbers[n] if len(numbers) > n else 0
            p = 14 if p == 1 else p
            point = point * 100 + p
        point = point * 100 + (0 if any([ card.is_joker for card in cards]) else 1)
        return point

    @classmethod
    def point_to_hand(cls, point):
        return point//(100**6)








