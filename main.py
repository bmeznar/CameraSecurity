import cv2
import numpy as np
import datetime
from flask import Flask, render_template, Response

cam=cv2.VideoCapture(0)

ret,frame1=cam.read()
ret,frame2=cam.read()

app=Flask(__name__)

while(1):
    #mirror slike
    mirrorf1=cv2.flip(frame1,1)
    mirrorf2=cv2.flip(frame2,1)
    mirror=cv2.flip(frame1,1)

    #zaznavanje premikanja
    diff=cv2.absdiff(mirrorf1,mirrorf2)
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
        cv2.rectangle(mirrorf1,(x,y),(x+w,y+h),(0,255,0),1) #narise kvadratke
        cv2.putText(mirror,"Status: {}".format('Movement'),(10,20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3) #napise status

    trenutno=datetime.datetime.now()
    cv2.putText(mirror,"Date/Time: {}".format(trenutno.strftime("%d-%m-%Y %H:%M:%S")),(10,460),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)


    #združevanje za prikaz dveh videov
    both = np.concatenate((mirror, mirrorf1), axis=1)


    #stream videa
    """"@app.route('/')
    def index():
        return render_template('index.php')

    def gen():
        frame=cv2.imencode('.jpg',mirror)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n'+frame+b'\r\n')


    @app.route('/video_feed')
    def video_feed():
        return Response (gen(), mimetype='multipart/x-mixed-replace; boundary=frame')"""


    #prikaz slike
    original=cv2.imshow('frame',both)
    frame1=frame2
    ret,frame2=cam.read()


    a=cv2.waitKey(1)

    if a==27:
        break


cam.release()
cv2.destroyAllWindows()
