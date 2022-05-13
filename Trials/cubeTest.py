import cv2
import mediapipe as mp
import time
import math

widthCam,heightCam = 640,480

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, widthCam)
    cap.set(4,heightCam)
    xOffset = 0
    yOffset = 0
    lengthCube = 40
    Xforward = True
    while cap.isOpened():
        success, img = cap.read()
        yOffset = 10
        p1X, p1Y = 10, 30
        p2X, p2Y = p1X, p1Y + lengthCube
        p3X, p3Y = p1X + lengthCube, p1Y + lengthCube
        p4X, p4Y = p1X + lengthCube, p1Y
        R2p1X, R2p1Y = p1X + xOffset, p1Y + yOffset
        R2p2X, R2p2Y = p2X + xOffset, p2Y + yOffset
        R2p3X, R2p3Y = p3X + xOffset, p3Y + yOffset
        R2p4X, R2p4Y = p4X + xOffset, p4Y + yOffset
        if xOffset < -lengthCube/2:
            Xforward = True
        if xOffset > lengthCube/2:
            Xforward = False
        if Xforward:
            xOffset += 1
        else:
            xOffset -= 1


        #primary square
        cv2.line(img, (p1X, p1Y), (p2X, p2Y), (0, 0, 255), 2)
        cv2.line(img, (p2X, p2Y), (p3X, p3Y), (0, 0, 255), 2)
        cv2.line(img, (p3X, p3Y), (p4X, p4Y), (0, 0, 255), 2)
        cv2.line(img, (p4X, p4Y), (p1X, p1Y), (0, 0, 255), 2)

        #second square
        cv2.line(img, (R2p1X, R2p1Y), (R2p2X, R2p2Y), (0, 0, 255), 2)
        cv2.line(img, (R2p2X, R2p2Y), (R2p3X, R2p3Y), (0, 0, 255), 2)
        cv2.line(img, (R2p3X, R2p3Y), (R2p4X, R2p4Y), (0, 0, 255), 2)
        cv2.line(img, (R2p4X, R2p4Y), (R2p1X, R2p1Y), (0, 0, 255), 2)

        # connect the two squares
        cv2.line(img, (p1X, p1Y), (R2p1X, R2p1Y), (0, 0, 255), 2)
        cv2.line(img, (p2X, p2Y), (R2p2X, R2p2Y), (0, 0, 255), 2)
        cv2.line(img, (p3X, p3Y), (R2p3X, R2p3Y), (0, 0, 255), 2)
        cv2.line(img, (p4X, p4Y), (R2p4X, R2p4Y), (0, 0, 255), 2)

        cv2.imshow('img', img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()