
import numpy as np
from HandTracking import Allpoints


#Allpoints = [(195, 331), (247, 342), (306, 325), (350, 311), (383, 306), (303, 253), (338, 215), (358, 191), (376, 170), (280, 232), (309, 181), (327, 152), (343, 127), (250, 223), (272, 173), (287, 143), (302, 118), (217, 225), (224, 185), (230, 159), (238, 135)]



class HandData:
    def __init__(self):
        self.crHand = []

    def Hand(self):
        self.crHand = Allpoints[:21]


    def Angle(self):
        angles = []

        for i in range(1, 19): # Its not 1,2 bc we of the line 21. If i = 21 then i + 2 would be incorrect

            p1 = np.array(self.crHand[i])
            p2 = np.array(self.crHand[i + 1])
            p3 = np.array(self.crHand[i + 2])
            

            v1 = p1 - p2
            v2 = p3 - p2

            l1 = np.linalg.norm(v1) # A norm  of a vector is its length. Linalg stand for linear algebra
            l2 = np.linalg.norm(v2)

            if l1 == 0 or l2 == 0:
                continue

            cos_theta = np.dot(v1, v2) / (l1 * l2) # Mesures how align the vectors are and then we normalize by deviding by the whole length
            cos_theta = np.clip(cos_theta, -1.0, 1.0) # Computers may return floats like 1.000000001 but with clip we get 1 or 0 exacly

            angle = np.degrees(np.arccos(cos_theta))
            angles.append(angle)


        print(angles)
        return angles




p1 = HandData()
p1.Hand()
angles = p1.Angle()

print(angles)