import numpy as np

d = 4

point = np.array([0, 4, 6])

def map_to_screen(position):
    return position[:2] * d / position[2]

print(map_to_screen(point))