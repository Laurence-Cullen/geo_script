#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from mpl_toolkits.basemap import Basemap  # conda install basemap
import reverse_geocoder as rg  # pip install reverse_geocoder
import numpy as np
import pandas as pd

bm = Basemap()   # default: projection='cyl'

class World(object):
    """
    Builds up a string which maps to a mercator projection of the Earth's land masses, characters over land will
    be represented by unicode characters from scripts used in the local geographical area. Characters over the sea are
    represented by space characters.
    """
    def __init__(self, width, height, character_picker, max_absolute_lat=83.0):
        self.width = width
        self.height = height
        self.max_absolute_lat = max_absolute_lat

        # calculating the latitude and longitude resolution from the given
        self.lat_step = 2 * max_absolute_lat / height
        self.lon_step = 360 / width

        # cells holds the characters which represent the part of the world covered by the grid cell coordinates tuple
        # (row, col)
        self.cells = {}

        # loads in provided character picker
        self.character_picker = character_picker

        # initialising every grid cell location with an empty string so dictionary keys can be iterated through to
        # access every grid cell
        for row in range(0, self.height):
            for col in range(0, self.width):
                self.cells[(row, col)] = ''

    def row_to_lat(self, row):
        """Converts a row position on a mercator projection into a latitude value."""
        return self.max_absolute_lat - row * self.lat_step

    def col_to_lon(self, col):
        """Converts a column position on a mercator projection into a longitude value."""
        return -180 + col * self.lon_step

    def fill_land(self, hard_coded_script=None):
        """
        Fills in the cells dictionary keys of mercator locations with a space character if it is over the sea or
        with a unicode script character if it is over land.
        """
        if hard_coded_script is not None:
            # if script to select characters from is hardcoded only take characters from this script regardless of which
            # country the land being painted is within
            for cell in self.cells.keys():
                self.cells[cell] = ' '

                if bm.is_land(xpt=self.col_to_lon(cell[1]), ypt=self.row_to_lat(cell[0])):
                    self.cells[cell] = self.character_picker.random_character(script=hard_coded_script)
                else:
                    self.cells[cell] = ' '

        else:
            land_cells = []

            print('determining where land is present')

            for cell in self.cells.keys():
                self.cells[cell] = ' '

                # using base_map to check if a given cell location is over land or sea
                if bm.is_land(xpt=self.col_to_lon(cell[1]), ypt=self.row_to_lat(cell[0])):

                    land_cells.append(cell)

            # print(land_cells)

            # converting (row, col) tuples into (lat, lon) tuples for reverse geocoder to work with
            lat_lon_land_tuples = [(self.row_to_lat(coord[0]), self.col_to_lon(coord[1])) for coord in land_cells]
            print(lat_lon_land_tuples)

            print('performing reverse lookup')

            # finding the country each coordinate tuple is within using the reverse geocoder
            results = rg.search(lat_lon_land_tuples)

            print(results)

            print('assigning characters')

            # iterating through the results of reverse geocoding
            for result_index in range(0, len(results)):
                # extracting the country code from the reverse geocoder results
                country_code = results[result_index]['cc']

                if country_code in self.character_picker.country_codes:
                    # getting script used within country associated with the given country_code
                    script = self.character_picker.get_script_from_country_code(country_code)
                    print(script)
                    self.cells[land_cells[result_index]] = self.character_picker.random_character(script=script)
                else:
                    raise ValueError('unknown country code: %s' % country_code)

    def as_unicode(self):
        string = ''

        for row in range(0, self.height):
            for col in range(0, self.width):
                string += self.cells[(row, col)]
            string += '\n'

        return string

    def __str__(self):
        """Stitches together characters in each cell location to form a single string."""
        string = ''

        for row in range(0, self.height):
            for col in range(0, self.width):
                string += self.cells[(row, col)]
            string += '\n'

        return string


class CountryScriptCharacterMapper(object):
    """A utility that can map from a country to a script and from a script to its constituent characters."""
    def __init__(self, script_character_file_path, country_scripts_file_path):
        # loading file which maps from a script to the characters that comprise it
        self.script_characters = pd.read_csv(script_character_file_path)

        # mapping from countries and country codes to the scripts used by those countries
        self.country_scripts = pd.read_csv(country_scripts_file_path, keep_default_na=False)

    def random_character(self, script):
        """Pick a random character from a given script."""
        if script in self.script_characters['Script'].values:

            script_index = list(self.script_characters['Script'].values).index(script)

            character_set = list(self.script_characters['Characters'][script_index].decode("utf-8"))

            # selecting random character from all characters within script
            characters_in_script = len(character_set)
            character = character_set[np.random.randint(0, characters_in_script)]

            # TODO find a more elegant solution to double width characters
            # to deal with hanzi characters being twice the width of other unicode characters, simply delete half of
            # them
            # if script == 'hanzi':
            #     if np.random.randint(0,2) > 0:
            #         character = ''

            # print(character)

            return character

        raise ValueError('unsupported script')

    @property
    def country_codes(self):
        return self.country_scripts['Country Code'].values

    def get_script_from_country_code(self, country_code):
        """Maps from a country code to the script used in that country."""
        country_code_index = list(self.country_scripts['Country Code'].values).index(country_code)
        return self.country_scripts['Script'][country_code_index]


def main():
    # instantiating CharacterPicker with hand built files which map from a script to the characters that comprise it and
    # another file which maps from a country to the script most commonly used within that country
    character_picker = CountryScriptCharacterMapper(script_character_file_path='./script_characters.csv',
                                                    country_scripts_file_path='./country_scripts.csv')

    world = World(width=300, height=100, character_picker=character_picker, max_absolute_lat=85)

    print('World contains ' + str(len(world.cells)) + ' cells')

    world.fill_land()

    world_string = world.as_unicode()

    print(world_string)


if __name__ == '__main__':
    main()
