import reverse_geocoder as rg
import time
import numpy as np

coord_list = []


coords_to_generate = 1000

for i in range(0, coords_to_generate):
    lat_lon = ((np.random.random_sample() * 180) - 90, (np.random.random_sample() * 360) - 180)

    coord_list.append(lat_lon)

coord_tuple = tuple([(coord[0], coord[1]) for coord in coord_list])


list_start_time = float(time.time())
# for coord in coord_list:
#     rg.search(coord)
list_end_time = float(time.time())


tuple_start_time = float(time.time())
result = rg.search(coord_tuple)
tuple_end_time = float(time.time())

list_time = list_end_time - list_start_time

tuple_time = tuple_end_time - tuple_start_time


print('list_time = %f' % list_time)
print('tuple_time = %f' % tuple_time)
