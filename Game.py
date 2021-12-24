import random
import time

import cv2
import numpy as np
import cvzone
from cvzone.HandTrackingModule import HandDetector

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Find function
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coeff = np.polyfit(x, y, 2)

# Game variables
cx, cy = 250, 250
color = (255, 0, 255)
counter = 0
score = 0
startTime = time.time()
totalTime = 20
# Loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    if time.time() - startTime < totalTime:
        hands = detector.findHands(img, draw=False)  # Find hands

        if hands:
            lmlist = hands[0]['lmList']
            x, y, w, h = hands[0]['bbox']
            # print(lmlist)
            x1, y1 = lmlist[5]
            x2, y2 = lmlist[17]

            distance = int(np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))
            A, B, C = coeff
            distanceCM = A * (distance ** 2) + B * distance + C

            if distanceCM < 50:
                if x < cx < x + w and y < cy < y + h:
                    counter = 1

            # print(distance, distanceCM)
            # print distance on screen
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)
            cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x + 5, y - 10))

        if counter:
            counter += 1
            color = (0, 255, 0)
            if counter == 3:
                cx = random.randint(100, 1100)
                cy = random.randint(100, 600)
                color = (255, 0, 255)
                score += 1
                counter = 0

        # Create a button
        cv2.circle(img, (cx, cy), 30, color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 20, (255, 255, 255), 2)
        cv2.circle(img, (cx, cy), 30, (50, 50, 50), 2)

        # Game HUD
        cvzone.putTextRect(img, f'Time: {int(totalTime - (time.time()-startTime))}', (1000, 75), scale=3, offset=20)
        cvzone.putTextRect(img, f'Score: {str(score).zfill(2)}', (60, 75), scale=3, offset=20)

    else:
        cvzone.putTextRect(img, f'Time is up!', (400, 400), scale=5, thickness=7, offset=30)
        cvzone.putTextRect(img, f'Your Score {str(score)}', (450, 500), scale=3, offset=20)
        cvzone.putTextRect(img, f'Press r to restart', (430, 570), scale=3, offset=20)

    cv2.imshow("Webcam", img)
    key = cv2.waitKey(1)

    if key == ord('r'):
        startTime = time.time()
        score = 0
