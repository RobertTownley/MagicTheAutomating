import math
import random
import typing as T
from assets import save_asset_for_card


from cards import (
    collect_cards_from_commander,
    collect_cards_from_themes,
    collect_cards_from_tribe,
)
from models import Card, Deck, Theme, Tribe


def build_deck(
    commander: Card, themes: T.List[Theme], tribe: T.Union[Tribe, None]
) -> Deck:
    deck = Deck(commander=commander, themes=themes, tribe=tribe)

    cards = []
    cards += collect_cards_from_commander(deck.commander)
    cards += collect_cards_from_themes(themes)
    cards += collect_cards_from_tribe(tribe)

    viable_cards = list(filter(deck.card_is_legal, cards))
    sections = [
        "Creature",
        "Artifact",
        "Enchantment",
        "Planeswalker",
        "Instant",
        "Sorcery",
    ]
    for section in sections:
        add_cards_to_deck(deck, viable_cards, section)

    while deck.card_count < 67:
        card = random.choice(viable_cards)
        deck.add_card(card)

    # Lands
    add_cards_to_deck(deck, viable_cards, "Land")
    fill_deck_with_basic_lands(deck)

    return deck


def add_cards_to_deck(deck, viable_cards, section):
    average_cards_for_section = deck.commander.asset[
        section.lower() if section != "Land" else "nonbasic"
    ]
    cards_to_add = max(
        random.randint(
            average_cards_for_section - 2,
            average_cards_for_section + 2,
        ),
        0,
    )
    cards_of_type = []
    for card in viable_cards:
        duplicates = [
            c for c in cards_of_type if c.sanitized_name == card.sanitized_name
        ]
        if not len(duplicates) and card.primary_type == section:
            cards_of_type.append(card)

    if len(cards_of_type) <= cards_to_add:
        selected = cards_of_type
    else:
        top_cards_count = math.ceil(cards_to_add / 2)
        selected = cards_of_type[:top_cards_count]

        remaining = cards_to_add - top_cards_count
        to_select = cards_of_type[top_cards_count:]
        selected += random.sample(to_select, remaining)

    for card in selected:
        deck.add_card(card)


def fill_deck_with_basic_lands(deck):
    for land_slug in [
        "forest",
        "plains",
        "mountain",
        "swamp",
        "island",
    ]:
        save_asset_for_card(land_slug)

    LAND_MAP = {
        "b": Card.build_from_filepath("cards/swamp.json"),
        "g": Card.build_from_filepath("cards/forest.json"),
        "r": Card.build_from_filepath("cards/mountain.json"),
        "w": Card.build_from_filepath("cards/plains.json"),
        "u": Card.build_from_filepath("cards/island.json"),
    }
    while deck.card_count < 99:
        for color in deck.commander.colors:
            if deck.card_count < 99:
                land = LAND_MAP[color]
                deck.add_card(land)


def save_deck(deck):
    parts = [
        f"{deck.commander.sanitized_name}_",
        "_".join([t.sanitized_name for t in deck.themes]),
        "" if not deck.tribe else deck.tribe.sanitized_name,
    ]
    filename = "_".join([p for p in parts if p])

    content = "\n".join(
        [f"{c.name}" for c in [*list(reversed(deck.cards)), deck.commander]]
    )
    with open(f"static/assets/decks/{filename}.txt", "w+") as f:
        f.write(content)
    print(deck)
    print(filename)
