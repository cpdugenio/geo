import os

import xml.etree.ElementTree as ET

from .data import get_learned_countries


PATHS_TO_REMOVE = (
    "./ns0:rect[@id='World']",
    "./ns0:path[@id='Ocean']",
    "./ns0:g[@id='labels']",
    "./ns0:g[@id='AQ']",
)


def _get_clean_svg():
    """Returns clean world states svg root (without cruft).

    Returns:
        ElementTree

    """
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

    return xml_root


def _create_modified_svg(group_modification, output_path,
        final_modification=None):
    """For every country in learned countries, apply modification and write.

    Args:
        group_modification (func(ElementTree, Elements)): XML tree and matched
            group.
        final_modification (func(ElementTree)): Final XML tree after group
            modification.

    """
    xml_root = _get_clean_svg()

    for country in get_learned_countries():
        p = f".//ns0:g[@id='{country}']"
        groups = xml_root.findall(p , namespaces={'ns0': "http://www.w3.org/2000/svg"})
        if not groups:
            print(f"Failed to find {country}: {p}")
        for group in groups:
            try:
                group_modification(xml_root, group)
            except Exception as e:
                print(f'Failed to modify "{country}": ({group}) {e}')

    if final_modification:
        final_modification(xml_root)

    xml_root.write(output_path)


def create_learned_svg(args):
    """Create learned.svg to highlight learned countries"""
    def _group_modification(xml_root, group):
        for el in group.iter():
            el.set("fill", "orange")
            el.set("stroke", "blue")

    _create_modified_svg(
        _group_modification,
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "outputs",
            "learned.svg"
        )
    )


def create_unlearned_svg(args):
    """Create unlearned.svg to highlight learned countries"""
    OPACITY = "0.6"

    def _group_modification(xml_root, group):
        group.set("opacity", OPACITY)

    def _final_modification(xml_root):
        for country in xml_root.findall(
                "./ns0:g",
                namespaces={'ns0': "http://www.w3.org/2000/svg"}):
            if country.get("opacity") == OPACITY:
                continue
            for el in country.iter():
                el.set("fill", "red")
                el.set("stroke", "blue")

    _create_modified_svg(
        _group_modification,
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "outputs",
            "unlearned.svg"
        ),
        final_modification=_final_modification
    )


