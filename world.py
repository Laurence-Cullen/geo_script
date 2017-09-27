#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import division
from mpl_toolkits.basemap import Basemap
import numpy as np
import pandas as pd

bm = Basemap()   # default: projection='cyl'

class World(object):
    def __init__(self, width, height, max_mod_lat):
        self.width = width
        self.height = height
        self.max_mod_lat = max_mod_lat

        self.lat_step = 2 * max_mod_lat / height
        self.lon_step = 360 / width

        self.cells = {}

        self.character_picker = CharacterPicker(script_file_path='./scripts.csv')

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
                self.cells[cell] = self.character_picker.random_character(script='latin')
            else:
                self.cells[cell] = ' '


    def __str__(self):
        string = ''

        for row in range(0, self.height):
            for col in range(0, self.width):
                string += self.cells[(row, col)]
            string += '\n'

        return string

class CharacterPicker(object):
    def __init__(self, script_file_path):
        self.script_data = pd.read_csv(script_file_path)

        print(self.script_data)
        print(self.script_data)


    def random_character(self, script):
        if script in self.script_data['Script'].values:

            script_index = list(self.script_data['Script'].values).index(script)

            characters_in_script = len(self.script_data['Characters'].values[script_index])

            return self.script_data['Characters'][script_index][np.random.randint(0, characters_in_script)]





        raise ValueError('unsupported script')

def main():
    world = World(width=100, height=30, max_mod_lat=85)

    print('World contains ' + str(len(world.cells)) + ' cells')

    world.fill_land()

    print(world)

    # character_picker = CharacterPicker('./scripts.csv')

    print 'ظضذخثتشرقصفسنملكيطحزوهدجب'


if __name__ == '__main__':
    main()