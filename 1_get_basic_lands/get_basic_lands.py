#!/usr/bin/env python3

import json
import sys
from time import sleep
from typing import List

import requests


def request_card_data(data_page: str) -> List:
    """Get card information from scryfall. Recursive, in case of multiple-page returns."""
    output = []
    sleep(0.1)
    response = requests.get(data_page)
    if response.status_code == 200:
        cards_json = response.json()
        has_more = cards_json["has_more"]
        for card in cards_json["data"]:
            card_json = {}
            card_json["id"] = card["id"]
            card_json["uri"] = card["scryfall_uri"]
            card_json["art"] = card["image_uris"]["art_crop"]
            output.append(card_json)
        if has_more and "next_page" in cards_json:
            next_page = cards_json["next_page"]
            output.extend(request_card_data(next_page))
    return output


def main() -> None:
    """Given a basic land type, find all the non-fullart, non-snow basic lands of that type from scryfall."""
    land_type = sys.argv[1]
    card_data = request_card_data(
        "https://api.scryfall.com/cards/search?q=type%3Abasic+type%3A"
        + land_type
        + "+unique%3Aart+in%3Apaper+not%3Afullart+-type%3Asnow+-set%3Aana+-set%3Asld+-set%3Apana"
    )
    with open(land_type + ".json", "w") as outfile:
        json.dump(card_data, outfile)


if __name__ == "__main__":
    main()
