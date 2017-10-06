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

    def fill_land(self, hard_coded_script=None):
        if hard_coded_script is not None:
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

                if bm.is_land(xpt=self.col_to_lon(cell[1]), ypt=self.row_to_lat(cell[0])):
                    land_cells.append(cell)

                    # local_script = self.character_picker.get_local_script(lat=self.row_to_lat(cell[0]),
                    #                                                       lon=self.col_to_lon(cell[1]))
                    #
                    # print(local_script)

                    # self.cells[cell] = self.character_picker.random_character(script=local_script)

            print(land_cells)

            coords_tuple = [(self.row_to_lat(coord[0]), self.col_to_lon(coord[1])) for coord in land_cells]
            print(coords_tuple)

            print('performing reverse lookup')
            results = rg.search(coords_tuple)

            print(results)

            print('assigning characters')
            for result_index in range(0, len(results)):
                country_code = results[result_index]['cc']

                if country_code in self.character_picker.country_scripts['Country Code'].values:
                    country_code_index = list(self.character_picker.country_scripts['Country Code'].values).index(country_code)

                    script = self.character_picker.country_scripts['Script'][country_code_index]

                    print(script)

                    self.cells[land_cells[result_index]] = self.character_picker.random_character(script=script)

                else:
                    print('unknown country code: %s' % country_code)


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

    def random_character(self, script):
        """Pick a random character from a given script."""
        if script in self.script_characters['Script'].values:

            script_index = list(self.script_characters['Script'].values).index(script)

            character_set = list(self.script_characters['Characters'][script_index].decode("utf-8"))

            characters_in_script = len(character_set)

            character = character_set[np.random.randint(0, characters_in_script)]

            # to deal with hanzi characters being twice the width of other unicode characters, simply delete half of
            # them
            # if script == 'hanzi':
            #     if np.random.randint(0,2) > 0:
            #         character = ''

            # print(character)

            return character

        raise ValueError('unsupported script')


def main():

    character_picker = CharacterPicker(script_character_file_path='./script_characters.csv',
                                       country_scripts_file_path='./country_scripts.csv')

    world = World(width=1000, height=300, max_mod_lat=85, character_picker=character_picker)

    print('World contains ' + str(len(world.cells)) + ' cells')

    world.fill_land(hard_coded_script='latin')

    world_string = world.as_unicode()

    print(world_string)


if __name__ == '__main__':
    main()
