import cv2
import os
import tkinter as tk
from PIL import ImageTk, Image
import torch
from tracker import *
from time import strftime
import numpy as np
from threading import Timer
from tkinter import filedialog
from tkinter import messagebox

######################################################
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
cap = cv2.VideoCapture('cctv.mp4')
tracker = Tracker()
area_1 =[(0,0),(0,0),(0,0),(0,0)]
area = set()
#######################################################

def process_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (1020, 500))
        cv2.polylines(frame, [np.array(area_1, np.int32)], True, (0, 255, 0), 3)
        results = model(frame)
        list = []
        for index, row in results.pandas().xyxy[0].iterrows():
            x1 = int(row['xmin'])
            y1 = int(row['ymin'])
            x2 = int(row['xmax'])
            y2 = int(row['ymax'])
            b = str(row['name'])
            if 'person' in b:
                list.append([x1, y1, x2, y2])

        box_ids = tracker.update(list)
        for box_id in box_ids:
            x, y, w, h, id = box_id
            cv2.rectangle(frame, (x, y), (w, h), (0,255,0), 2)
            cv2.putText(frame, str(id), (x, y), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
            result = cv2.pointPolygonTest(np.array(area_1, np.int32), (int(w), int(h)), False)
            if result > 0:
                area.add(id)
        # print(len(area))
        # Convert the OpenCV frame to a PIL image
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image)
        # Update the image in the label
        label.config(image=imgtk)
        label.image = imgtk

    # Schedule the next frame processing
    window.after(1, process_frame)


# function to count pedestrians
def check():
    string = str(len(area))
    count = tk.Label(window, font=('calibri', 50, 'bold'), background='#0096DC', foreground='white')
    count.pack()
    count.place(x=200,y=400)
    count.config(text=string)
    Timer(1, check).start()


# function for timer
def time():
    st = strftime('%H:%M:%S %p')
    lbl.config(text=st)
    lbl.after(1000, time)


# function for webcam
def webcam():
    global cap
    cap = cv2.VideoCapture(0)


# function to upload file
def browseFiles():
    file = filedialog.askopenfile(mode='r', filetypes=[('video files', '*.mp4'), ('video files', '*.jpg')])
    filepath = os.path.abspath(file.name)
    global cap
    cap = cv2.VideoCapture(filepath)



def poly():
    new = [(377,315),(429,373),(535,339),(500,296)]
    global area_1
    area_1 = new

def leave():
    res = messagebox.askquestion('PROMPT', 'EXIT NOW?')
    if res == 'yes' :
        window.destroy()




#####################################################################################################################
window = tk.Tk()
window.geometry("1080x720")
window.configure(background="#0096DC")
window.title("pedestrian detection: VIBHOR ARYA ")
#labels
label = tk.Label(window)
label.pack()
ped = tk.Label(window, text="PEDESTRIAN DETECTION",font=('calibri', 30, 'bold'),background='#0096DC',foreground='red')
ped.place(x=700,y=600)
name = tk.Label(window, text="VIBHOR ARYA - MCA(67-C)",font=('calibri', 20, 'bold'),background='#0096DC',foreground='white')
name.place(x=700,y=680)
#label for clock
lbl = tk.Label(window, font=('calibri', 30, 'bold'),background='#0096DC',foreground='yellow')
lbl.pack()
lbl.place(x=200,y=600)
time()

#buttons#
start_button = tk.Button(window,height= 5, width=10, text="Start", command=process_frame)
start_button.place(x=1500,y=20)
stop_button = tk.Button(window,height= 5, width=10, text="close", command=leave)
stop_button.place(x=1500,y=120)
wb = tk.Button(window,height= 5, width=10, text="web", command=lambda:[webcam(),process_frame()])
wb.place(x=1500,y=200)
cross = tk.Button(window,height= 5, width=10, text="COUNT", command=lambda :[poly(),check()])
cross.place(x=1500,y=280)
files = tk.Button(window,height= 5, width=10, text="upload", command=browseFiles)
files.place(x=1500,y=380)
#window frame for displaying video feed
frame = tk.Frame(window, highlightcolor="black", width=5, height=550, background="red")
frame.place(x=400,y=5)
frame2 = tk.Frame(window, highlightcolor="black", width=5, height=550, background="red")
frame2.place(x=1500,y=5)
frame4 = tk.Frame(window, highlightcolor="black", width=1100, height=5, background="red")
frame4.place(x=400,y=550)

window.mainloop()


