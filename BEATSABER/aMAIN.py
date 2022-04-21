import math
import random
from pygame import mixer #sounds
import cv2 #images
import mediapipe as mp #trained models for landmark detection

mixer.init() # play sounds init

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose() #initialize pose

widthCam, heightCam = 640, 480 #width height opencv
cap = cv2.VideoCapture(0) #open camera
cap.set(3, widthCam) #set camera width
cap.set(4, heightCam) #set camera height

def RNG(a, b): #random number generator
    return random.randint(a, b)

def main():
    leftEye = (300, 220) #left eye coordinates temperorary random
    rightEye = (340, 260) #right eye coordinates temperorary random
    score = 0
    BLUEBoxReset = 50 #box reset ticks. acts as timer for box reset
    redBoxReset = 50
    while True:
        BLUEtouching = False
        REDtouching = False

        success, img = cap.read() #read camera
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  #convert to rgb

        while not BLUEtouching or not REDtouching: #if touching is true, the box will be reset
            success, img = cap.read()
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxSize = 50

            cv2.rectangle(img, (0, 0), (widthCam, heightCam), (0, 0, 0), cv2.FILLED)  # black background

            results = pose.process(imgRGB)
            # print(results.pose_landmarks) #print landmarks info

            if results.pose_landmarks:
                mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)  # overall pose drawing
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    h, w, c = img.shape
                    # print(id, lm)
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if id == 15: #left wrist point
                        leftWristX, leftWristY = cx, cy
                        print("leftWrist", leftWristX, leftWristY)
                    if id == 16: #right wrist point
                        rightWristX, rightWristY = cx, cy
                        print("rightWrist", rightWristX, rightWristY)

                    # DRAW BOXES AND TOUCHING SENSE

                    if id == 20 or id == 19:  # arms
                        if BLUEBoxReset >= 50: #box timer reaches 50 ticks
                            BLUEcoor1 = (RNG(0, widthCam - boxSize), RNG(0, heightCam - boxSize)) #randomize box coordinates
                            BLUEcoor2 = (BLUEcoor1[0] + boxSize, BLUEcoor1[1] + boxSize) #creates other corner of box based on box size
                            BLUEmid = (int((BLUEcoor1[0] + BLUEcoor2[0]) / 2), int((BLUEcoor1[1] + BLUEcoor2[1]) / 2)) #center of box
                            BLUEBoxReset = 0 #reset box timer
                        BLUEBoxReset += 1 #increment BLUE box timer

                        if redBoxReset >= 50:
                            REDcoor1 = (RNG(0, widthCam - boxSize), RNG(0, heightCam - boxSize))
                            REDcoor2 = (REDcoor1[0] + boxSize, REDcoor1[1] + boxSize)
                            REDmid = (int((REDcoor1[0] + REDcoor2[0]) / 2), int((REDcoor1[1] + REDcoor2[1]) / 2))
                            redBoxReset = 0
                        redBoxReset += 1

                        print(id, cx, cy) #prints landmarks info for debugging

                        if id == 20:
                            BLUElength = math.hypot(cx - BLUEmid[0], cy - BLUEmid[1])

                            #creates line coordinates for stick
                            #starts with wrist and palm points, finds distance x and y and then multiplies by 3 and adds onto original point.
                            secondStickRightHandX, secondStickRightHandY = ((cx) + 3 * (int(cx - rightWristX)), cy + 3 * (int(cy - rightWristY)))

                            cv2.line(img, (cx, cy), (int(secondStickRightHandX), int(secondStickRightHandY)), (255, 0, 0), 10) #draws outline of stick
                            cv2.line(img, (cx, cy), (int(secondStickRightHandX), int(secondStickRightHandY)), (255, 255, 255), 3) #draws center glow line

                            if BLUElength < boxSize + 50: #tests if touching (around area)
                                score += 1 #increment score
                                BLUEtouching = True
                                BLUEBoxReset = 300
                        elif id == 19: #same as above but for RED box and left hand
                            secondStickLeftHandX, secondStickLeftHandY = ((cx) + 3 * (int(cx - leftWristX)), cy + 3 * (int(cy - leftWristY)))
                            print(secondStickLeftHandX, secondStickLeftHandY)
                            cv2.line(img, (cx, cy), (int(secondStickLeftHandX), int(secondStickLeftHandY)), (0, 0, 255),10)
                            cv2.line(img, (cx, cy), (int(secondStickLeftHandX), int(secondStickLeftHandY)),(255, 255, 255), 3)
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
            cv2.putText(img, str(int(score)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3) #score display. must be after flip or else text would be flipped
            cv2.imshow("BEATSABER", img)
            cv2.waitKey(1) #nessesary for cv2.imshow to work

if __name__ == '__main__': #calls main only when file is run
    main()
