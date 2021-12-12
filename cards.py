import random
from assets import retrieve_asset
from models import Card

from pprint import pprint


def find_random_commander_for_colors(color_code) -> Card:
    asset = retrieve_asset(f"commanders/{color_code}.json")
    commanders = asset["container"]["json_dict"]["cardlists"][0]["cardviews"]
    weights = list(map(lambda x: x["num_decks"], commanders))
    commander = random.choices(commanders, weights=weights)[0]
    return Card.build_from_resource(commander)
