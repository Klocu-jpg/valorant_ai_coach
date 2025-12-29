import numpy as np
from mss import mss

class ScreenCapturer:
    def __init__(self):
        self.sct = mss()
        self.monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

    def capture_frame(self):
        img = self.sct.grab(self.monitor)
        return np.array(img)