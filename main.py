import typing as T

from assets import download_assets
from cards import find_random_commander_for_colors
from colors import choose_random_colors
from decks import build_deck, save_deck
from exceptions import DeckException
from tribes import find_tribe_for_commander, get_all_tribes
from theme import find_themes_for_commander, get_all_themes


DECKS_TO_BUILD = 1
SELECTION_METHODOLOGY = 1


def run():
    download_assets()
    all_themes = get_all_themes()
    all_tribes = get_all_tribes()

    # Choose colors, select a commander for those colors, find a theme, populate
    for i in range(0, DECKS_TO_BUILD):
        try:
            color_code = choose_random_colors()
            commander = find_random_commander_for_colors(color_code)
            themes = find_themes_for_commander(commander, all_themes)
            tribe = find_tribe_for_commander(commander, all_tribes)
            deck = build_deck(commander, themes, tribe)
            save_deck(deck)
        except DeckException:
            # Deck won't work, keep going
            pass


run()
