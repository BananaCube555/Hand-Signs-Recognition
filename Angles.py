# This script is not needed

import numpy as np 





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
    #



def Anglev2(self):
        angles = []

        for i in range(1, 19): # Its not 1,2 bc we of the line 21. If i = 21 then i + 2 would be incorrect

            p1 = np.array(self.crHand[i])
            p2 = np.array(self.crHand[i + 1])
            p3 = np.array(self.crHand[i + 2])

            v1 = p1 - p2
            v2 = p3 - p2

            l1 = np.linalg.norm(v1)# A norm  of a vector is its length. Linalg stand for linear algebra
            l2 = np.linalg.norm(v2)

            if l1 == 0 or l2 == 0: 
                continue

            cos_theta = np.dot(v1, v2) / (l1 * l2)
            cos_theta = np.clip(cos_theta, -1.0, 1.0)

            angle = np.degrees(np.arccos(cos_theta))
            angles.append(angle)


        print(angles)
        return angles