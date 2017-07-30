from slackbot.bot import respond_to, listen_to
from plugins import tarot, images, mode, cache, api, playing, resources, log
from collections import OrderedDict
from itertools import groupby
import random
import slackbot_settings


cmd = lambda command: r'{0}{1}\s*$'.format(mode.test_prefix, command)

@listen_to(cmd("tarot"))
def fortune_tarot(message):
    if mode.uranai:
        log.write(message)
        deck  = tarot.Deck(shuffled=True)
        title = ""
        if drawn_cards_exists(deck, message):
            message.send("今の *" + api.get_user_mame(message.body["user"]) + "* さんに必要なキーカードはこちらです。")
            title += "キーカード: "
        card  = deck.draw_one(deck.major_arcanas)
        image = images.create_single_tarot_image(card)
        title   += card.name["en"].upper()
        comment  = "*{0}*\n{1}".format("キーワード", card.keywords)
        filename = 'tarot_{0}{1}.png'.format(card.name["en"], '_reversed' if card.reversed else '')
        api.post_image(message, image, title=title, comment=comment, file_name=filename)
        lead_user_to_channels(message)

@listen_to(cmd("tarot 3"))
def fortune_tarot_3(message):
    if mode.uranai:
        log.write(message)
        deck  = tarot.Deck(shuffled=True)
        cards = deck.draw_cards(deck.major_arcanas, 3)
        image = images.create_triple_tarot_image(cards)
        when     = ["過去","現在","未来"]
        title    = "・".join(when)
        comments = "\n".join(["*{0}: {1}*\n{2}".format(when[cards.index(card)], card.info, card.keywords) for card in cards])
        filename = 'tarot_three.png'
        api.post_image(message, image, title=title, comment=comments, file_name=filename)
        cache.add("uranai", message, [ card.name for card in cards ])
        lead_user_to_channels(message)

@listen_to(cmd("tarot ([a-zA-Z\s]+)"))
def fortune_tarot_name(message, name):
    if mode.uranai:
        log.write(message)
        deck  = tarot.Deck(shuffled=False)
        cards = deck.pick_by_names(deck.major_arcanas + deck.minor_arcanas, [name])
        if not cards:
            return
        card  = cards[0]
        image = images.create_single_tarot_image(card, card.display_name)
        title    = card.name["en"].upper()
        comment  = "\n".join([
            "*{0}*\n{1}".format("正位置のキーワード", card.get_keywords(reversed=False)),
            "*{0}*\n{1}".format("逆位置のキーワード", card.get_keywords(reversed=True))]) if card.keywords else None
        filename = 'tarot_{0}.png'.format(card.name["en"])
        api.post_image(message, image, title=title, comment=comment, file_name=filename)
        lead_user_to_channels(message)

@listen_to(cmd("tarot help"))
def fortune_tarot_help(message):
    if mode.uranai:
        log.write(message)
        help = OrderedDict()
        help.update((
            ("tarot", "１枚のカードを引きます。"),
            ("tarot 3", "過去・現在・未来を表す３枚のカードを引きます。"),
            ("tarot help", "ヘルプを表示します。"),
            ("tarot help mao", "まおーヘルプを表示します。"),
            ("tarot [name]", "[name]のカードを表示します。"),
            ("tarot names", "カードの名前を一覧表示します。"),
        ))
        message.send(create_help_message(help, break_line=True))
        lead_user_to_channels(message)

@listen_to(cmd("tarot names"))
def fortune_tarot_names(message):
    if mode.uranai:
        log.write(message)
        help = OrderedDict()
        deck = tarot.Deck(shuffled=False)
        help.update((
            (card.name["en"].lower(), "{0}のカード".format(card.name["jp"]))
            for card in deck.major_arcanas
        ))
        message.send(create_help_message(help, break_line=False))
        lead_user_to_channels(message)

@listen_to(cmd("tarot help mao"))
def fortune_tarot_help_mao(message):
    if mode.uranai:
        mao_help = api.get_message(slackbot_settings.CHANNEL_TAROT, "1500304822.076050")
        if mao_help:
            message.send(create_pre_message(mao_help["text"], show_mao=True))
            lead_user_to_channels(message)


@listen_to(cmd("poker"))
def casino_playing_card_poker(message):
    if mode.card:
        log.write(message)
        cards = deal_cards(message, 5, shuffled=True, use_joker=1)
        cache.add_ranking("poker", message, playing.PokerHand.create_point(cards), playing.PokerHand.open(cards))
        msg = get_message_for_poker(playing.PokerHand.open(cards))
        if msg:
            message.send(msg)
        lead_user_to_channels(message)

@listen_to(cmd("poker rank"))
def casino_playing_card_poker_rank(message):
    if mode.card:
        log.write(message)
        help = OrderedDict()
        data   = sorted(cache.get_ranking("poker", message), key=lambda c: int(c["point"]), reverse=True)
        if len(data) < 1:
            message.send("いまならあなたが一位になれますよ！")
            return
        groups = groupby(data, key=lambda c: int(c["point"]))
        help.update((
            (str(i+1),", ".join([ "{0} ({1}) [{2}]".format(
                api.get_user_mame(data["user"]),
                resources.playing_cards.poker_hands[playing.PokerHand.point_to_hand(gs[0])]["jp"],
                data["count"][1]
            ) for data in gs[1] ])) for i, gs in enumerate(groups)
        ))
        message.send(create_help_message(help, break_line=False, show_mao=False))
        lead_user_to_channels(message)


@listen_to(cmd("poker help"))
def casino_playing_cards_joker(message):
    if mode.card:
        log.write(message)
        help = OrderedDict()
        help.update((
            ("poker", "ポーカーで勝負です。"),
            ("poker rank", "その日のランキングを表示します。\n\n[ランキング表示]\nランク: プレイヤー (役) [試行回数]"),
        ))
        message.send(create_help_message(help, break_line=True, show_mao=False))
        lead_user_to_channels(message)


@listen_to(cmd("deal a card"))
def casino_playing_card_one(message):
    if mode.card:
        deal_cards(message, 1)
        lead_user_to_channels(message)

@listen_to(cmd("deal ([0-9]+) cards?"))
def casino_playing_cards(message, count):
    if mode.card:
        log.write(message)
        count = int(count)
        if 1 <= count <= 5:
            deal_cards(message, count)
        elif count < 1:
            message.send("素敵なジョークです。")
        else:
            message.send("すみません、5枚までになっております。")
        lead_user_to_channels(message)

@listen_to(cmd("joker"))
def casino_playing_cards_joker(message):
    if mode.card:
        log.write(message)
        deck = playing.Deck()
        card = deck.pick_joker()
        image = images.create_playing_card_image([card])
        filename = "joker.png"
        title = "ジョーカー"
        comment = None
        api.post_image(message, image, title=title, comment=comment, file_name=filename)
        message.send("どうぞ")
        lead_user_to_channels(message)

@listen_to(cmd("porker"))
def casino_playing_cards_porker(message):
    if mode.card:
        log.write(message)
        oink = random.choice(["ぶぅ", "ぶーぶー", "ぶひ〜", "ブヒブヒ", "おいんくおいんく"])
        message.send(":piggy: < " + oink)
        lead_user_to_channels(message)

@listen_to(cmd("porker rank"))
def casino_playing_cards_porker2(message):
    if mode.card:
        log.write(message)
        help = OrderedDict()
        help.update((
            ("1", "黒豚"),
            ("2", "平牧三元豚"),
            ("3", "白金豚"),
            ("4", "TOKYO X"),
            ("5", "あぐー豚"),
            ("6", "イベリコ豚"),
            ("7", "金華豚"),
            ("8", "梅山豚"),
            ("9", "ヨークシャー"),
            ("10", "牡丹肉"),
        ))
        message.send(create_help_message(help, break_line=False, show_mao=False))
        lead_user_to_channels(message)

@listen_to(cmd("porker help"))
def casino_playing_cards_porker3(message):
    if mode.card:
        n = random.randint(0,5)
        image = resources.poker_help_images.crop((0 + 320 * n, 0, 0 + 320 * (n + 1), 170))
        api.post_image(message, image, title="porkerより", comment=None, file_name="poker_help.png")


def drawn_cards_exists(deck, message):
    prev_card_names = cache.get("uranai", message)
    if prev_card_names:
        deck.pick_by_names(deck.major_arcanas, prev_card_names)
        return True
    return False

def create_pre_message(text, show_mao=True):
    mao = "　:speech_balloon:\n:mao_rev:" if show_mao else ""
    return "```" + text + "\n```" + mao

def create_help_message(help, break_line=False, show_mao=True):
    delimiter = "\n" if break_line else " "
    help_message = "\n".join(["{0}:{2}{1}".format(cmd, desc, delimiter) for cmd,desc in help.items() ])
    return create_pre_message(help_message, show_mao=show_mao)

def deal_cards(message, count, shuffled=True, use_joker=1):
    deck = playing.Deck(shuffled=shuffled, use_joker=use_joker)
    cards = deck.draw_cards(count)
    image = images.create_playing_card_image(cards)
    filename = "playing_cards.png"
    title = api.get_user_mame(message.body["user"]) + "さんの手札"
    comment = None
    api.post_image(message, image, title=title, comment=comment, file_name=filename)
    return cards

def get_message_for_poker(hand):
    if hand in {"ファイブカード"}:
        return "これはまさかの、{0}・・・".format(hand)
    if hand in {"ロイヤルストレートフラッシュ"}:
        return "ほう、{0}、これは素晴らしい！".format(hand)
    if hand in {"ストレートフラッシュ", "フォーカード", "フルハウス"}:
        return "ふむ、{0}ですか、お見事。".format(hand)
    if hand in {"フラッシュ", "ストレート", "スリーカード"}:
        return "{0}ですね、なかなか。".format(hand)
    if hand in {"ツーペア", "ワンペア"}:
        return "{0}ですね。".format(hand)
    return None

def lead_user_to_channels(message):
    if message.body["channel"] in [slackbot_settings.CHANNEL_GENERAL]:
        channel = None
        if mode.uranai:
            channel = slackbot_settings.CHANNEL_TAROT
        elif mode.card:
            channel = slackbot_settings.CHANNEL_POKER
        if channel:
            message.send("つづきは {0} でどうぞ！".format(api.get_channel_tag(channel)))