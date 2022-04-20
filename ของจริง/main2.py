import cv2
import imutils
import numpy
import numpy as np
import matplotlib.pyplot as plt
import math

from scipy.spatial import distance as dist
def take_a_photo():
    # cap = cv2.VideoCapture(1)
    cap = cv2.VideoCapture('rtsp://192.168.1.101:8080/h264_pcm.sdp')
    while True:
        _, frame = cap.read()

        frame = cv2.resize(frame, (800, 800))

        # w = frame.shape[0]
        # h = frame.shape[1]
        start_point =(100,150)
        end_point =(700,650)

        frame = cv2.rectangle(frame, start_point, end_point, (0,0,255), 2)
        cv2.imshow('preview-frame',frame)
        key = cv2.waitKey(1)

        if key == ord('c'):
            # _, frame = cap.read()
            # frame = cv2.resize(frame, (800, 800))
            cropped_image = frame[150:650, 100:700]
            cv2.imwrite('capture.jpg',cropped_image)

            cv2.destroyAllWindows()
            break

def findA4():
    img = cv2.resize(cv2.imread('capture.jpg'), (800, 800))
    cv2.imshow('img', img)
    cv2.waitKey(0)

    # lower = numpy.array([150,150,150])
    # upper = numpy.array([255,255,255])
    mask_a4 = cv2.inRange(img,numpy.array([150,150,150]),numpy.array([255,255,255]))
    cv2.imshow('mask_a4', mask_a4)
    cv2.waitKey(0)
    kernel = np.ones((10, 10), np.uint8)
    mask_a4 = cv2.dilate(mask_a4, kernel, iterations=1)
    mask_a4 = cv2.erode(mask_a4, kernel, iterations=1)

    cv2.imshow('mask_a4', mask_a4)
    cv2.waitKey(0)

    cnts = cv2.findContours(mask_a4, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        epsilon = 0.06 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        contourSS = cv2.drawContours(img, [approx], 0, (0, 255,0), 2)
        # print(approx)

    myPoints = np.array(approx, dtype=np.int32)
    # print('********************************')
    # print(myPoints)
    # print('********************************')


    cv2.imshow('img', img)
    # plt.imshow(img)
    # plt.show()
    cv2.waitKey(0)

    w =2480;
    h = 3508;
    point0=myPoints[0]
    point1 = myPoints[1]
    point4 = myPoints[4]
    # print('********************************')
    # print('P0 = ',point0)
    # print('P1 = ', point1)
    # print('P4 = ', point4)
    point0 = point0[0]
    point1 = point1[0]
    point4 = point4[0]
    # print('P0 = ', point0)
    # print('P1 = ', point1)
    # print('P4 = ', point4)
    XP0 = point0[0]
    XP1 = point1[0]
    XP4 = point4[0]

    YP1 = point1[1]
    YP4 = point4[1]
    # print('XP0 = ', XP0)
    # print('XP1 = ', XP1)
    # print('XP4 = ', XP4)
    # print('YP1 = ', YP1)
    # print('YP4 = ', YP4)

    if XP0>XP1 and YP1<YP4 :
        pts1 = np.float32([myPoints[1], myPoints[0], myPoints[2], myPoints[4]])
    else :
        pts1 = np.float32([myPoints[0], myPoints[4], myPoints[1], myPoints[3]])

    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (w, h))
    # cv2.imshow('img', result)
    # cv2.waitKey(0)
    cv2.imwrite('result_A4.jpg', result)

def findSizeFoot ():
    A4 = cv2.imread('result_A4.jpg')
    A4 = cv2.resize(A4, (2480, 3508))
    # cv2.imshow('result_A4.jpg', A4)
    # cv2.waitKey(0)
    mask_a4 = cv2.inRange(A4, numpy.array([150, 150, 150]), numpy.array([255, 255, 255]))
    # cv2.imshow('mask_a4', mask_a4)
    # cv2.waitKey(0)
    kernel = np.ones((100, 100), np.uint8)
    mask_a4 = cv2.dilate(mask_a4, kernel, iterations=1)
    mask_a4 = cv2.erode(mask_a4, kernel, iterations=1)
    thresh1 = cv2.threshold(mask_a4, 125, 255, cv2.THRESH_BINARY_INV)[1]
    # cv2.imshow('mask_a4', thresh1)
    # cv2.waitKey(0)

    cnts = cv2.findContours(thresh1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)


    for c in cnts:

        x, y, w1, h1 = cv2.boundingRect(c)
        # cv2.rectangle(A4, (x, y), (x + w1, y + h1), (0, 255, 0), 10)
    for c in cnts:
        epsilon = 0.001 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        contourSS = cv2.drawContours(A4.copy(), [approx], 0, (0, 255,0), 2)
        # print(approx)
    plt.imshow(contourSS)
    plt.show()
    myPoints = np.array(approx, dtype=np.int32)
    # cv2.imshow('A4', A4)
    # cv2.waitKey(0)
    # size A4 = 21.0x29.7 cm ,2480x3508, 620x877 pixel , 1 cm = 29.52 pixel , 1 pixel = 0.03387
    dB = dist.euclidean((x,y),(x+w1,y))
    print('x = ', x)
    print('y = ', y)
    print('w1 = ', w1)
    print('h1 = ', h1)
    print('db = ', dB)
    cv2.circle(A4, (w1, h1), 5, (0, 255, 64), 100)
    cv2.circle(A4, (x, y), 5, (0, 255, 64), 100)
    HF = h1*(21/2480)
    error=4.5/100
    HF = HF+(HF*error)
    # print('H1 = ', h1)
    # print('W1 = ', w1)
    print('HF = ', HF)
    plt.imshow(cv2.cvtColor(thresh1, cv2.COLOR_BGR2RGB))
    plt.show()
    # [y1: y2, x1: x2]
    h1 = (3508-h1)+int(h1*3/4)

    # print('h1 = ', h1)
    crop_img = thresh1[0:h1 , : ]
    # plt.imshow(crop_img )
    # plt.show()
    cnts = cv2.findContours(crop_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:

        x, y, w1, h1 = cv2.boundingRect(c)
        cv2.rectangle(A4, (x, y), (x + w1, y + h1), (0, 0, 255), 10)

    # print('x = ', x)
    # print('y = ', y)
    # print('w1 = ', w1)
    # print('h1 = ', h1)

    WF = w1 * (21 / 2480)
    error = 0 / 100
    WF = WF - (WF * error)
    print('WF = ',WF)
    plt.imshow(cv2.cvtColor(A4, cv2.COLOR_BGR2RGB))
    plt.show()
take_a_photo()
findA4()
findSizeFoot()
