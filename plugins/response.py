from slackbot.bot import respond_to, listen_to
from plugins import tarot, images


@listen_to(r'^tarot$')
def fortune_tarot(message):
    deck = tarot.Deck(shuffled=True)
    card = deck.pick_one_from(deck.major_arcanas)
    filename = ('tarot_{0}_inverted.png' if card.inverted else 'tarot_{0}.png').format(card.name["en"])
    comment  = "*{0}*\n{1}".format(card.info, card.keywords)
    image = images.concat([card.image, card.back, card.back])
    images.post(message, image, title=card.name["en"].upper(), comment=comment, file_name=filename)

@listen_to(r'^tarot 3')
def fortune_3tarot(message):
    deck  = tarot.Deck(shuffled=True)
    cards = deck.pick(3)
    image = images.concat([card.image for card in cards])
    when  = ["過去","現在","未来"]
    comments = "\n".join(["*{0}:　{1}*　{2}".format(when[cards.index(card)], card.info, card.keywords) for card in cards])
    filename = 'tarot_three.png'
    images.post(message, image, title="・".join(when), comment=comments, file_name=filename)
