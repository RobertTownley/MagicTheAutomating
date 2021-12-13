import typing as T
import os
import random

from assets import is_not_asset_file
from models import Card, Tribe


def find_tribe_for_commander(commander: Card, all_tribes) -> T.Union[Tribe, None]:
    # Find themes where the selected commander is a top commander
    for tribe in all_tribes:
        if commander.sanitized_name in tribe.top_commander_slugs:
            return tribe
    return None


def get_all_tribes() -> T.List[Tribe]:
    directory = "static/assets/tribes"
    filepaths = list(filter(is_not_asset_file, os.listdir(directory)))
    tribes = [Tribe.build_from_filepath(f) for f in filepaths]
    random.shuffle(tribes)
    return tribes
