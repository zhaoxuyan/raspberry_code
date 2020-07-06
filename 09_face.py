# -*- coding: utf-8 -*
import cv2
from matplotlib import pyplot as plt
import copy
import os
import numpy as np

classifier_base_path = "/home/pi/.local/lib/python3.7/site-packages/cv2/data"
# 获取人脸识别分类器
face_cascade = cv2.CascadeClassifier(os.path.join(classifier_base_path, 'haarcascade_frontalface_default.xml'))

# 检测图片中的人脸
def detect_face_img():
    # 读取图片
    img_path = "./11.jpg"
    origin = cv2.imread(img_path)
    img = copy.deepcopy(origin)

    # 灰度转换
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.15, minNeighbors = 5, minSize = (5,5))
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    
    # 保存画框后的图片
    cv2.imwrite('face.jpg',img)
    # 显示两张图片
    imgs = np.hstack([origin,img])
    cv2.imshow("face_detection", imgs)
    cv2.waitKey()
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        return 0

def detect_face_camera():
    # 摄像头
    cap = cv2.VideoCapture(0) 
    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(20,20)
        )
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        if ret:
            cv2.imshow('video',frame)
            k = cv2.waitKey(30) & 0xff
            if k == 27: # press 'ESC' to quit
                break
        else:
            print("error")
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    detect_face_img()
    detect_face_camera()