from tkinter import*
import cv2
from PIL import Image,ImageTk
def temp():
   return 0



win = Tk()
win.geometry("700x350")
label =Label(win)
label.grid(row=0, column=0)
str = 'cctv.mp4'
str = Button(win, text="web", command=temp)
cap= cv2.VideoCapture(str)
frame = Frame(win, borderwidth=6, bg="grey",relief=SUNKEN)
frame.grid(pady=(100,150))
frame.grid(padx=(650,650))

def show_frames():
   # Get the latest frame and convert into Image
   cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   img = Image.fromarray(cv2image)
   # Convert image to PhotoImage
   imgtk = ImageTk.PhotoImage(image = img)
   label.imgtk = imgtk
   label.configure(image=imgtk)
   # Repeat after an interval to capture continiously
   label.after(20, show_frames)

btn = Button(frame,text='show',bg='white',fg='black', command=show_frames)
btn.grid()
btn2 = Button(frame,text='close',bg='white',fg='black', command=win.destroy)
btn2.grid()






win.mainloop()