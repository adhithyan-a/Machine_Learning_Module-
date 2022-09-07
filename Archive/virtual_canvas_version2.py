# Version 2
# optimised 

from cmath import sqrt
import cv2
import numpy as np
import hand_tracking_module_new as htm
import time
import os


folder_path = "Overlays"
myList = os.listdir(folder_path)
print(myList)

overlayList = []
for impath in myList:
    image = cv2.imread(f'{folder_path}/{impath}')
    overlayList.append(image)
print(len(overlayList))

header_top = overlayList[0][0:110,0:1280] 
header_side = overlayList[0][0:720,0:150]

drawColor = [255,255,255]
xp,yp = 0,0
imgCanvas = np.zeros((720,1280,3),np.uint8)

eraserthickness  = 10
pencilthickness = 10
tool = 0

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = htm.handDetector(detectionCon=0.85)



while True:

# 1. importing image
    success,img = cap.read()
    img = cv2.flip(img,1)



# 2. finding hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList)!=0:
        # print(lmList)

        # tip of index and middle fingers
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]
        # tip of pinky finger
        x3,y3 = lmList[20][1:]



# 3.find which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)


# 4. selection mode - two fingers up
        if fingers[1] & fingers[2] == True:
            xp,yp = 0,0

            x= (x1+x2)//2
            y = (y1+y2)//2
            print("Selection mode")

            if x< 160 :
                if 115 < y < 230:
                    # header_top = overlayList[0][0:110,0:1280] 
                    header_side = overlayList[1][0:720,0:150]
                    tool = 0

                elif 230 < y < 345:
                    # header_top = overlayList[0][0:110,0:1280] 
                    header_side = overlayList[2][0:720,0:150]
                    tool = 1
                    

                elif 345 < y < 460:
                    # header_top = overlayList[0][0:110,0:1280] 
                    header_side = overlayList[3][0:720,0:150]
                    tool = 2

                elif 460 < y < 575:
                    # header_top = overlayList[0][0:110,0:1280] 
                    header_side = overlayList[4][0:720,0:150]
                    pencilthickness = 30

                elif 575 < y < 690:
                    # header_top = overlayList[0][0:110,0:1280] 
                    header_side = overlayList[5][0:720,0:150]
                    pencilthickness  = 10

            if y < 110 :
                if 200 < x < 380: #+180
                    header_top = overlayList[6][0:110,0:1280] 
                    # header_side = overlayList[6][0:720,0:150]
                    drawColor = [0,0,255]

                elif 380 < x < 560:
                    header_top = overlayList[7][0:110,0:1280] 
                    # header_side = overlayList[7][0:720,0:150]
                    drawColor = [103, 232, 110]

                elif 560 < x < 740:
                    header_top = overlayList[8][0:110,0:1280] 
                    # header_side = overlayList[8][0:720,0:150]
                    drawColor = [227, 244, 109]

                elif 740 < x < 920:
                    header_top = overlayList[9][0:110,0:1280] 
                    # header_side = overlayList[9][0:720,0:150]
                    drawColor = [24, 253, 255]

                elif 920 < x < 1100:
                    header_top = overlayList[10][0:110,0:1280] 
                    # header_side = overlayList[10][0:720,0:150]
                    drawColor = [255,255,255]   

                elif 1100 < x < 1280:
                    header_top = overlayList[11][0:110,0:1280] 
                    # header_side = overlayList[11][0:720,0:150]
                    drawColor = [0, 0, 0]     

            cv2.circle(img,(x,y),20,drawColor,thickness=5)


# 5. drawing mode - one finger up
        if fingers[1] & fingers[2] == False:
            cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
            print("Drawing mode")

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor==[0,0,0]:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserthickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserthickness)
                print('hi')

            if drawColor != (0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,pencilthickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,pencilthickness)

            xp, yp = x1, y1  


  # Palm erase     
        if fingers == [1,1,1,1,1]:
            rad = abs((x2-x1)*2)
            cv2.circle(img,(x1,y1),rad,(0,0,0),cv2.FILLED)
            print("palm erase")

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            cv2.line(img,(xp,yp),(x1,y1),thickness = rad*2,color = (0,0,0))
            cv2.line(imgCanvas,(xp,yp),(x1,y1),thickness = rad*2,color = (0,0,0))
            xp, yp = x1, y1  



    imggray= cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imginv=cv2.threshold(imggray,50,255,cv2.THRESH_BINARY_INV)
    imginv=cv2.cvtColor(imginv,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imginv)
    img=cv2.bitwise_or(img,imgCanvas)


# setting the header image
    img[0:110,0:1280] = header_top
    img[0:720,0:150] = header_side

    # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)

    cv2.imshow('Image',img)
    # cv2.imshow('Canvas',imgCanvas)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break