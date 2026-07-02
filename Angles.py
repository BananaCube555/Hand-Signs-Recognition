# This script is not needed

import numpy as np 


frames = [
    [
        (556, 293), (509, 293), (463, 277), (428, 265), (401, 260),
        (471, 208), (447, 173), (432, 150), (420, 130), (495, 191),
        (477, 145), (465, 117), (456, 93), (522, 188), (511, 142),
        (503, 115), (496, 91), (550, 193), (547, 158), (543, 135),
        (539, 114), (180, 313), (221, 312), (263, 300), (297, 290),
        (323, 285), (256, 233), (281, 196), (294, 171), (305, 149),
        (234, 219), (250, 172), (260, 143), (268, 118), (208, 217),
        (217, 172), (224, 143), (229, 118), (180, 223), (175, 189),
        (171, 166), (170, 145)
    ],
    [
        (179, 312), (221, 312), (263, 299), (297, 290), (322, 284),
        (257, 233), (281, 196), (294, 172), (305, 150), (234, 218),
        (251, 172), (261, 143), (270, 119), (208, 216), (217, 171),
        (225, 143), (231, 118), (180, 222), (175, 188), (171, 165),
        (170, 143), (556, 291), (509, 292), (463, 276), (428, 264),
        (400, 261), (470, 208), (446, 173), (432, 150), (420, 130),
        (495, 191), (476, 145), (465, 117), (455, 93), (522, 187),
        (510, 142), (503, 114), (496, 90), (550, 192), (546, 157),
        (543, 134), (539, 113)
    ],
    [
        (556, 290), (510, 291), (464, 276), (429, 264), (401, 260),
        (471, 208), (447, 172), (432, 150), (420, 129), (495, 191),
        (477, 145), (465, 116), (455, 93), (522, 187), (510, 141),
        (503, 113), (495, 89), (550, 192), (547, 157), (543, 133),
        (539, 112), (179, 311), (221, 311), (263, 299), (297, 289),
        (321, 283), (256, 232), (281, 196), (295, 172), (305, 150),
        (234, 218), (251, 172), (261, 143), (269, 118), (208, 215),
        (217, 171), (224, 142), (230, 117), (180, 222), (175, 188),
        (171, 165), (170, 143)
    ]
]



class HandData:
    def __init__(self):
        self.crHand = []

        self.FinalAngles = []
        
        self.angles = []

    def Angle(self):

        self.angles = []

        
        for f in range(len(frames)):

            frame_angles = []

            # Calculate angles for this frame
            for i in range(1, 18):

                p1 = np.array(frames[f][i])
                p2 = np.array(frames[f][i + 1])
                p3 = np.array(frames[f][i + 2])
                p4 = np.array(frames[f][i + 3])

                v1 = p1 - p2
                v2 = p3 - p2

                v3 = p2 - p3
                v4 = p4 - p3 

                l1 = np.linalg.norm(v1) # A norm  of a vector is its length. Linalg stand for linear algebra
                l2 = np.linalg.norm(v2)
                l3 = np.linalg.norm(v3)
                l4 = np.linalg.norm(v4)

                if l1 == 0 or l2 == 0 or l3 == 0 or l4 == 0:
                    continue

                cos_theta = np.dot(v1, v2) / (l1 * l2)
                cos_theta = np.clip(cos_theta, -1.0, 1.0)

                cos_theta2 = np.dot(v3, v4) / (l3 * l4)
                cos_theta2 = np.clip(cos_theta2, -1.0, 1.0)

                angle1 = np.degrees(np.arccos(cos_theta))
                angle2 = np.degrees(np.arccos(cos_theta2))

                
                frame_angles.append((angle1, angle2))

            
            self.angles.append(frame_angles)

        
        for frame_number, frame in enumerate(self.angles, start=1):
            print(f"\n Frame {frame_number}")
            for angle_pair in frame:
                print(angle_pair)

        return self.angles

    def Smoothing(self):

        # Holds the final averaged frame.
        # Example:
        # [
        #   (178.8,173.1),
        #   (173.1,47.8),
        #   ...
        # ]
        final = []

        # Loop through every angle position.
        #
        # Example:
        #
        # Frame1[0] = (179,171)
        # Frame2[0] = (177,178)
        # Frame3[0] = (179,169)
        #
        # We average these together.
        #
        for angle_index in range(len(self.angles[0])):

            angle1_values = []
            angle2_values = []

            # Collect the same angle from every frame.
            for frame in self.angles:

                angle1_values.append(frame[angle_index][0])
                angle2_values.append(frame[angle_index][1])

            # Average the collected values.
            #
            # This reduces noise from hand tracking.
            average_angle1 = np.mean(angle1_values)
            average_angle2 = np.mean(angle2_values)

            final.append((average_angle1, average_angle2))

        print("\nFinal Averaged Frame:")
        print(final)

        return final


    
p1 = HandData()
angles = p1.Angle()
smoothed = p1.Smoothing()