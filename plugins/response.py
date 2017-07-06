from slackbot.bot import respond_to, listen_to
from plugins import tarot, images, mode, cache, data
from collections import OrderedDict


@listen_to(r'{0}tarot$'.format(mode.test_prefix))
def fortune_tarot(message):
    if mode.uranai:
        deck  = tarot.Deck(shuffled=True)
        names = cache.get("uranai", message)
        if names:
            deck.pick_by_name(deck.major_arcanas, names)
            message.send("今の *" + data.get_username(message.body["user"]) + "* さんに必要なキーカードはこちらです。")
        card  = deck.pick_one_from(deck.major_arcanas)
        panel = images.text_at_center(images.concat([images.blank, images.blank]), card.info_rows)
        panel = images.set_size(panel, images.panel_size)
        image = images.concat([images.dropshadow(card.image), panel])
        image = images.bgcolor(images.set_size(image, images.canvas_size), images.bg_color)
        comment  = "*{0}*\n{1}".format("キーワード", card.keywords)
        filename = 'tarot_{0}.png'.format(card.name["en"] + '_reversed' if card.reversed else '')
        title    = ("" if not names else "キーカード: ") + card.name["en"].upper()
        images.post(message, image, title=title, comment=comment, file_name=filename)

@listen_to(r'{0}tarot 3$'.format(mode.test_prefix))
def fortune_tarot_3(message):
    if mode.uranai:
        deck  = tarot.Deck(shuffled=True)
        cards = deck.pick(deck.major_arcanas, 3)
        image = images.dropshadow(images.concat([card.image for card in cards]))
        image = images.bgcolor(images.set_size(image, images.canvas_size), images.bg_color)
        when  = ["過去","現在","未来"]
        comments = "\n".join(["*{0}: {1}*\n{2}".format(when[cards.index(card)], card.info, card.keywords) for card in cards])
        filename = 'tarot_three.png'
        images.post(message, image, title="・".join(when), comment=comments, file_name=filename)
        cache.add("uranai", message, [ card.name for card in cards ])

@listen_to(r'{0}tarot ([a-zA-Z\s]+)$'.format(mode.test_prefix))
def fortune_tarot_name(message, name):
    if mode.uranai:
        deck = tarot.Deck(shuffled=False)
        cards = deck.pick_by_name(deck.major_arcanas + deck.minor_arcanas, [name])
        if not cards:
            return
        card  = cards[0]
        display_name = "{0} {1}".format(card.roman, card.name["jp"]) if card.is_major else card.name["jp"]
        fontsize = 18 if card.is_major else 16
        panel = images.text_at_center(images.concat([images.blank, images.blank]), display_name, fontsize=fontsize)
        panel = images.set_size(panel, images.panel_size)
        image = images.concat([images.dropshadow(card.image), panel])
        image = images.bgcolor(images.set_size(image, images.canvas_size), images.bg_color)
        if card.keywords:
            comment = "\n".join([
                "*{0}*\n{1}".format("正位置のキーワード", card.keywords),
                "*{0}*\n{1}".format("逆位置のキーワード", card.keywords_another_side),
            ])
        else:
            comment = None
        filename = 'tarot_{0}.png'.format(card.name["en"])
        images.post(message, image, title=card.name["en"].upper(), comment=comment, file_name=filename)

@listen_to(r'{0}tarot help$'.format(mode.test_prefix))
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

        message.send("```" + "\n".join(["{0}:\n{1}".format(cmd, desc) for cmd,desc in help.items() ]) + "\n```" + images.mao)

@listen_to(r'{0}tarot names$'.format(mode.test_prefix))
def fortune_tarot_names(message):
    if mode.uranai:
        help = OrderedDict()
        deck = tarot.Deck(shuffled=False)
        help.update((
            (card.name["en"].lower(), "{0}のカード".format(card.name["jp"]))
            for card in deck.major_arcanas
        ))
        message.send("```" + "\n".join(["{0}: {1}".format(cmd, desc) for cmd,desc in help.items() ]) + "\n```" + images.mao)