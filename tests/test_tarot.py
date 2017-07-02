import unittest, json
from PIL import Image
from plugins import tarot, data

class TestTarot(unittest.TestCase):
    imageset = Image.open('../materials/tarot-waite.png')
    keywords = data.load('../materials/keywords.json')

    def test_tarot_card_numbers(self):
        deck = tarot.Deck(shuffled=False, imageset=self.imageset, keywords=self.keywords)
        major_arcanas = deck.major_arcanas
        minor_arcanas = deck.minor_arcanas
        self.assertEqual(len(major_arcanas), 22)
        self.assertEqual(len(minor_arcanas), 56)

    def test_pick_cards_major(self):
        deck = tarot.Deck(shuffled=False, imageset=self.imageset, keywords=self.keywords)
        cards = deck.pick(5)
        self.assertEqual(len(cards), 5)
        self.assertEqual(len(cards), len(set(cards)))
        self.assertFalse(any([card.inverted for card in cards]))
        self.assertEqual(len(deck.major_arcanas), 17)

    def test_pick_cards_minor(self):
        deck = tarot.Deck(shuffled=False, imageset=self.imageset, keywords=self.keywords)
        cards = deck.pick(5, minor_arcana=True)
        self.assertEqual(len(cards), 5)
        self.assertEqual(len(cards), len(set(cards)))
        self.assertFalse(any([card.inverted for card in cards]))
        self.assertEqual(len(deck.minor_arcanas), 51)

    def test_card_image(self):
        deck = tarot.Deck(shuffled=True, imageset=self.imageset, keywords=self.keywords)
        card = deck.pick_one_from(deck.minor_arcanas)
        card.image.save('test.png')
        self.assertEqual(card.image.size, (85,140))

    def test_card_keyword(self):
        with open('../materials/keywords.json','r') as f:
            data = json.load(f)

        for n,pos in  data.items():
            for k,p in pos.items():
                keywords = p["keywords"]
                self.assertEqual(len(keywords), len(set(keywords)))

        deck = tarot.Deck(shuffled=False, imageset=self.imageset, keywords=self.keywords)
        card = deck.pick_one_from(deck.major_arcanas)
        print(card.info, card.keywords)
        self.assertGreater(len(card.keywords), 0)





