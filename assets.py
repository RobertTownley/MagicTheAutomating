import json
import requests
import os

from colors import COLOR_CODES

FILEPATH = "static/assets"
COMMANDERS_FILEPATH = f"{FILEPATH}/commanders"


BASE_URL = "https://json.edhrec.com/"
COMMANDERS_URL = f"{BASE_URL}/commanders"


def download_assets():
    download_commanders_by_color()
    print("Downloading assets...")
    # https://json.edhrec.com/commanders/rg.json


def download_commanders_by_color():
    for color_code in COLOR_CODES:
        filepath = f"{COMMANDERS_FILEPATH}/{color_code}.json"
        url = f"{COMMANDERS_URL}/{color_code}.json"
        request_asset_and_save(url=url, filepath=filepath)


def request_asset_and_save(url, filepath, overwrite=False):
    if os.path.isfile(filepath) and not overwrite:
        return
    if overwrite:
        os.remove(filepath)
    print(f"Saving {filepath}")
    response = requests.get(url)
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
