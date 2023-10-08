import numpy as np
import matplotlib.pyplot as plt

class Screen():
    def __init__(self, size, distance):
        self.size = size
        self.distance = distance
        self.screen = np.zeros(self.size)
        self.origin = [int(self.size[i] / 2) for i in (0, 1)]

    def project(self, coords):
        for point in coords:
            scale = self.distance / point[2]
            pos = [int(point[i] * scale) + self.origin[i] for i in (1, 0)]
            # axes need to be swapped for plotting
            self.screen.itemset(*pos, 1)

    def show(self):
        plt.imshow(self.screen, origin='lower')
        plt.axis('off')
        plt.show()

screen = Screen((100, 100), 5)

shape = [np.array([20*np.sin(t), 50*np.cos(t), 6]) for t in np.linspace(0, 2*np.pi, 1000)]

screen.project(shape)
screen.show()