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
