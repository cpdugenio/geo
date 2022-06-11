import os
import pprint
import requests

from .iso  import COUNTRY_TO_ISO, PERSONAL_MAPPING

TOKEN = os.environ['NOTION_TOKEN']
DATABASE_ID = 'f526009c2f05441497796059cf1a228c'
REQUEST_URL = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'

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

def get_learned_countries():
    """Returns list of countries in ISO code that is learned.

    Returns:
        list[str]
    """
    db_entries = _get_database_entries()
    countries = [
        title['plain_text']
        for row in db_entries
        for title in row['properties']['Country']['title']
    ]
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
