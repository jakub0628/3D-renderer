import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

def unit(vector):
    return vector / np.linalg.norm(vector)

def rot(axis, angle, vector):
    s = np.sin(angle)
    c = np.cos(angle)
    matrix = np.array({
        'x' : [[1, 0, 0], [0, c, -s], [0, s, c]],
        'y' : [[c, 0, s], [0, 1, 0], [-s, 0, c]],
        'z' : [[c, -s, 0], [s, c, 0], [0, 0, 1]]
    }[axis])
    return np.matmul(matrix, vector)

class Screen():
    def __init__(self, size, camera_dist):
        self.size = size
        self.camera_dist = camera_dist
        self.center = [int(self.size[i] / 2) for i in (0, 1)]
        self.clear()
        self.create_canvas()

    def create_canvas(self):
        self.fig, self.ax = plt.subplots()
        self.artists = []

    def clear(self):
        self.screen = np.full(self.size, -2.0)
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

    def draw(self):
        self.fig.patch.set_visible(False)
        self.ax.axis('off')
        container = [self.ax.imshow(self.screen, origin='lower')]
        self.artists.append(container)

    def ascii(self):
        for row in self.screen:
            for val in row:
                if val == -2:
                    pixel = ' '
                else:
                    pixel_val = int(5.5 * (val+1)) # [-1, 1] -> [0, 11]
                    pixel = '.,-~:;=!*#$@'[pixel_val]
                print(pixel, end='')
            print('')
        print('\x1b[H') # ANSI terminal screen flush

    def animate(self, body, frames, fps, n_rotations=[0.5, 1, 1.5]):
        for f in range(frames):
            print(f'{f} / {frames}')
            self.clear()
            body.rotation = [2*np.pi * f*n/frames for n in n_rotations]
            self.project(body.draw())
            self.draw()

        anim = animation.ArtistAnimation(fig=self.fig, artists=self.artists)
        anim.save('donut.gif', writer=animation.FFMpegWriter(fps=fps))


class Torus():
    def __init__(self, rotation=[0, 0, 0], position=[0, 0, 250], R_val=50, r_val=20, light=[0, -1, 0]):
        self.rotation = np.array(rotation)
        self.position = np.array(position)
        self.R0 = np.array([R_val, 0, 0])
        self.r0 = np.array([0, r_val, 0])
        self.light = np.array(light)

    def draw(self):
        points = []
        for a in np.linspace(0, 2*np.pi, 256):
            r = rot('z', a, self.r0) # create a circle

            for b in np.linspace(0, 2*np.pi, 256):
                v = rot('y', b, r + self.R0) # move circle from the rotation axis by R0 and rotate
                Tr = self.transform(rot('y', b, r)) # rotate and transform the circle drawing vector (surface normal)
                brightness = - np.dot(unit(self.light), unit(Tr)) # calculate lighting

                Tv = self.transform(v) + self.position # transform and move the entire torus away from the screen
                Tv = np.append(Tv, brightness)
                points.append(Tv)

        return points
    
    def transform(self, vector):
        for axis in range(3):
            angle = self.rotation[axis]
            vector = rot('xyz'[axis], angle, vector)
        return vector

screen = Screen((64, 64), 100)
screen.animate(Torus(), 120, 30)