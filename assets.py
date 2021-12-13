import json
import requests
import os

from colors import COLOR_CODES
from django.utils.text import slugify

FILEPATH = "static/assets"
CARDS_FILEPATH = f"{FILEPATH}/cards"
DECKS_FILEPATH = f"{FILEPATH}/decks"
COMMANDERS_FILEPATH = f"{FILEPATH}/commanders"
THEMES_FILEPATH = f"{FILEPATH}/themes"
TRIBES_FILEPATH = f"{FILEPATH}/tribes"


BASE_URL = "https://json.edhrec.com"
CARDS_URL = f"{BASE_URL}/cards"
COMMANDERS_URL = f"{BASE_URL}/commanders"
TRIBES_URL = f"{BASE_URL}/tribes"
THEMES_URL = f"{BASE_URL}/themes"


def download_assets():
    print("Downloading assets...")
    ensure_folders_exist()
    download_commanders_by_color()
    download_themes()
    download_tribes()


def ensure_folders_exist():
    paths = [
        FILEPATH,
        CARDS_FILEPATH,
        COMMANDERS_FILEPATH,
        THEMES_FILEPATH,
        TRIBES_FILEPATH,
        DECKS_FILEPATH,
    ]
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)


def download_commanders_by_color():
    for color_code in COLOR_CODES:
        filepath = f"{COMMANDERS_FILEPATH}/{color_code}.json"
        url = f"{COMMANDERS_URL}/{color_code}.json"
        request_asset_and_save(url=url, filepath=filepath)


def download_themes():
    url = "https://json.edhrec.com/themes.json"
    filepath = f"{THEMES_FILEPATH}/themes.json"
    request_asset_and_save(url, filepath)

    asset = retrieve_asset("themes/themes.json")
    for theme in asset["container"]["json_dict"]["cardlists"][0]["cardviews"]:
        theme_url = f"{BASE_URL}{theme['url']}.json"
        slug = slugify(theme["name"])
        theme_filepath = f"{THEMES_FILEPATH}/theme-{slug}.json"
        request_asset_and_save(theme_url, theme_filepath)

    # Save additional themes
    url = "https://json.edhrec.com/themes-themesbypopularitysort-1.json"
    filepath = f"{THEMES_FILEPATH}/themes-2.json"
    request_asset_and_save(url, filepath)

    asset = retrieve_asset("themes/themes-2.json")
    for theme in asset["cardviews"]:
        theme_url = f"{BASE_URL}{theme['url']}.json"
        slug = slugify(theme["name"])
        theme_filepath = f"{THEMES_FILEPATH}/theme-{slug}.json"
        request_asset_and_save(theme_url, theme_filepath)


def download_tribes():
    url = "https://json.edhrec.com/tribes.json"
    filepath = f"{TRIBES_FILEPATH}/tribes.json"
    request_asset_and_save(url, filepath)

    asset = retrieve_asset("tribes/tribes.json")
    for tribe in asset["container"]["json_dict"]["cardlists"][0]["cardviews"]:
        tribe_url = f"{BASE_URL}{tribe['url']}.json"
        slug = slugify(tribe["name"])
        theme_filepath = f"{TRIBES_FILEPATH}/tribe-{slug}.json"
        request_asset_and_save(tribe_url, theme_filepath)


def request_asset_and_save(url, filepath, overwrite=False):
    if os.path.isfile(filepath) and not overwrite:
        return
    if overwrite:
        os.remove(filepath)
    print(f"Saving {filepath}")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Could not get {url}")
    with open(filepath, "w+") as f:
        f.write(response.text)


def save_asset_for_commander(slug):
    filepath = f"{COMMANDERS_FILEPATH}/{slug}.json"
    url = f"{COMMANDERS_URL}/{slug}.json"
    request_asset_and_save(url=url, filepath=filepath)


def retrieve_asset(filename):
    with open(f"{FILEPATH}/{filename}") as f:
        data = json.loads(f.read())
    return data


def is_not_asset_file(filepath):
    assets = [
        "tribes.json",
        "themes.json",
        "themes-2.json",
    ]
    return filepath not in assets


def save_asset_for_card(slug):
    if "/" in slug:
        # Eg theme or tribe cards, or partner commanders
        slug = slug.split("/")[0]
    filepath = f"{CARDS_FILEPATH}/{slug}.json"
    url = f"{CARDS_URL}/{slug}.json"
    request_asset_and_save(url=url, filepath=filepath)
