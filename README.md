# ColorfulLands

This is a series of python scripts that can determine the 'colorosity' of Magic: the Gathering basic lands.

I specifically wrote it to discover the 'bluest' Mountain card. If you don't feel like running all this code yourself, you can just look at the ordered lands folder and see my results. 

Oh, and I should mention that all of the card image art that I've been running against is copyrighted by Wizards of the Coast or sometimes by other artists, and not me. I think I have adhered to Scryfall's image use policy, but in any case the Scryfall people haven't endorsed, approved of, or are even aware of this bit of software.

To run this yourself, your python requires the poetry meta-dependency. Run ```python -m pip install poetry``` if you haven't already, and then from the ```app``` folder you should be able to run ```poetry install```. Then you should be able to run any of these scripts from their directories by entering a ```poetry shell```.