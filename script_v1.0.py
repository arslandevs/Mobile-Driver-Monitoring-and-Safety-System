from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import time
import imutils
import dlib
import cv2
import playsound


def euclidean_dist(ptA, ptB):
    return np.linalg.norm(ptA - ptB)


def eye_aspect_ratio(eye):
    A = euclidean_dist(eye[1], eye[5])
    B = euclidean_dist(eye[2], eye[4])

    C = euclidean_dist(eye[0], eye[3])

    ear = (A + B) / (2.0 * C)

    return ear


EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 14

COUNTER = 0
ALARM_ON = False

detector = cv2.CascadeClassifier(
    "E:\\DataScience & AI\\Projects\\fyp\\finalProject\\haarcascade_frontalface_default.xml")
predictor = dlib.shape_predictor(
    "E:\\DataScience & AI\\Projects\\fyp\\finalProject\\shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

vs = VideoStream(src=0).start()
time.sleep(1.0)

while True:
    frame = vs.read()
    # frame = cv2.imread("C:\\Users\\salman\\Pictures\\face_4.jpeg")
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rects = detector.detectMultiScale(gray, scaleFactor=1.1,
                                      minNeighbors=5, minSize=(30, 30),
                                      flags=cv2.CASCADE_SCALE_IMAGE)

    MAX_AREA = 0.0

    if len(rects) >= 1:

        for (x_rect, y_rect, w_rect, h_rect) in rects:
            AREA = w_rect*h_rect

            if AREA > MAX_AREA:
                MAX_AREA = AREA
                (x, y, w, h) = (x_rect, y_rect, w_rect, h_rect)

        rect = dlib.rectangle(int(x), int(y), int(x + w),
                              int(y + h))

        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        global ear
        ear = (leftEAR + rightEAR) / 2.0

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        if ear < EYE_AR_THRESH:
            COUNTER += 1

            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                # if not ALARM_ON:
                #     ALARM_ON = True
                #     playsound.playsound('buzzer.wav')

                cv2.putText(frame, "ATTENTION!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        else:
            COUNTER = 0
            ALARM_ON = False

        cv2.putText(frame, f"EAR:{ear}", (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    l1 = []
    l1.append(ear)
    for i, x in enumerate(l1):
        if i % 10000000 == 0:
            print(round(l1[-1:][0], 3))
        else:
            print("attention!")
    # print(ear)
    # time.sleep(0.2)

cv2.destroyAllWindows()
vs.stop()
# -----------------------------------------------------------------------------

# TODO: ralph work
round([0.1231312][0])

l1 = [i for i in range(20)]
l1
l2=[]
for i, x in enumerate(l1):
    if i % 3 == 0:
        l2.append(x)
        print(l2[-1:][0])
