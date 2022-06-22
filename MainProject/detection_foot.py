import torch
import cv2
import os
import cvzone
def detect_by_video(camera,pathModel):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=pathModel)
    cap = cv2.VideoCapture(camera)
    while True:
        _, frame = cap.read()
        results = model(frame)
        key = cv2.waitKey(1)
        if key == ord('c'):
            cv2.destroyAllWindows()
            crops = results.crop(save=True)
            crops = crops[0]['im']
            # crops = cv2.resize(crops, (800, 800))
            crops = cv2.cvtColor(crops, cv2.COLOR_BGR2RGB)
            cv2.imwrite('output/crops.jpg', crops)
            # cv2.imshow('crop', crops)
            # cv2.waitKey(0)
            break
        results.render()
        cv2.imshow('preview-frame',frame)

def detect_by_img(pathImg,pathModel):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=pathModel)
    # frame = 'D:/GitHub/projectsonteen/yolov5-master/test/foot (37).jpg'
    frame = pathImg
    results = model(frame)
    results.render()
    testlocation=[]
    testlocation=results.pandas().xyxy[0]
    print(results.pandas().xyxy[0])
    print(testlocation)
    print(testlocation.xmax[0])
    x1,y1 = testlocation.xmin[0],testlocation.ymin[0]
    x2,y2 = testlocation.xmax[0],testlocation.ymax[0]
    (x, y) = (x2 + x1) / 2, (y2 + y1) / 2
    print(x,y)
    # if results.names[0] == 'flat foot' :
    #     print('The best brand shoes for you is Adidas.')
    # elif results.names[0] == 'normal foot' :
    #     print('The best brand shoes for you is Adidas and Nike')

    #
    image_rgb = cv2.cvtColor(results.imgs[0], cv2.COLOR_BGR2RGB)
    image_rgb = cv2.circle(image_rgb, (int(x),int(y)), radius=0, color=(0, 0, 255), thickness=10)
    cv2.imshow('img', image_rgb)
    cv2.waitKey(0)
    crops = results.crop(save=True)
    crops = crops[0]['im']
    # crops = cv2.resize(crops, (800, 800))
    crops = cv2.cvtColor(crops, cv2.COLOR_BGR2RGB)
    cv2.imwrite('output/crops.jpg', crops)

def readAllfile():
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='D:/GitHub/projectsonteen/my models/best_typeFoot.pt')
    path = 'D:/GitHub/projectsonteen/yolov5-master/test/'
    dir = os.listdir(path)
    # print(path)
    # print(len(dir))
    # print(dir)

    for i in dir:
        print(path + i)
        img = cv2.imread(path + i)
        print(img)
        results = model(img)
        results.render()
        print(results.pandas().xyxy[0])
        img =results.imgs[0]

        cv2.imwrite("D:/GitHub/projectsonteen/yolov5-master/result test/" + i, img)


# take_a_photo(1)
# detect_from_img()
# readAllfile()

