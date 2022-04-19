import cv2
import mediapipe as mp
import time
import random

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

widthCam,heightCam = 640,480
cap = cv2.VideoCapture(0)
cap.set(3, widthCam)
cap.set(4, heightCam)
pTime = 0


def RNG(min, max):
    return random.randint(min, max)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            print(id, lm)
            cx, cy = int(lm.x * widthCam), int(lm.y * heightCam)
            cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime


    cv2.imshow("Image", img)
    cv2.waitKey(1)