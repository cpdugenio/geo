import os

import xml.etree.ElementTree as ET

from .data import get_learned_countries


PATHS_TO_REMOVE = (
    "./ns0:rect[@id='World']",
    "./ns0:path[@id='Ocean']",
    "./ns0:g[@id='labels']",
    "./ns0:g[@id='AQ']",
)


def create_learned_svg(args):
    xml_root = ET.parse(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "ext",
            "SVG-World-Map",
            "src",
            "world-states.svg"
        )
    )

    for path in PATHS_TO_REMOVE:
        for el in xml_root.findall(
                path,
                namespaces={'ns0': "http://www.w3.org/2000/svg"}):
            xml_root.find('.').remove(el)

    for country in get_learned_countries():
        p = f".//ns0:g[@id='{country}']"
        groups = xml_root.findall(p , namespaces={'ns0': "http://www.w3.org/2000/svg"})
        if not groups:
            print(f"Failed to find {country}: {p}")
        for group in groups:
            for el in group.iter():
                el.set("fill", "orange")
                el.set("stroke", "blue")

    xml_root.write(os.path.join(
        os.path.dirname(__file__),
        "..",
        "outputs",
        "learned.svg"
    ))
