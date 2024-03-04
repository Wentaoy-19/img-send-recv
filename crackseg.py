import cv2
import numpy as np
import matplotlib.pyplot as plt

def seg_crack(img_path):
    img = cv2.imread(img_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,30,0])
    upper_red = np.array([10,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    result = cv2.bitwise_and(img,img,mask=mask1)
    return result

def seg_png(img_path):
    img = seg_crack(img_path)
    ret = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    for i in range(0,img.shape[0]):
        for j in range(0,img.shape[1]):
            if(img[i,j,0]==0):
                img[i,j,2] = 0
            else:
                img[i,j,2] = 255
                img[i,j,1] = 0
                img[i,j,0] = 0
    result = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    B,G,R = cv2.split(img)
    _, Alpha= cv2.threshold(R, 200, 255, cv2.THRESH_BINARY)

    B2,G2,R2,A2 = cv2.split(result)
    A2 = Alpha
    result = cv2.merge([B2,G2,R2,A2]) #通道合并
    return result

def seg_and_save(img_path, save_path):
    ret = seg_png(img_path)
    filename = "SEG_"+img_path.split("/")[-1]
    cv2.imwrite(f"{save_path}/{filename}",ret)