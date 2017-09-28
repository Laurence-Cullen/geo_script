#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from mpl_toolkits.basemap import Basemap
import reverse_geocoder as rg
import numpy as np
import pandas as pd

bm = Basemap()   # default: projection='cyl'



class World(object):
    def __init__(self, width, height, max_mod_lat, character_picker):
        self.width = width
        self.height = height
        self.max_mod_lat = max_mod_lat

        self.lat_step = 2 * max_mod_lat / height
        self.lon_step = 360 / width

        self.cells = {}

        self.character_picker = character_picker

        for row in range(0, self.height):
            for col in range(0, self.width):
                self.cells[(row, col)] = ''

    def row_to_lat(self, row):
        return self.max_mod_lat - row * self.lat_step

    def col_to_lon(self, col):
        return -180 + col * self.lon_step

    def fill_land(self):
        for cell in self.cells.keys():
            if bm.is_land(xpt=self.col_to_lon(cell[1]), ypt=self.row_to_lat(cell[0])):

                local_script = self.character_picker.get_local_script(lat=self.row_to_lat(cell[0]),
                                                                      lon=self.col_to_lon(cell[1]))

                print(local_script)

                self.cells[cell] = self.character_picker.random_character(script=local_script)
            else:
                self.cells[cell] = ' '

    def as_unicode(self):
        string = ''

        for row in range(0, self.height):
            for col in range(0, self.width):
                string += self.cells[(row, col)]
            string += '\n'

        return string

    def __str__(self):
        string = ''

        for row in range(0, self.height):
            for col in range(0, self.width):
                string += self.cells[(row, col)]
            string += '\n'

        return string


class CharacterPicker(object):
    def __init__(self, script_character_file_path, country_scripts_file_path):
        self.script_characters = pd.read_csv(script_character_file_path)
        self.country_scripts = pd.read_csv(country_scripts_file_path, keep_default_na=False)

        # print(self.script_characters)


    def get_local_script(self, lat, lon):
        """Determine what script predominates in a local area."""
        results = rg.search(geo_coords=(lat, lon))

        country_code = results[0]['cc']

        if country_code in self.country_scripts['Country Code'].values:
            country_code_index = list(self.country_scripts['Country Code'].values).index(country_code)

            return self.country_scripts['Script'][country_code_index]

        print(self.country_scripts['Country Code'].values)
        raise ValueError('unknown country code: %s' % country_code)

    def random_character(self, script):
        """Pick a random character from a given script."""
        if script in self.script_characters['Script'].values:

            script_index = list(self.script_characters['Script'].values).index(script)

            character_set = list(self.script_characters['Characters'][script_index].decode(("utf-8")))

            characters_in_script = len(character_set)

            character = character_set[np.random.randint(0, characters_in_script)]

            print(character)

            return character

        raise ValueError('unsupported script')


def main():

    character_picker = CharacterPicker(script_character_file_path='./script_characters.csv',
                                       country_scripts_file_path='./country_scripts.csv')

    world = World(width=300, height=90, max_mod_lat=85, character_picker=character_picker)

    print('World contains ' + str(len(world.cells)) + ' cells')

    world.fill_land()

    world_string = world.as_unicode()

    print(world_string)




if __name__ == '__main__':
    main()
