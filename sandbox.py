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
            pos = [int(point[i] * self.camera_dist / point_z) + self.center[i] for i in (1, 0)]
            # axes need to be swapped for plotting

            if point_z < self.z_buffer[*pos]:
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

screen = Screen((500, 500), 200)

# ellipse
# shape = [np.array([200*np.sin(t), 500*np.cos(t), 6]) for t in np.linspace(0, 2*np.pi, 1000)]

# rails
# shape = [np.array([-200, -200, 200+t]) for t in np.linspace(0, 500, 1000)] + [np.array([200, -200, 200+t]) for t in np.linspace(0, 500, 1000)]

# tilted square
# shape = [np.array([x, y, 10+0.01*y]) for x in np.linspace(-300, 300, 500) for y in np.linspace(0, 300, 500)]

# circle by rotation
# shape = []
# for t in np.linspace(0, 2*np.pi, 500):
#     rot = np.array([[np.cos(t), -np.sin(t), 0], [np.sin(t), np.cos(t), 0], [0, 0, 1]])
#     init_vector = np.array([300, 300, 10])
#     shape.append(np.matmul(rot, init_vector))

# sphere
# shape = []
# vector = np.array([200, 0, 0])
# offset = np.array([0, 0, 300])
# for t in np.linspace(0, 2*np.pi, 1000):
#     rot_z = np.array([[np.cos(t), -np.sin(t), 0], [np.sin(t), np.cos(t), 0], [0, 0, 1]])
#     for b in np.linspace(0, np.pi, 1000):
#         rot_y = np.array([[np.cos(b), 0, np.sin(b)], [0, 1, 0], [-np.sin(b), 0, np.cos(b)]])
#         shape.append(np.matmul(rot_y, np.matmul(rot_z, vector)) + offset)

# cylinder
# shape = []
# vector = np.array([200, 0, 0])
# offset = np.array([0, -100, 300])
# for b in np.linspace(0, 2*np.pi, 500):
#     rot_y = np.array([[np.cos(b), 0, np.sin(b)], [0, 1, 0], [-np.sin(b), 0, np.cos(b)]])
#     for dy in np.linspace(0, -20, 500):
#         shape.append(np.matmul(rot_y, vector) + [0, dy, 0] + offset)

# torus
# shape = []
# radius = np.array([50, 0, 0])
# offset = np.array([0, 0, 250])
# for a in np.linspace(0, 2*np.pi, 100):
#     for b in np.linspace(0, 2*np.pi, 100):
#         v = rot('z', a, radius)
#         v = rot('y', b, v + [100, 0, 0])
#         v = rot('x', -np.pi/4, v)
#         shape.append(v + offset)

def transform(vector):
    return rot('x', -np.pi/4, vector)

R_val = 100
r_val = 50

offset = np.array([0, 0, 250])
light=np.array([0, -1, 0])
shape = []

R0 = np.array([R_val, 0, 0])
r0 = np.array([0, r_val, 0])

for a in np.linspace(0, 2*np.pi, 500):
    r = rot('z', a, r0)

    for b in np.linspace(0, 2*np.pi, 500):
        v = rot('y', b, r + R0)
        Tr = transform(rot('y', b, r))
        brightness = - np.dot(unit(light), unit(Tr))
        Tv = transform(v) + offset
        Tv = np.append(Tv, brightness)
        shape.append(Tv)

screen.project(shape)
screen.show()