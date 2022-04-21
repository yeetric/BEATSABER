import cv2
import mediapipe as mp
import time
import random
import math

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()


widthCam,heightCam = 640,480
cap = cv2.VideoCapture(0)
cap.set(3, widthCam)
cap.set(4, heightCam)
pTime = 0


def RNG(a, b):
    return random.randint(a, b)


def main():
    leftEye = (300, 220)
    rightEye = (340, 260)
    score = 0
    BLUEBoxReset= 50
    redBoxReset = 50
    while True:
        BLUEtouching = False
        REDtouching = False
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


        while not BLUEtouching or not REDtouching:
            success, img = cap.read()
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxSize = 50

            cv2.rectangle(img, (0, 0), (widthCam, heightCam), (0, 0, 0), cv2.FILLED) # black background


            results = pose.process(imgRGB)
            # print(results.pose_landmarks)

            if results.pose_landmarks:
                mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS) #overall pose drawing
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    h, w, c = img.shape
                    # print(id, lm)
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if id == 15:
                        leftWristX, leftWristY = cx, cy
                        print("leftWrist", leftWristX, leftWristY)
                    if id==16:
                        rightWristX, rightWristY = cx, cy
                        print("rightWrist", rightWristX, rightWristY)
                    # DRAW BOXES AND TOUCHING SENSE
                    # cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                    if id == 20 or id == 19:  #arms
                        if BLUEBoxReset >= 50:
                            BLUEcoor1 = (RNG(0, widthCam - boxSize), RNG(0, heightCam - boxSize))
                            BLUEcoor2 = (BLUEcoor1[0] + boxSize, BLUEcoor1[1] + boxSize)
                            BLUEmid = (int((BLUEcoor1[0] + BLUEcoor2[0]) / 2), int((BLUEcoor1[1] + BLUEcoor2[1]) / 2))
                            BLUEBoxReset = 0
                        BLUEBoxReset += 1

                        if redBoxReset >= 50:
                            REDcoor1 = (RNG(0, widthCam - boxSize), RNG(0, heightCam - boxSize))
                            REDcoor2 = (REDcoor1[0] + boxSize, REDcoor1[1] + boxSize)
                            REDmid = (int((REDcoor1[0] + REDcoor2[0]) / 2), int((REDcoor1[1] + REDcoor2[1]) / 2))
                            redBoxReset = 0
                        redBoxReset += 1

                        print(id, cx,cy)
                        if id == 20:
                            BLUElength = math.hypot(cx - BLUEmid[0], cy - BLUEmid[1])

                            secondStickRightHandX, secondStickRightHandY = ((cx) + 3*(int(cx-rightWristX)), cy + 3*(int(cy-rightWristY)))
                            cv2.line(img, (cx,cy), (int(secondStickRightHandX),int(secondStickRightHandY)), (255, 0, 0), 2)

                            if BLUElength < boxSize+50:
                                score += 1
                                BLUEtouching = True
                                BLUEBoxReset = 300
                        elif id == 19:
                            secondStickLeftHandX, secondStickLeftHandY = ( (cx) + 3 * (int(cx - leftWristX)), cy + 3 * (int(cy - leftWristY)))
                            print(secondStickLeftHandX, secondStickLeftHandY)
                            cv2.line(img, (cx,cy), (int(secondStickLeftHandX),int(secondStickLeftHandY)), (0, 0, 255), 2)
                            REDlength = math.hypot(cx - REDmid[0], cy - REDmid[1])

                            if REDlength < boxSize + 50:
                                score += 1
                                REDtouching = True
                                redBoxReset = 100
                    try:
                        cv2.circle(img, BLUEmid, 5, (255, 0, 0), cv2.FILLED)
                        cv2.rectangle(img, BLUEcoor1, BLUEcoor2, (255, 0, 0), 2)
                        cv2.circle(img, REDmid, 5, (0, 0, 255), cv2.FILLED)
                        cv2.rectangle(img, REDcoor1, REDcoor2, (0, 0, 255), 2)
                    except:
                        print("hand off screen")
            img = cv2.flip(img, 1)  # flip the frame horizontally
            cv2.putText(img, str(int(score)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
            cv2.imshow("Image", img)
            cv2.waitKey(1)
if __name__ == '__main__':
    main()