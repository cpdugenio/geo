import os
import pprint
import requests

from .iso  import COUNTRY_TO_ISO, PERSONAL_MAPPING

DATABASE_ID = 'f526009c2f05441497796059cf1a228c'
REQUEST_URL = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'
TOKEN = os.environ.get('NOTION_TOKEN')
if not TOKEN:
    try:
        with open(os.path.join(os.path.dirname(__file__), '..', '.SECRET')) as f:
            TOKEN = f.read().strip()
    except:
        raise RuntimeError("Failed to get Notion integration token")

ANKI_DB_COL_COUNTRY = 'Country'
ANKI_DB_COL_TAGS = 'Tags'
ANKI_DB_COL_TITLE = 'title'
ANKI_DB_KEY_NAME = 'name'


def _get_database_entries():
    has_more = True
    start_cursor = None
    results = []
    while has_more:
        data = {}
        if start_cursor:
            data['start_cursor'] = start_cursor
        response = requests.post(
            REQUEST_URL,
            headers={
                "Authorization": f'Bearer {TOKEN}',
                "Notion-Version": "2022-02-22",
            },
            json=data
        )
        response_json = response.json()
        if 'status' in response_json:
            raise RuntimeError(response_json)

        results.extend(response_json['results'])
        has_more = response_json['has_more']
        start_cursor = response_json['next_cursor']

    return results


def _get_row_title(row):
    """Get row plain text title.

    Returns:
        str

    """
    return ''.join(
        title['plain_text']
        for title in row['properties'][ANKI_DB_COL_COUNTRY][ANKI_DB_COL_TITLE]
    )


def get_country_groupings():
    """Returns dict from country grouping to list of countries.

    Returns:
        dict[str, list[str]]

    """
    db_entries = _get_database_entries()
    country_groupings = {}
    for row in db_entries:
        country = _get_row_title(row)
        for tag in row['properties'][ANKI_DB_COL_TAGS]['multi_select']:
            tag_name = tag[ANKI_DB_KEY_NAME]
            country_groupings.setdefault(tag_name, []).append(country)

    return country_groupings


def get_learned_countries():
    """Returns list of countries in ISO code that is learned.

    Returns:
        list[str]
    """
    db_entries = _get_database_entries()
    countries = [_get_row_title(row) for row in db_entries]
    isos = []
    for country in countries:
        try:
            isos.append(
                COUNTRY_TO_ISO[
                    PERSONAL_MAPPING.get(country, country)
                ]
            )
        except KeyError as e:
            print(f"Failed to get iso for {country}")
            raise e
    return isos
