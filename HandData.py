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

    