import numpy as np
import matplotlib.pyplot as plt

def unit(vector):
    return vector / np.linalg.norm(vector)

def rot(axis, angle, vector):
    s = np.sin(angle)
    c = np.cos(angle)
    matrix = np.array({
        'z' : [[c, -s, 0], [s, c, 0], [0, 0, 1]],
        'y' : [[c, 0, s], [0, 1, 0], [-s, 0, c]],
        'x' : [[1, 0, 0], [0, c, -s], [0, s, c]]
    }[axis])
    return np.matmul(matrix, vector)

def spin(param, vector):
    vector = rot('x', param/10, vector)
    vector = rot('y', param/15, vector)
    vector = rot('z', param/20, vector)
    return vector

class Screen():
    def __init__(self, size, camera_dist):
        self.size = size
        self.camera_dist = camera_dist
        self.center = [int(self.size[i] / 2) for i in (0, 1)]
        self.clear()

    def clear(self):
        self.screen = np.zeros(self.size)
        self.z_buffer = np.full(self.size, np.inf) # stores z-coordinates for plotted points

    def project(self, coords):
        for point in coords:
            pos = []

            for i in (1, 0): # axes need to be swapped for plotting
                screen_coord = int(point[i] * self.camera_dist / point[2])
                if abs(screen_coord) < int(self.size[i] / 2):
                    pos.append(screen_coord + self.center[i])
                else: # projection beyond the screen
                    pos = []
                    break
                
            if pos and point[2] < self.z_buffer[*pos]: # closer than the previous object mapping to this pixel
                self.screen.itemset(*pos, point[3])
                self.z_buffer.itemset(*pos, point[2])

    def show(self, index):
        plt.imshow(self.screen, origin='lower')
        plt.axis('off')
        plt.savefig(f'{index}.png')
        # plt.show()

    def ascii(self):
        for row in self.screen:
            # print('')
            for val in row:
                pixel_val = int(10 * (val+1) / 2) # [-1, -1] -> [0, 4]
                # pixel = ' ░▒▓█'[pixel_val]
                pixel = " .:-=+*#%@"[pixel_val]
                print(pixel, end='')
            print('')

class Torus():
    def __init__(self, t=0, R_val=50, r_val=20, offset_val=250, light=np.array([0, -1, 0])):
        self.t = t
        self.R0 = np.array([R_val, 0, 0])
        self.r0 = np.array([0, r_val, 0])
        self.offset = np.array([0, 0, offset_val])
        self.light = light

    def draw(self):
        points = []
        for a in np.linspace(0, 2*np.pi, 256):
            r = rot('z', a, self.r0) # create a circle

            for b in np.linspace(0, 2*np.pi, 256):
                v = rot('y', b, r + self.R0) # move circle from the rotation axis by R0 and rotate
                Tr = self.transform(rot('y', b, r)) # rotate and transform the circle drawing vector (surface normal)
                brightness = - np.dot(unit(self.light), unit(Tr)) # calculate lighting

                Tv = self.transform(v) + self.offset # transform and move the entire torus away from the screen
                Tv = np.append(Tv, brightness)
                points.append(Tv)

        return points

    def transform(self, vector):
        vector = rot('x', self.t/10, vector)
        vector = rot('y', self.t/15, vector)
        vector = rot('z', self.t/20, vector)
        return vector

screen = Screen((64, 64), 100)
torus = Torus()

for t in range(5):
    screen.clear()
    torus.t = t
    screen.project(torus.draw())
    screen.ascii()
    # screen.show(t)