import _thread
import time
import numpy as np
import cv2
import dlib
import imutils

class Detector():
    def __init__(self):
        self.coordinates = np.zeros((68,2))
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.lastFrame = None
        print("detector started")
        _thread.start_new_thread(self.readFrame, ())


    def readFrame(self):
        print("reading new frame")
        cap = cv2.VideoCapture(0)
        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            frame = imutils.resize(frame, width=300)
            self.lastFrame = frame

            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.readKeyPoints(gray)

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    def readKeyPoints(self, image):
        rects = self.detector(image, 1)
        for (i, rect) in enumerate(rects):
            # determine the facial landmarks for the face region, then
            # convert the landmark (x, y)-coordinates to a NumPy array
            shape = self.predictor(image, rect)
            for i in range(0, 68):
                self.coordinates[i] = (shape.part(i).x/300, shape.part(i).y/300)

    def getKeyPoints(self):
        print("getter", self.coordinates)
        return self.coordinates

    def getData(self):
        coor = np.copy(self.coordinates)

        face_max = np.amax(coor[:, 1])
        face_min = np.amin(coor[:, 1])

        if face_max == face_min:
            return None

        left_dist_to_eye = coor[37,1] - coor[19,1]
        right_dist_to_eye = coor[44,1] - coor[24,1]

        ave_dist_to_eye = (left_dist_to_eye + right_dist_to_eye) / 2
        return ave_dist_to_eye/(face_max-face_min)

    def getLastFrame(self):
        return self.lastFrame

if __name__ == "__main__":
    detector = Detector()
    while True:
        detector.getData()