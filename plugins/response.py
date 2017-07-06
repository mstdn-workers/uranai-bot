from slackbot.bot import respond_to, listen_to
from plugins import tarot, images, mode, cache, data
from collections import OrderedDict


cmd = lambda command: r'{0}{1}\s*$'.format(mode.test_prefix, command)

@listen_to(cmd("tarot"))
def fortune_tarot(message):
    if mode.uranai:
        deck  = tarot.Deck(shuffled=True)
        title = ""
        if drawn_cards_exists(deck, message):
            message.send("今の *" + data.get_username(message.body["user"]) + "* さんに必要なキーカードはこちらです。")
            title += "キーカード: "
        card  = deck.draw_one(deck.major_arcanas)
        image = images.create_single_tarot_image(card)
        title   += card.name["en"].upper()
        comment  = "*{0}*\n{1}".format("キーワード", card.keywords)
        filename = 'tarot_{0}.png'.format(card.name["en"] + '_reversed' if card.reversed else '')
        images.post(message, image, title=title, comment=comment, file_name=filename)

@listen_to(cmd("tarot 3"))
def fortune_tarot_3(message):
    if mode.uranai:
        deck  = tarot.Deck(shuffled=True)
        cards = deck.draw_cards(deck.major_arcanas, 3)
        image = images.create_triple_tarot_image(cards)
        when     = ["過去","現在","未来"]
        title    = "・".join(when)
        comments = "\n".join(["*{0}: {1}*\n{2}".format(when[cards.index(card)], card.info, card.keywords) for card in cards])
        filename = 'tarot_three.png'
        images.post(message, image, title=title, comment=comments, file_name=filename)
        cache.add("uranai", message, [ card.name for card in cards ])

@listen_to(cmd("tarot ([a-zA-Z\s]+)"))
def fortune_tarot_name(message, name):
    if mode.uranai:
        deck  = tarot.Deck(shuffled=False)
        cards = deck.pick_by_names(deck.major_arcanas + deck.minor_arcanas, [name])
        if not cards:
            return
        card  = cards[0]
        display_name = "{0} {1}".format(card.roman, card.name["jp"]) if card.is_major else card.name["jp"]
        image = images.create_single_tarot_image(card, display_name)
        title    = card.name["en"].upper()
        comment  = "\n".join([
            "*{0}*\n{1}".format("正位置のキーワード", card.keywords),
            "*{0}*\n{1}".format("逆位置のキーワード", card.keywords_another_side)]) if card.keywords else None
        filename = 'tarot_{0}.png'.format(card.name["en"])
        images.post(message, image, title=title, comment=comment, file_name=filename)

@listen_to(cmd("tarot help"))
def fortune_tarot_help(message):
    if mode.uranai:
        help = OrderedDict()
        help.update((
            ("tarot", "１枚のカードを引きます。"),
            ("tarot 3", "過去・現在・未来を表す３枚のカードを引きます。"),
            ("tarot help", "ヘルプを表示します。"),
            ("tarot [name]", "[name]のカードを表示します。"),
            ("tarot names", "カードの名前を一覧表示します。"),
        ))
        message.send(create_help_message(help, break_line=True))

@listen_to(cmd("tarot names"))
def fortune_tarot_names(message):
    if mode.uranai:
        help = OrderedDict()
        deck = tarot.Deck(shuffled=False)
        help.update((
            (card.name["en"].lower(), "{0}のカード".format(card.name["jp"]))
            for card in deck.major_arcanas
        ))
        message.send(create_help_message(help, break_line=False))


def drawn_cards_exists(deck, message):
    prev_card_names = cache.get("uranai", message)
    if prev_card_names:
        deck.pick_by_names(deck.major_arcanas, prev_card_names)
        return True
    return False

def create_help_message(help, break_line=False):
    division = "\n" if break_line else " "
    mao      = "　:speech_balloon:\n:mao_rev:"
    return "```" + "\n".join(["{0}:{2}{1}".format(cmd, desc, division) for cmd,desc in help.items() ]) + "\n```" + mao