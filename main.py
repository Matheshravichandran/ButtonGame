import  cv2
import  numpy as np
import cvzone
from cvzone.HandTrackingModule import HandDetector

#Webcam
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

#Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

#Find function
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coeff = np.polyfit(x, y, 2)

#Loop
while True:
    success, img = cap.read()
    hands = detector.findHands(img, draw=False) #Find hands

    if hands:
        lmlist = hands[0]['lmList']
        x, y, w, h = hands[0]['bbox']
        # print(lmlist)
        x1, y1 = lmlist[5]
        x2, y2 = lmlist[17]

        distance = int(np.sqrt((x1-x2)**2 + (y1-y2)**2))
        A, B, C = coeff
        distanceCM = A * (distance**2) + B * distance + C
        print(distance, distanceCM)
        #print distance on screen
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,255), 3)
        cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x+5, y-10))

    cv2.imshow("Webcam", img)
    cv2.waitKey(1)