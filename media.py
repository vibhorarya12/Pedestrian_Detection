import cv2


# capture frames from a video
cap = cv2.VideoCapture( r'C:\Users\vchan\OneDrive\Desktop\Untitled Folder\pedestrian and walk 360.mp4',0)

# Trained XML classifiers describes some features of some object we want to detect
pedestrian_cascade = cv2.CascadeClassifier("haarcascade_fullbody.xml")

# loop runs if capturing has been initialized.
def pedestrianDetection(frame):
    # reads frames from a video
    ret, frames = cap.read()
    # convert to gray scale of each frames
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
    # Detects pedestrians of different sizes in the input image
    pedestrians = pedestrian_cascade.detectMultiScale(frame, 1.1, 1)
    # To draw a rectangle in each pedestrians
    for (x,y,w,h) in pedestrians:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, 'Person', (x + 6, y - 6), font, 0.5, (0, 255, 0), 1)
        # Display frames in a window
    return frame
input = cv2.imread("image.jpg")
output = pedestrianDetection(input)
cv2.imshow(output)