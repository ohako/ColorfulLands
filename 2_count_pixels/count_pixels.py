#!/usr/bin/env python3

import colorsys
import io
import json
import sys
from time import sleep

from PIL import Image
import requests


def main() -> None:
    """Given a basic land type (and info files from the previous module), count the colors of pixels.

    Convert each pixel from RGB to HSL.
    A given pixel is 'white' if the lightness value is .85 or above.
    A given pixel is 'blue' if the hue is 240+-30.
    A given pixel is 'black' if the lightness value is .15 or below.
    A given pixel is 'red' if the hue is 0+-30.
    A given pixel is 'green' if the hue is 120+-30.

    I'm not doing anything with the saturation value. Maybe I should.
    """
    land_type = sys.argv[1]
    json_images = []
    with io.open("data/" + land_type + ".json", "rb") as input_stream:
        json_data = json.load(input_stream)
        for json_image in json_data:
            pixels = 0
            light_pixels = 0
            dark_pixels = 0
            non_redness = 0
            non_greenness = 0
            non_blueness = 0
            sleep(0.1)
            with requests.get(json_image["art"], stream=True) as response:
                if not response.ok:
                    print(str(response.status_code) + "\n")
                    print(response.text + "\n")
                    continue
                image = Image.open(response.raw)
                for pixel in image.getdata():
                    red = pixel[0] / 255
                    green = pixel[1] / 255
                    blue = pixel[2] / 255
                    hue, lightness, saturation = colorsys.rgb_to_hls(red, green, blue)
                    hue = hue * 360
                    pixels += 1
                    if lightness >= 0.85:
                        light_pixels += 1
                    elif lightness <= 0.15:
                        dark_pixels += 1
                    non_redness += (360 - hue if hue > 180 else hue) ** 2
                    non_greenness += (120 - hue if hue < 300 else 120 + (360 - hue)) ** 2
                    non_blueness += (240 - hue if hue > 60 else 120 + hue) ** 2
                json_image["white"] = light_pixels / pixels
                json_image["blue"] = non_blueness
                json_image["black"] = dark_pixels / pixels
                json_image["red"] = non_redness
                json_image["green"] = non_greenness
                json_images.append(json_image)
    with open(land_type + "_with_pixel_counts.json", "w") as outfile:
        json.dump(json_images, outfile)


if __name__ == "__main__":
    main()
