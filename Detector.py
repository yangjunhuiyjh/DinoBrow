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
        print("detector started")
        _thread.start_new_thread(self.readFrame, ())

    def readFrame(self):
        print("reading new frame")
        cap = cv2.VideoCapture(0)
        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            frame = imutils.resize(frame, width=300)

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

    def getAvePoints(self):
        face_ave_height = np.mean(self.coordinates[:, 1], axis = 0)
        brow_ave_height = np.mean(self.coordinates[18:28, 1], axis = 0)
        print(face_ave_height, brow_ave_height)
        return (face_ave_height, brow_ave_height)

if __name__ == "__main__":
    detector = Detector()
    while True:
        detector.getAvePoints()