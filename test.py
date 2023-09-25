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

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Open the video capture
cap = cv2.VideoCapture('cctv.mp4')
def webcam():
    global cap
    cap = cv2.VideoCapture(0)
# Create a tracker instance
#tracker will assign id's to pedestrians
tracker = Tracker()
area_1 =[(377,315),(429,373),(535,339),(500,296)]

area = set()


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
        print(len(area))
        # Convert the OpenCV frame to a PIL image
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image)
        # Update the image in the label
        label.config(image=imgtk)
        label.image = imgtk

    # Schedule the next frame processing
    window.after(1, process_frame)

#function to count pedestrians
def check():
    string = str(len(area))
    count = tk.Label(window, font=('calibri', 30, 'bold'), background='#0096DC', foreground='white')
    count.pack()
    count.place(x=100, y=600)
    count.config(text=string)
    Timer(1, check).start()
# Create the Tkinter window
window = tk.Tk()
window.geometry("1080x720")
window.configure(background="#0096DC")
window.title("pedestrian detection")

def time():
    st = strftime('%H:%M:%S %p')
    lbl.config(text=st)
    lbl.after(1000, time)


def leftclick(event):
    print("clicked")
# Create a label to display the video feed
label = tk.Label(window)
label.pack()
#label for clock
lbl = tk.Label(window, font=('calibri', 30, 'bold'),background='#0096DC',foreground='yellow')
lbl.pack()
lbl.place(x=200,y=600)
time()
#buttons for gui
start_button = tk.Button(window,height= 5, width=10, text="Start", command=process_frame)
start_button.pack()
start_button.place(x=1500,y=20)
stop_button = tk.Button(window,height= 5, width=10, text="close", command=window.destroy)
stop_button.pack()
stop_button.place(x=1500,y=120)
ped = tk.Label(window, text="pedestrian detection",font=('calibri', 30, 'bold'),background='#0096DC',foreground='red')
ped.place(x=700,y=600)
wb = tk.Button(window,height= 5, width=10, text="web", command=lambda:[webcam(),process_frame()])
wb.pack()
wb.place(x=1500,y=200)
cross = tk.Button(window,height= 5, width=10, text="COUNT", command=check)
cross.pack()
cross.place(x=1500,y=280)
frame = tk.Frame(window, highlightcolor="black", width=5, height=550, background="red")
frame.pack()
frame.place(x=400,y=5)
frame2 = tk.Frame(window, highlightcolor="black", width=5, height=550, background="red")
frame2.place(x=1500,y=5)
frame4 = tk.Frame(window, highlightcolor="black", width=1100, height=5, background="red")
frame4.place(x=400,y=550)
window.bind("<Button-1>",leftclick)

# Start the Tkinter main loop
window.mainloop()
cap.release()
cv2.destroyAllWindows()
