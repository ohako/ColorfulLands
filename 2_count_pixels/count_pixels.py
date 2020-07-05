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
    with io.open(land_type + ".json", "rb") as input_stream:
        json_data = json.load(input_stream)
        for json_image in json_data:
            pixels = 0
            light_pixels = 0
            blue_pixels = 0
            dark_pixels = 0
            red_pixels = 0
            green_pixels = 0
            sleep(0.1)
            image = Image.open(requests.get(json_image["art"], stream=True).raw)
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
                elif saturation <= 0.15:
                    continue
                elif hue <= 15 or hue >= 345:
                    red_pixels += 1
                elif 120 <= hue <= 150:
                    green_pixels += 1
                elif 200 <= hue <= 230:
                    blue_pixels += 1
            json_image["white"] = light_pixels / pixels
            json_image["blue"] = blue_pixels / pixels
            json_image["black"] = dark_pixels / pixels
            json_image["red"] = red_pixels / pixels
            json_image["green"] = green_pixels / pixels
            json_images.append(json_image)
    with open(land_type + "_with_pixel_counts.json", "w") as outfile:
        json.dump(json_images, outfile)


if __name__ == "__main__":
    main()
