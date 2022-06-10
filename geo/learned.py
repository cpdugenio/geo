import os

import xml.etree.ElementTree as ET

from .data import get_learned_countries

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

    for el in xml_root.findall(
            "./ns0:rect[@id='World']",
            namespaces={'ns0': "http://www.w3.org/2000/svg"}):
        xml_root.find('.').remove(el)

    for el in xml_root.findall(
            "./ns0:path[@id='Ocean']",
            namespaces={'ns0': "http://www.w3.org/2000/svg"}):
        xml_root.find('.').remove(el)

    for country in get_learned_countries():
        p = f".//ns0:g[@id='{country}']"
        print(p)
        for group in xml_root.findall(
                p, namespaces={'ns0': "http://www.w3.org/2000/svg"}):
            for el in group.iter():
                el.set("fill", "orange")

    xml_root.write(os.path.join(
        os.path.dirname(__file__),
        "..",
        "outputs",
        "learned.svg"
    ))
