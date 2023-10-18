import numpy as np
import matplotlib.pyplot as plt

def unit(vector):
    return vector / np.linalg.norm(vector)

def rotate(vector, axis, theta):
    dot = np.dot(vector, axis)
    cross = np.cross(vector, axis)
    return vector*np.cos(theta) + axis*dot*(1-np.cos(theta)) + cross*np.sin(theta)

def get_perp(vector):
    return unit(np.cross(np.array([1, 0, 0]), vector))

class Screen():
    def __init__(self, size, camera_dist):
        self.size = size
        self.camera_dist = camera_dist
        self.screen = np.zeros(self.size)
        self.center = [int(self.size[i] / 2) for i in (0, 1)]
        self.z_buffer = np.full(self.size, np.inf) # stores z-coordinates for plotted points

    def project(self, coords):
        for point in coords:
            point_z, point_b = point[2], point[3]
            pos = []

            for i in (1, 0): # axes need to be swapped for plotting
                screen_coord = int(point[i] * self.camera_dist / point_z)
                if abs(screen_coord) < int(self.size[i] / 2):
                    pos.append(screen_coord + self.center[i])
                else: # projection beyond the screen
                    pos = []
                    break
                
            if pos and point_z < self.z_buffer[*pos]:
                self.screen.itemset(*pos, point_b)
                self.z_buffer.itemset(*pos, point_z)

    def show(self):
        plt.imshow(self.screen, origin='lower')
        plt.axis('off')
        plt.show()

def rot(axis, t, vector):
    if axis == 'z':
        matrix = np.array([[np.cos(t), -np.sin(t), 0], [np.sin(t), np.cos(t), 0], [0, 0, 1]])
    elif axis == 'y':
        matrix = np.array([[np.cos(t), 0, np.sin(t)], [0, 1, 0], [-np.sin(t), 0, np.cos(t)]])
    elif axis == 'x':
        matrix = np.array([[1, 0, 0], [0, np.cos(t), -np.sin(t)], [0, np.sin(t), np.cos(t)]])
    else:
        return None

    return np.matmul(matrix, vector)

screen = Screen((64, 64), 100)


def transform(vector):
    return rot('x', -np.pi/4, vector)

R_val = 50
r_val = 20

offset = np.array([0, 0, 250])
light=np.array([0, -1, 0])
shape = []

R0 = np.array([R_val, 0, 0])
r0 = np.array([0, r_val, 0])

for a in np.linspace(0, 2*np.pi, 256):
    r = rot('z', a, r0)

    for b in np.linspace(0, 2*np.pi, 256):
        v = rot('y', b, r + R0)
        Tr = transform(rot('y', b, r))
        brightness = - np.dot(unit(light), unit(Tr))
        Tv = transform(v) + offset
        Tv = np.append(Tv, brightness)
        shape.append(Tv)

screen.project(shape)
screen.show()