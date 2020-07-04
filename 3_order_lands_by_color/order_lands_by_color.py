#!/usr/bin/env python3

import csv
import io
import json
import sys
from typing import Dict


color = "white"


def sort_by_color(e: Dict) -> float:
    """Sorting function, using a globally-declared color variable."""
    return e[color]


def main() -> None:
    """Given a basic land type and a color (and a data file from the previous module),

    order the lands by how colorful they are.
    """
    land_type = sys.argv[1]
    global color
    color = sys.argv[2]
    with io.open(land_type + "_with_pixel_counts.json", "rb") as input_stream:
        lands = list(json.load(input_stream))
    lands.sort(reverse=True, key=sort_by_color)
    with open("ordered_" + color + "_" + land_type + ".csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        for land in lands:
            csv_writer.writerow([land["uri"], land[color]])


if __name__ == "__main__":
    main()
