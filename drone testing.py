from djitellopy import Tello
import cv2, math, time
import numpy as np
fbrange=[6200,6800]
# pid=[0.4,0.4,0]
# pError=int(0)
w,h=360,240
tello = Tello()
tello.connect()
tello.streamon()
frame_read = tello.get_frame_read()
tello.takeoff()
# tello.send_rc_control(0,0,25,0)
# time.sleep(1.8)
def findFace(img):
    faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(imgGray,1.2,8)
    myFaceListc=[]
    myFaceListArea=[]
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cx=x+w//2
        cy=y+h//2
        area=w*h
        cv2.circle(img,(cx,cy),5,(0,255,0),cv2.FILLED)
        myFaceListc.append([cx,cy])
        myFaceListArea.append(area)
    if len(myFaceListArea)!=0:
        i=myFaceListArea.index(max(myFaceListArea))
        return img,[myFaceListc[i],myFaceListArea[i]]
    else:
        return img,[[0,0],0]
def tracMe(info):
    # pError=0
    fb=0
    area=info[1]
    x,y=info[0]
    error=x-w//2
    # speed=pid[0]*error+pid[1]*(error-pError)
    # speed=int(np.clip(speed,-100,100))
    if area>fbrange[0] and area<fbrange[1]:
        fb=0
    elif area>fbrange[1]:
        fb=-20
    elif area<fbrange[0]:
        fb=20 
    if x==0:
        speed=0
        error=0
    if y==0:
        speed=0
        error=0
    print(fb)
    tello.send_rc_control(0,fb,0,0)
    return error

while True:
    img = frame_read.frame
    # img=cv2.resize(img)
    img,info=findFace(img)
    # findFace(img)
    tracMe(info)
    print("Area ",info[1])
    cv2.imshow("drone", img)
    key = cv2.waitKey(1) & 0xff
    if key == 27: # ESC
        break
    elif key == ord('w'):
        tello.move_forward(30)
    elif key == ord('s'):
        tello.move_back(30)
    elif key == ord('a'):
        tello.move_left(30)
    elif key == ord('d'):
        tello.move_right(30)
    elif key == ord('e'):
        tello.rotate_clockwise(30)
    elif key == ord('q'):
        tello.rotate_counter_clockwise(30)
    elif key == ord('r'):
        tello.move_up(30)
    elif key == ord('f'):
        tello.move_down(30)

tello.land()

