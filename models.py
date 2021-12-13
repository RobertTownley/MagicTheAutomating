import json
import typing as T
from dataclasses import dataclass

from django.utils.text import slugify


from assets import retrieve_asset, save_asset_for_commander, save_asset_for_card
from colors import normalize_colors


@dataclass
class Theme:
    asset: dict
    name: str
    top_commander_slugs: T.List[str]

    @classmethod
    def build_from_filepath(cls, filename):
        with open(f"static/assets/themes/{filename}") as f:
            asset = json.loads(f.read())
        data = asset["container"]["json_dict"]["cardlists"]
        top_commander_slugs = list(map(lambda x: x["sanitized"], data[0]["cardviews"]))
        return cls(
            asset=asset,
            name=asset["container"]["title"],
            top_commander_slugs=top_commander_slugs,
        )

    def __str__(self):
        return f"Theme ({self.name})"

    def __repr__(self):
        return f"Theme ({self.name})"

    @property
    def sanitized_name(self):
        return f"{slugify(self.name)}-theme"


@dataclass
class Tribe:
    asset: dict
    name: str
    top_commander_slugs: T.List[str]

    @classmethod
    def build_from_filepath(cls, filename):
        with open(f"static/assets/tribes/{filename}") as f:
            asset = json.loads(f.read())
        data = asset["container"]["json_dict"]["cardlists"]

        def get_commander_name(cardview):
            # Remove tribe name from slug, eg 'kemba-kha-regent/cat' -> kemba-kha-regent
            return cardview["sanitized"].split("/")[0]

        top_commander_slugs = list(map(get_commander_name, data[0]["cardviews"]))
        return cls(
            asset=asset,
            name=asset["container"]["title"],
            top_commander_slugs=top_commander_slugs,
        )

    @property
    def sanitized_name(self):
        return f"{slugify(self.name)}-tribe"


@dataclass
class Card:
    # Asset Details
    primary_type: str
    colors: T.List[str]
    color_identity: T.List[str]
    cmc: int
    inclusion: int
    is_commander: bool
    name: str
    num_decks: int
    sanitized_name: str

    # Deck Details
    is_commander: bool

    def __str__(self):
        return self.name

    @classmethod
    def build_from_resource(cls, resource):
        if resource.get("is_commander"):
            save_asset_for_commander(resource["sanitized"])
        else:
            save_asset_for_card(resource["sanitized"])

        return cls(
            cmc=resource["cmc"],
            colors=[x.lower() for x in resource["color_identity"]],
            color_identity=resource["color_identity"],
            inclusion=resource["inclusion"],
            name=resource["name"],
            num_decks=resource["num_decks"],
            primary_type=resource["primary_type"],
            sanitized_name=resource["sanitized"],
            is_commander=True if resource.get("is_commander") else False,
        )

    @classmethod
    def build_from_filepath(cls, filename):
        with open(f"static/assets/{filename}") as f:
            asset = json.loads(f.read())
            resource = asset["container"]["json_dict"]["card"]

        return cls(
            cmc=resource["cmc"],
            colors=[x.lower() for x in resource.get("color_identity", [])],
            color_identity=resource.get("color_identity"),
            inclusion=resource.get("inclusion"),
            name=resource["name"],
            num_decks=resource.get("num_decks"),
            primary_type=resource.get("primary_type"),
            sanitized_name=resource.get("sanitized"),
            is_commander=True if resource.get("is_commander") else False,
        )

    @property
    def asset(self):
        if self.is_commander:
            return retrieve_asset(f"commanders/{self.sanitized_name}.json")
        else:
            return retrieve_asset(f"cards/{self.sanitized_name}.json")

    @property
    def color_asset(self):
        color_str = "".join(self.color_identity)
        return retrieve_asset(f"commanders/{color_str}.json")


class Deck:
    cards: T.List[Card]
    commander: Card
    themes: T.List[Theme]
    tribe: T.Union[Tribe, None]

    def __init__(self, commander, themes, tribe):
        self.cards = []
        self.commander = commander
        self.themes = themes
        self.tribe = tribe

    def __str__(self):
        return f"""Deck:\n
        Commander: {self.commander.name}\n 
        Themes: {[t.name for t in self.themes]}\n 
        Tribe: {self.tribe.name if self.tribe else "None"}
        Cards: {self.card_count}
        """

    @property
    def card_count(self, card_type=None):
        if card_type:
            cards = [c for c in self.cards if c.primary_type == card_type]
        else:
            cards = self.cards
        return len(cards)

    def add_card(self, card: Card):
        if self.card_is_legal(card):
            self.cards.append(card)

    def card_is_legal(self, card: Card) -> bool:
        # Make sure deck isn't full
        if self.card_count >= 99:
            return False

        # Check if it's a dual commander
        if card.sanitized_name.count("/") > 0:
            return False

        # Check if card is in deck already
        if "Basic Land" not in card.asset["container"]["json_dict"]["card"]["type"]:
            for c in self.cards:
                if c.sanitized_name == card.sanitized_name:
                    return False

        # Check if colors are valid
        card_colors = normalize_colors(card.colors)
        deck_colors = normalize_colors(self.commander.colors)
        if any([c not in deck_colors for c in card_colors]):
            return False

        return True
