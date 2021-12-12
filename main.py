import typing as T

from assets import download_assets
from cards import find_random_commander_for_colors
from colors import choose_random_colors
from decks import build_deck
from theme import find_theme_weightings_for_commander


SELECTION_METHODOLOGY = 1


def run():
    download_assets()

    if SELECTION_METHODOLOGY == 1:
        # Choose colors, select a commander for those colors, find a theme, populate
        color_code = choose_random_colors()
        commander = find_random_commander_for_colors(color_code)
        print(commander)
        # theme_weightings = find_theme_weightings_for_commander(commander)
        # build_deck(
        #    colors=colors, commander=commander, theme_weightings=theme_weightings
        # )
    else:
        raise Exception(f"Unknown selection methodology: {SELECTION_METHODOLOGY}")
    # themes, strategies = select_random_themes_and_tribes()
    # deck = build_deck(themes, strategies)
    # add_mana_base(deck)


"""
def select_random_themes_and_tribes() -> T.Tuple[T.List[Theme], T.List[Tribe]]:
    print("Selecting random themes and straegies...")
    themes = []
    tribes = []
    return (themes, tribes)

def build_deck(themes: T.List[Theme], strategies: T.List[Tribe]) -> Deck:
    return Deck()

def add_mana_base(deck: Deck) -> Deck:
    return deck


def choose_colors() -> T.List[Color]:
    return []
"""

if __name__ == "__main__":
    run()
