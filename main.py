import cv2
import numpy as np
import datetime

#cam=cv2.VideoCapture('http://192.168.0.38:8080/video')
cam=cv2.VideoCapture(0)

ret,frame1=cam.read()
ret,frame2=cam.read()

while(1):
    basic=frame1
    ret,osnova=cam.read()

    #zaznavanje premikanja
    diff=cv2.absdiff(frame1,frame2)
    gray=cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(5,5),0)
    _,thresh=cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    dialated=cv2.dilate(thresh,None,iterations=3)
    contours, _ =cv2.findContours(dialated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #risanje kvadratov na sliko, kjer se premika
    for contour in contours:
        (x,y,w,h)=cv2.boundingRect(contour)
        if cv2.contourArea(contour)<700:
            continue
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),1) #narise kvadratke
        cv2.putText(osnova,"Status: {}".format('Movement'),(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,0,255),1) #napise status

    trenutno=datetime.datetime.now()
    cv2.putText(osnova,"Date/Time: {}".format(trenutno.strftime("%d-%m-%Y %H:%M:%S")),(10,350),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),1)


    #združevanje za prikaz dveh videov
    both = np.concatenate((osnova, frame1), axis=1)


    #prikaz slike
    original=cv2.imshow('Kamera',both)
    frame1=frame2
    ret,frame2=cam.read()


    a=cv2.waitKey(1)

    if a==27:
        break

cam.release()
cv2.destroyAllWindows()
