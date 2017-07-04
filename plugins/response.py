from slackbot.bot import respond_to, listen_to
from plugins import tarot, images, mode


@listen_to(r'{0}tarot$'.format(mode.test_prefix))
def fortune_tarot(message):
    if mode.uranai:
        deck  = tarot.Deck(shuffled=True)
        card  = deck.pick_one_from(deck.major_arcanas)
        panel = images.set_size(
            images.text_at_center(images.concat([images.blank, images.blank]), card.info_rows), images.panel_size)
        image = images.bgcolor(images.set_size(
            images.concat([images.dropshadow(card.image), panel]), images.canvas_size), images.bg_color)
        comment  = "*{0}*\n{1}".format("キーワード", card.keywords)
        filename = ('tarot_{0}_inverted.png' if card.reversed else 'tarot_{0}.png').format(card.name["en"])
        images.post(message, image, title=card.name["en"].upper(), comment=comment, file_name=filename)

@listen_to(r'{0}tarot 3'.format(mode.test_prefix))
def fortune_3tarot(message):
    if mode.uranai:
        deck  = tarot.Deck(shuffled=True)
        cards = deck.pick(3)
        image = images.bgcolor(images.set_size(
            images.dropshadow(images.concat([card.image for card in cards])), images.canvas_size), images.bg_color)
        when  = ["過去","現在","未来"]
        comments = "\n".join(["*{0}: {1}*　{2}".format(when[cards.index(card)], card.info, card.keywords) for card in cards])
        filename = 'tarot_three.png'
        images.post(message, image, title="・".join(when), comment=comments, file_name=filename)

