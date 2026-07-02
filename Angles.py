# This script is not needed

import numpy as np 

# HARD CODED FRAMES
# frames = [
#     [
#         (556, 293), (509, 293), (463, 277), (428, 265), (401, 260),
#         (471, 208), (447, 173), (432, 150), (420, 130), (495, 191),
#         (477, 145), (465, 117), (456, 93), (522, 188), (511, 142),
#         (503, 115), (496, 91), (550, 193), (547, 158), (543, 135),
#         (539, 114), (180, 313), (221, 312), (263, 300), (297, 290),
#         (323, 285), (256, 233), (281, 196), (294, 171), (305, 149),
#         (234, 219), (250, 172), (260, 143), (268, 118), (208, 217),
#         (217, 172), (224, 143), (229, 118), (180, 223), (175, 189),
#         (171, 166), (170, 145)
#     ],
#     [
#         (179, 312), (221, 312), (263, 299), (297, 290), (322, 284),
#         (257, 233), (281, 196), (294, 172), (305, 150), (234, 218),
#         (251, 172), (261, 143), (270, 119), (208, 216), (217, 171),
#         (225, 143), (231, 118), (180, 222), (175, 188), (171, 165),
#         (170, 143), (556, 291), (509, 292), (463, 276), (428, 264),
#         (400, 261), (470, 208), (446, 173), (432, 150), (420, 130),
#         (495, 191), (476, 145), (465, 117), (455, 93), (522, 187),
#         (510, 142), (503, 114), (496, 90), (550, 192), (546, 157),
#         (543, 134), (539, 113)
#     ],
#     [
#         (556, 290), (510, 291), (464, 276), (429, 264), (401, 260),
#         (471, 208), (447, 172), (432, 150), (420, 129), (495, 191),
#         (477, 145), (465, 116), (455, 93), (522, 187), (510, 141),
#         (503, 113), (495, 89), (550, 192), (547, 157), (543, 133),
#         (539, 112), (179, 311), (221, 311), (263, 299), (297, 289),
#         (321, 283), (256, 232), (281, 196), (295, 172), (305, 150),
#         (234, 218), (251, 172), (261, 143), (269, 118), (208, 215),
#         (217, 171), (224, 142), (230, 117), (180, 222), (175, 188),
#         (171, 165), (170, 143)
#     ]
# ]



import numpy as np


class HandData:

    def __init__(self, frames):
        # frames = list of frames
        # each frame = 21 landmarks (x,y)
        self.frames = frames

        # will store raw finger features per frame
        # shape: [frame][5 fingers]
        self.features = []

        # will store smoothed features
        self.smoothed = []

    # ---------------------------------------------------
    # CORE FUNCTION: angle between 3 points
    # A = start, B = joint, C = end
    # ---------------------------------------------------
    def angle(self, a, b, c):

        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        # create vectors
        v1 = a - b
        v2 = c - b

        # compute lengths (magnitude of vectors)
        l1 = np.linalg.norm(v1)
        l2 = np.linalg.norm(v2)

        # avoid division by zero (bad detection cases)
        if l1 == 0 or l2 == 0:
            return 0

        # cosine formula
        cos_theta = np.dot(v1, v2) / (l1 * l2)

        # clamp to avoid floating errors (like 1.0000001)
        cos_theta = np.clip(cos_theta, -1.0, 1.0)

        # convert to degrees
        return np.degrees(np.arccos(cos_theta))

    # ---------------------------------------------------
    # EXTRACT FEATURES (THIS IS THE IMPORTANT PART)
    # turns 21 points → 5 finger values
    # ---------------------------------------------------
    def extract(self):

        self.features = []

        # loop through each frame (time step)
        for frame in self.frames:

            # -------------------------
            # MediaPipe LANDMARK MAP:
            # 0  = wrist
            # 1-4  = thumb
            # 5-8  = index
            # 9-12 = middle
            # 13-16 = ring
            # 17-20 = pinky
            # -------------------------

            wrist = frame[0]

            # -------------------------
            # FINGER ANGLES
            # we measure bending using 3 points:
            # wrist → base → tip
            # -------------------------

            # THUMB (special structure)
            thumb = self.angle(frame[0], frame[2], frame[4])

            # INDEX
            index = self.angle(frame[0], frame[5], frame[8])

            # MIDDLE
            middle = self.angle(frame[0], frame[9], frame[12])

            # RING
            ring = self.angle(frame[0], frame[13], frame[16])

            # PINKY
            pinky = self.angle(frame[0], frame[17], frame[20])

            # store one frame feature vector
            self.features.append([
                thumb,
                index,
                middle,
                ring,
                pinky
            ])

        return self.features

    # ---------------------------------------------------
    # SMOOTHING FUNCTION
    # reduces noise using moving average
    # ---------------------------------------------------
    def smooth(self, window=3):

        self.smoothed = []

        # loop each frame
        for i in range(len(self.features)):

            frame_result = []

            # loop each finger (5 values)
            for j in range(len(self.features[0])):

                values = []

                # look back last "window" frames
                for k in range(max(0, i - window + 1), i + 1):

                    values.append(self.features[k][j])

                # average values over time
                avg = np.mean(values)

                frame_result.append(avg)

            self.smoothed.append(frame_result)

        return self.smoothed

    