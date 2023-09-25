# import the opencv library
import os.path
import cv2
import tkinter as tk
from tkinter import filedialog
import numpy as np
from tkinter.filedialog import askopenfile
from PIL import Image,ImageTk
# define a video capture object
def leftclick(event):
    print("clicked")


vid = cv2.VideoCapture("cctv.mp4")


def track_coordinates(window_name):
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"Coordinates: ({x}, {y})")

    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_callback)

    while True:
        # Capture frame from a video source or load an image
        # For simplicity, let's use a black image
        frame = np.zeros((480, 640, 3), np.uint8)

        # Display the frame in the window
        cv2.imshow(window_name, frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


def cam():
    while (True):

        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


def browseFiles():
    file = filedialog.askopenfile(mode='r', filetypes=[('video files', '*.mp4'),('video files', '*.jpg')])
    filepath = os.path.abspath(file.name)
    global vid
    vid = cv2.VideoCapture(filepath)



window = tk.Tk()
window.geometry("700x350")
window.configure(background="#0096DC")
button1 = tk.Button(window, height= 5, width=10, text="Start", command=lambda:[cam(),track_coordinates("FRAME")])
button2 = tk.Button(window, height= 5, width=10, text="upload", command=browseFiles)
button1.pack()
button2.pack()
window.bind("<Button-1>",leftclick)
window.mainloop()

