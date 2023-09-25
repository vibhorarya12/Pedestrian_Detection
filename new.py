import cv2
import tkinter as tk
from PIL import ImageTk, Image
import torch
from tracker import *
from time import strftime
from tkinter import filedialog
import os
import tkinter.messagebox
import yolov5
import numpy as np
import ultralytics

cv2.namedWindow('MYWINDOW')
def msg():
    tkinter.messagebox.showinfo("Closing window",  "Exit Now?")
    print("executed")
# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Open the video capture
cap = cv2.VideoCapture('cctv.mp4')


# Create a tracker instance
#tracker will assign id's to pedestrians
tracker = Tracker()
def browseFiles():
    file = filedialog.askopenfile(mode='r', filetypes=[('video files', '*.mp4'),('video files', '*.jpg')])
    filepath = os.path.abspath(file.name)
    global cap
    cap = cv2.VideoCapture(filepath)

# Callback function for mouse events
def POINTS(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colorsBGR = [x, y]
        print(colorsBGR)

# Function to process each frame and update the GUI
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
            cv2.rectangle(frame, (x, y), (w, h), (0,255,0), 2)
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

# Create the Tkinter window
def web():
    global cap
    cap = cv2.VideoCapture(0)
    process_frame()




window = tk.Tk()
window.geometry("700x350")
window.configure(background="#0096DC")
window.title("pedestrian detection")
def time():
    string = strftime('%H:%M:%S %p')
    lbl.config(text=string)
    lbl.after(1000, time)

# Create a label to display the video feed
label = tk.Label(window)
label.pack()
#label for clock
lbl = tk.Label(window, font=('calibri', 30, 'bold'),background='#0096DC',foreground='yellow')
lbl.pack()
lbl.place(x=200,y=600)

time()

# Create a button to start processing frames
start_button = tk.Button(window,height= 5, width=10, text="Start", command=lambda:[process_frame(),])
start_button.pack()
start_button.place(x=1500,y=20)
stop_button = tk.Button(window,height= 5, width=10, text="close", command=lambda:[msg()])
stop_button.pack()
stop_button.place(x=1500,y=120)
ped = tk.Label(window, text="pedestrian detection",font=('calibri', 30, 'bold'),background='#0096DC',foreground='red')
ped.place(x=700,y=600)
wb = tk.Button(window,height= 5, width=10, text="web", command=web)
wb.pack()
wb.place(x=1500,y=200)
files = tk.Button(window,height= 5, width=10, text="upload", command=browseFiles)
files.pack()
files.place(x=1500,y=300)


frame = tk.Frame(window, highlightcolor="black", width=5, height=550, background="red")

frame.pack()
frame.place(x=400,y=5)
frame2 = tk.Frame(window, highlightcolor="black", width=5, height=550, background="red")
frame2.place(x=1500,y=5)
# frame3 = tk.Frame(window, highlightcolor="black", width=1100, height=5, background="black")
# frame3.place(x=400,y=5)
frame4 = tk.Frame(window, highlightcolor="black", width=1100, height=5, background="red")
frame4.place(x=400,y=550)
# Set up the mouse callback
cv2.namedWindow('FRAME')
cv2.setMouseCallback('FRAME', POINTS)
# Start the Tkinter main loop
window.mainloop()


# Release the video capture and destroy windows

