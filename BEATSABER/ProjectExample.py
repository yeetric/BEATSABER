#thumb to middle is click
#thumb to index is space
#cursor following palm

import cv2
import mediapipe as mp
import time
import pyautogui
import math

widthCam,heightCam = 640,480

pyautogui.FAILSAFE = False
class handDetector():
    def __init__(self, mode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex,
                                        self.detectionCon, self.trackCon)

    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
        try:
            if self.results.multi_hand_landmarks:
                for handLms in self.results.multi_hand_landmarks:
                    if draw:
                        self.mp_drawing.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
            return img
        except:
            print("Don't go off screen")

    def findPosition(self, img, handNo=0,draw=True):
        lmList=[]
        if self.results.multi_hand_landmarks:
            myHands=self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHands.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id,cx,cy])
                if draw:
                    try:
                        if id == 9:
                            pyautogui.moveTo(4.5 * -cx + 2320, 4 * cy - 400)
                            cv2.circle(img, (cx, cy), 14, (255, 0, 255), cv2.FILLED)
                    except:
                        print("Don't go off screen")
        return lmList
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    cap.set(3, widthCam)
    cap.set(4,heightCam)
    detector=handDetector()
    while cap.isOpened():
        success, img = cap.read()
        img=detector.findHands(img,draw=False) #if you don't want hand o utline, change draw to False
        lmList = detector.findPosition(img, draw=True) #if you don't want the pink circle, change it to lmList = detector.findPosition(img,draw=False)
        if len(lmList)!=0:
            #TURN THE NEXT LINE OFF LATER
            # print(lmList[9]) #printing the poistion of number [9]
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            x3, y3 = lmList[12][1], lmList[12][2]


            #shows circle and lines on index and thumb
            cv2.circle(img,(x1, y1),10,(0, 255, 255),cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 3)
            cv2.line(img, (x1, y1), (x3, y3), (0, 255, 255), 3)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 10, (255,150,0), cv2.FILLED)


            #length between thumb and INDEX
            length1 = math.hypot(x2-x1,y2-y1)

            #length between thumb and MIDDLE
            length2 = math.hypot(x3 - x1, y3 - y1)

            #prints distance between thumb and other fingers
            thecoordinates=(f"{int(length1)} , {int(length2)}")


            if length1<16: #change later
                pyautogui.press('space')
                time.sleep(0.05)
            elif length2<30:
                pyautogui.click()


        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime


        #if you want the frames per second
        # cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)


        # If you want to show the image, leave the line underneath uncommented, otherwise, comment it out
        # flip mirror image opencv
        cv2.imshow('img', cv2.flip(img,1))



        cv2.waitKey(1)

if __name__ == "__main__":
    print("AirMouse No Touch Control has been activated")
    time.sleep(5)
    print("Click the X arrow at the top right to deactivate")
    main()