import random


COLOR_CODES = [
    "b",
    "g",
    "r",
    "w",
    "u",
    # 2 Color
    "wu",
    "ub",
    "br",
    "rg",
    "gw",
    "wb",
    "ur",
    "bg",
    "rw",
    "gu",
    # 3 Color
    "wub",
    "ubr",
    "brg",
    "gwu",
    "wbg",
    "urw",
    "bgu",
    "rwb",
    "gur",
    # 4 Color
    "wubr",
    "ubrg",
    "rgwu",
    "gwub",
    "wubrg",
    "colorless",
]

# How likely a certain # of colors should be to be chosen
LIKELIHOOD_MAP = [
    [1, 2],
    [2, 4],
    [3, 3],
    [4, 2],
    [5, 1],
]


def choose_random_colors():
    """Select a random number, then that number of random colors


    TODO: Deduping random.choices biases towards fewer colors
    """
    return random.choice(COLOR_CODES)


def normalize_colors(theme_colors):
    if type(theme_colors) == str:
        # "ur"
        parts = list(theme_colors)
    elif type(theme_colors) == list:
        if len(theme_colors) == 1:
            # ['ruw']
            parts = list(theme_colors[0])
        else:
            parts = theme_colors
    elif type(theme_colors) == dict:
        parts = list(theme_colors["icons"])
    else:
        raise Exception(f"Unknown type {type(theme_colors)}")
    parts = [c.lower() for c in parts]
    return "".join(sorted(parts))
