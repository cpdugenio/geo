import os

from .data import get_country_groupings



ANKI_GROUPING_TAG_IGNORE = (
    'Africa',
    'Eurasia',
    'Island',
    'Transcontinental',
)

EXPORT_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "outputs",
    "groupings.txt",
)

def create_anki_groupings(args):
    with open(EXPORT_FILE, 'w') as f:
        for grouping, countries in get_country_groupings().items():
            if grouping in ANKI_GROUPING_TAG_IGNORE:
                continue
            fcountries = ''.join(f'<li>{country}</li>' for country in countries)
            f.write(
                f"({len(countries)}) {grouping};<ul>{fcountries}</ul>\n"
            )


