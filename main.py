import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

width, height = 1280, 720
folder_path = "Presentation"
gesture_threshold = 300
buttonpressed = False
buttoncounter = 0
buttondelay = 20
Annotations = [[]]
Annotationnum = -1
Annotationstart = False
# camera setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# get the list of images
pathImages = sorted(os.listdir(folder_path), key=len)
# print(pathImages)

imgNumber = 0
hs, ws = int(120 * 1), int(213 * 1)

# hand Detector
Detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    # Import Images
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folder_path, pathImages[imgNumber])
    imgcurrent = cv2.imread(pathFullImage)
    hands, img = Detector.findHands(img)
    cv2.line(img, (0, gesture_threshold), (width, gesture_threshold), (0, 255, 0), 10)
    if hands and buttonpressed is False:
        hand = hands[0]

        cx, cy = hand['center']
        lmlist = hand['lmList']
        fingers = Detector.fingersUp(hand)

        # constrained values for easier drawing

        xVal = int(np.interp(lmlist[8][0], [width // 2, w], [0, width]))
        yVal = int(np.interp(lmlist[8][1], [150, height - 150], [0, height]))
        indexFinger = xVal, yVal

        if cy <= gesture_threshold:

            # Gesture1= Left
            if fingers == [1, 0, 0, 0, 0]:

                buttonpressed = True
                if imgNumber > 0:
                    Annotations = [[]]
                    Annotationstart = False
                    Annotationnum = -1
                    imgNumber -= 1
            # Gesture2= Right
            if fingers == [0, 0, 0, 0, 1]:

                buttonpressed = True
                if imgNumber < len(pathImages) - 1:
                    Annotations = [[]]
                    Annotationnum = -1
                    Annotationstart = False

                    imgNumber += 1
        # Gesture3: Show Pointer
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgcurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        # Gesture4: Draw
        if fingers == [0, 1, 0, 0, 0]:
            if Annotationstart is False:
                Annotationstart = True
                Annotationnum += 1
                Annotations.append([])
            Annotations[Annotationnum].append(indexFinger)
            cv2.circle(imgcurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
        else:
            Annotationstart = False

        # Gesture5: Erase
        if fingers == [0, 1, 1, 1, 0]:
            if Annotations:
                Annotations.pop(-1)
                Annotationnum -= 1
                buttonpressed = True
    else:
        Annotationstart = False

    # ButtonPressed iterations
    if buttonpressed:
        buttoncounter += 1
        if buttoncounter > buttondelay:
            buttoncounter = 0
            buttonpressed = False
    for i, annotation in enumerate(Annotations):
        for j in range(len(annotation)):
            if j != 0:
                cv2.line(imgcurrent, annotation[j - 1], annotation[j], (0, 0, 200), 12)
    # for i in range(len(Annotations)):
    #     for j in range(len(Annotations[i])):
    #         if j != 0:
    #             cv2.line(imgcurrent, Annotations[i][j - 1], Annotations[i][j], (0, 0, 200), 12)

    # Adding webcam image on the sildws
    imagesmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgcurrent.shape
    imgcurrent[0:hs, w - ws:w] = imagesmall
    cv2.imshow("Image", img)
    cv2.imshow("Slides", imgcurrent)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
