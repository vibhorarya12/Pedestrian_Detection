# functions
import cv2
import tkinter as tk
from PIL import ImageTk, Image
import torch
from tracker import *
from time import strftime
import yolov5
import numpy as np
import ultralytics
from threading import Timer
from tkinter import filedialog
import os
# function to process frame

def process_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (1020, 500))
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
            cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)
            cv2.putText(frame, str(id), (x, y), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)

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
    count = tk.Label(window, font=('calibri', 30, 'bold'), background='#0096DC', foreground='white')
    count.pack()
    count.place(x=100, y=600)
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


