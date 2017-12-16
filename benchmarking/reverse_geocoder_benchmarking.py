import reverse_geocoder as rg
import time
import numpy as np
from mpl_toolkits.basemap import Basemap


coord_list = []

number_of_coords = 1000000

for i in range(0, number_of_coords):
    lat_lon = ((np.random.random_sample() * 180) - 90, (np.random.random_sample() * 360) - 180)

    coord_list.append(lat_lon)

coord_tuple = tuple([(coord[0], coord[1]) for coord in coord_list])

print('random coord list generated')

list_start_time = float(time.time())
# for coord in coord_list:
#     rg.search(coord)
list_end_time = float(time.time())

print('list element wise reverse lookup complete')

tuple_start_time = float(time.time())
result = rg.search(coord_tuple)
tuple_end_time = float(time.time())

print('tuple reverse lookup complete')

bm_instantiation_start_time = float(time.time())
bm = Basemap()   # default: projection='cyl'
bm_instantiation_end_time = float(time.time())

print('Basemap object instantiated')

# measuring how long it takes for is_land() lookups to complete
is_land_start_time = float(time.time())
for coord in coord_list:
    bm.is_land(xpt=coord[1], ypt=coord[0])
is_land_end_time = float(time.time())


list_time = list_end_time - list_start_time
tuple_time = tuple_end_time - tuple_start_time
bm_instantiation_time = bm_instantiation_end_time - bm_instantiation_start_time
is_land_time = is_land_end_time - is_land_start_time

print('list_time = %f' % list_time)
print('tuple_time = %f' % tuple_time)
print('bm_instantiation_time = %f' % bm_instantiation_time)
print('is_land_time = %f' % is_land_time)