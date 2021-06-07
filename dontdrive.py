import playsound
import cv2
import dlib
import imutils
from imutils import face_utils
from imutils.video import VideoStream
import numpy as np
import pandas as pd
import time
import gspread
from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials
scope = ["..."]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "C:\\Users\\Syed Arsalan Amin\\Desktop\\test1\\finalProject\\creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("sleepData").sheet1


# ------------------------------------------------------------------------------
# TODO: values upation to the cloud portion
# l1 = [i for i in range(20)]  # inserting 5 values to the google spreadsheet
# l1
# l2 = []
# for i in l1:
#     l2.append(i)
#     time.sleep(0.2)
#     print(l2[-1:])
#     sheet.insert_row(l2[-1:])

#
# -----------------------------------------------------------------------------
# TODO: Add the header line 'Time Stamp', 'Eye Aspect Ratio', 'Status'

# sheet.insert_row(['Time Stamp', 'Eye Aspect Ratio', 'Status'], 1)
# -----------------------------------------------------------------------------
# TODO: Image processing portion


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

global l1
l1 = []

count = 0

while True:

    count += 1

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
            AREA = w_rect * h_rect

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

    l1.append(ear)
    if count % 200 == 0:
        date = pd.Timestamp.now().strftime("%T - %A - %D ")
        recent_ear = round(l1[-1:][0], 2)
        sheet.insert_row([date, recent_ear, "Keep Driving"
                          if recent_ear >= 0.28 else "Warning!"], 2)

        print(f"Time: {date}, EAR: {recent_ear}", print("Keep Driving")
              if recent_ear >= 0.28 else print("Warning!"))

cv2.destroyAllWindows()
vs.stop()


# sheet.insert_row([round(l1[-1:][0], 3)])
# print(round(l1[-1:][0], 3))

# ------------------------------------------------------------------------------
# TODO: rough work
# date = pd.to_datetime("now").strftime("%T - %A - %D ")
# date
#
# l1
# print(round(l1[-1:][0], 3))
# for i, x in enumerate(l1):
#     if i % 10 == 0:
#         l2.append(x)
#         print(round(l1[-1:][0], 3))
#     else:
#         print("attention!")

# for i, x in enumerate(l1):
#     # sheet.insert_row([x])
#     print(f"{i}, EAR:{round(x, 3)}")

# l1
# i = enumerate(l1, 0)
# l = list(i)
#
# len(l1)
# l[:5]

#
# count = 0
# for i in range(5):
#     count += 1
#     print(count)


# -----------------------------------------------------------------------------
# TODO: this code block prints the value of iteration after certain number
# of iteration

# l = [i for i in range(400)]
# count = 0
#
# list1 = []
# counter1 = 0
#
# while True:
#     while True:
#
#         list1.append(l)
#
#     def print_ind(list, n):
#         count = 0
#         while True:
#             count += 1
#             # print(count)
#
#             for i, x in enumerate(list, count):
#                 if i % n == 0:
#                     print(x)
#             break
#
#     print_ind(list1, 100)
#     break

# ------------------------------------------------------------------------------
# pd.to_datetime("now").strftime("%T - %A - %D ")
# pd.Timestamp.now().strftime("%T - %A - %D ")
