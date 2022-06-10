import os

import svgutils.transform as sg

from .data import get_learned_countries

def create_learned_svg(args):
    fig = sg.fromfile(os.path.join(
        os.path.dirname(__file__),
        "..",
        "ext",
        "simple-world-map",
        "world-map.svg"
    ))

    for country in get_learned_countries():
        try:
            country_fig = fig.find_id(country)
        except IndexError:
            print(f"Failed to find {country} in map")
        country_fig.root.set("fill", "orange")

    fig.save(os.path.join(
        os.path.dirname(__file__),
        "..",
        "outputs",
        "learned.svg"
    ))
