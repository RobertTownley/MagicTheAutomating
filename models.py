import typing as T
from dataclasses import dataclass


from assets import retrieve_asset, save_asset_for_commander


class Deck:
    pass


class Theme:
    pass


class Tribe:
    pass


@dataclass
class Card:
    # Asset Details
    colors: T.List[str]
    color_identity: T.List[str]
    cmc: int
    inclusion: int
    name: str
    num_decks: int
    sanitized_name: str

    # Deck Details
    is_commander: bool = False

    def __str__(self):
        return self.name

    @classmethod
    def build_from_resource(cls, resource):
        if resource.get("is_commander"):
            save_asset_for_commander(resource["sanitized"])

        return cls(
            cmc=resource["cmc"],
            colors=[x.lower() for x in resource["color_identity"]],
            color_identity=resource["color_identity"],
            inclusion=resource["inclusion"],
            name=resource["name"],
            num_decks=resource["num_decks"],
            sanitized_name=resource["sanitized"],
        )

    @property
    def asset(self):
        return retrieve_asset(f"commanders/{self.sanitized_name}.json")
