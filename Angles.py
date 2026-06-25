import numpy as np


class Fingers:
    def __init__(self,p5,p6,p7,p8):
        pass


def Angle():
    p5 = np.array([100, 300])
    p6 = np.array([100, 250])
    p7 = np.array([100, 200])

    v1 = p5 - p6
    v2 = p7 - p6

    dot = np.dot(v1, v2) # This is so we can get in the future how similar their direction is but its not acurate since the output can be effected by the size of the vectors
    len1 = np.linalg.norm(v1) # Get the length of the vector
    len2 = np.linalg.norm(v2)

    cos_theta = dot / (len1 * len2) # We devide the output of the dot product so we can find the 
    cos_theta = np.clip(cos_theta, -1.0, 1.0) # We force cos_theta to be between -1 and 1

    angle = np.degrees(np.arccos(cos_theta)) #

    print(angle)
    