import numpy as np

def pulse(t):
    SPEED_FACTOR=0.8
    SIZE_VARIANCE=0.1
    return 1 + SIZE_VARIANCE*np.sin(2*np.pi*t*SPEED_FACTOR)

def fadeout(t):
    return max(0, 1-t/3)

