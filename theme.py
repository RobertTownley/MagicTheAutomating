import typing as T
from models import Card, Theme


def find_theme_weightings_for_commander(commander: Card) -> T.Dict[Theme, int]:
    print(commander)
    return {
        Theme(): 1,
        Theme(): 2,
    }
