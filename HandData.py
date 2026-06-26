from main import H1points, H2points, Allpoints
import numpy as np

class HandData:
    def __init__(self):
        self.crHand = []

    def Hand(self):
        self.crHand = Allpoints[:21]

    def Normalize(self):
        pass

    def Angle(self):
        angles = []

        for i in range(1, 19):

            p1 = np.array(self.crHand[i])
            p2 = np.array(self.crHand[i + 1])
            p3 = np.array(self.crHand[i + 2])

            v1 = p1 - p2
            v2 = p3 - p2

            l1 = np.linalg.norm(v1)
            l2 = np.linalg.norm(v2)

            if l1 == 0 or l2 == 0:
                continue

            cos_theta = np.dot(v1, v2) / (l1 * l2)
            cos_theta = np.clip(cos_theta, -1.0, 1.0)

            angle = np.degrees(np.arccos(cos_theta))
            angles.append(angle)

        return angles