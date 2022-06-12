import json
import os

WORLD_MAP_JSON_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "ext",
    "SVG-World-Map",
    "src",
    "country-data.json"
)

with open(WORLD_MAP_JSON_PATH) as f:
    WORLD_MAP_JSON = json.load(f)

COUNTRY_TO_ISO = {
    name: k
    for k, v in WORLD_MAP_JSON.items()
    for name in (v['name'], v.get('altnames')) if name
}

PERSONAL_MAPPING = {
    "Holy See (Vatican City)": "Holy See",
}
