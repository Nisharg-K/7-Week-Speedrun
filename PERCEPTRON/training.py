#This will be test dataset for training the model
import random


class Point:

    def __init__(self, canvas_width, canvas_height):
        self.x = random.uniform(0, canvas_width)
        self.y = random.uniform(0, canvas_height)
    def label(self):
        return 1 if self.y > self.x else 0
    
