import os
import random
import typing as T

from assets import is_not_asset_file
from colors import normalize_colors
from models import Card, Theme


ALL_THEMES = None


def get_all_themes():
    filepaths = list(filter(is_not_asset_file, os.listdir("static/assets/themes")))
    themes = [Theme.build_from_filepath(f) for f in filepaths]
    random.shuffle(themes)
    return themes


def find_themes_for_commander(
    commander: Card, all_themes: T.List[Theme]
) -> T.List[Theme]:
    MAX_THEMES = 3
    themes = []

    # Find themes where the selected commander is a top commander
    for theme in all_themes:
        if commander.sanitized_name in theme.top_commander_slugs:
            themes.append(theme)

    # Find themes for the commander's color scheme
    for theme in all_themes:
        if good_theme_for_commander_colors(theme, commander):
            themes.append(theme)
            if len(themes) > MAX_THEMES:
                break

    themes_to_choose = random.randint(1, MAX_THEMES)
    return themes[:themes_to_choose]


def good_theme_for_commander_colors(theme, commander):
    """Returns true if a commander's colors are in the top X for a theme"""
    try:
        theme_colors = get_colors_for_theme(theme)
    except Exception as e:
        print("Couldn't get colors for theme", e)
        return False
    commander_colors = normalize_colors(commander.colors)
    return commander_colors in theme_colors


def get_colors_for_theme(theme):
    IN_TOP = 5
    if theme.asset.get("relatedinfo"):
        asset_colors = theme.asset["relatedinfo"]["colors"]
        return list(map(normalize_colors, asset_colors))[:IN_TOP]
    else:
        # Get colors of first few commanders
        commanders = theme.asset["container"]["json_dict"]["cardlists"][0]["cardviews"]
        return [normalize_colors(c["color_identity"]) for c in commanders[:IN_TOP]]
