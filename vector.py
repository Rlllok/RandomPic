import random
import numpy as np


class Vector:

    def __init__(self, items):
        self.items = np.array(items)
        self.len = len(items)
        self.iter = 0

    def next(self):
        if self.iter >= 0 and self.iter < self.len - 1:
            self.iter += 1
            return self.current()
        else:
            return None

    def current(self):
        return self.items[self.iter]

    def previous(self):
        if self.iter > 0 and self.iter < self.len:
                self.iter -= 1
                return self.current()
        else:
            return None

    def shuffle(self):
        self.iter = 0
        np.random.shuffle(self.items)
        
