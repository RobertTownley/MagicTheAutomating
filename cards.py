import typing as T
import random
from assets import retrieve_asset
from models import Card, Theme, Tribe


def find_random_commander_for_colors(color_code) -> Card:
    ALLOW_PARTNERS = (
        False  # TODO: Implement this later... structure is another complexity
    )
    asset = retrieve_asset(f"commanders/{color_code}.json")
    commanders = asset["container"]["json_dict"]["cardlists"][0]["cardviews"]
    if not ALLOW_PARTNERS:

        def is_commander_asset(commander):
            return commander.get("is_commander")

        commanders = list(filter(is_commander_asset, commanders))

    weights = list(map(lambda x: x["num_decks"], commanders))
    commander = random.choices(commanders, weights=weights)[0]
    return Card.build_from_resource(commander)


def collect_cards_from_commander(commander: Card) -> T.List[Card]:
    cards = []
    for cardlist in commander.asset["container"]["json_dict"]["cardlists"]:
        cards += get_cards_from_cardlist(cardlist)
    return cards


def collect_cards_from_themes(themes: T.List[Theme]) -> T.List[Card]:
    cards = []
    for theme in themes:
        for cardlist in theme.asset["container"]["json_dict"]["cardlists"]:
            cards += get_cards_from_cardlist(cardlist)
    return cards


def collect_cards_from_tribe(tribe: T.Union[Tribe, None]) -> T.List[Card]:
    if not tribe:
        return []
    cards = []
    for cardlist in tribe.asset["container"]["json_dict"]["cardlists"]:
        cards += get_cards_from_cardlist(cardlist)
    return cards


def get_cards_from_cardlist(cardlist: dict) -> T.List[Card]:
    cards = []
    for cardview in cardlist["cardviews"]:
        try:
            cards.append(Card.build_from_resource(cardview))
        except Exception as e:
            print("Couldn't build card", cardview["sanitized"])
    return cards
