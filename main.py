import cv2
import torch
from tracker import *
import yolov5
import numpy as np
import ultralytics


model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

cap=cv2.VideoCapture('dog.mp4')


def POINTS(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :
        colorsBGR = [x, y]
        print(colorsBGR)






tracker = Tracker()

# area_1 =[(377,315),(429,373),(535,339),(500,296)]
area_1 =[(0,0),(0,0),(0,0),(0,0)]
area = set()

def leftclick(event):
    print("clicked")

while True:
    ret,frame=cap.read()
    frame=cv2.resize(frame,(1020,500))
    cv2.polylines(frame,[np.array(area_1,np.int32)],True,(0,255,0),3)
    results = model(frame)
    # frame = np.squeeze(results.render())
    list = []
    for index,row in results.pandas().xyxy[0].iterrows():
        x1=int(row['xmin'])
        y1=int(row['ymin'])
        x2=int(row['xmax'])
        y2=int(row['ymax'])
        b=str(row['name'])
        if 'dog' in b:
            list.append([x1,y1,x2,y2])


    box_ids = tracker.update(list)
    for box_id in box_ids:
        x,y,w,h,id=box_id
        cv2.rectangle(frame,(x,y),(w,h),(255,0,255),2)
        cv2.putText(frame, str(id), (x, y), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 2)
        result =cv2.pointPolygonTest(np.array(area_1,np.int32), (int(w), int(h)),False)
        if result > 0:
            area.add(id)
    print(len(area))




    cv2.imshow('FRAME',frame)

    if cv2.waitKey(1)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()


