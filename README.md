# Pedestrian Detection and Counting System

This project is a real-time pedestrian detection and counting system developed using Python. The system leverages deep learning models and computer vision techniques to detect pedestrians in video feeds, such as from a CCTV camera, and counts them as they cross a predefined area. The GUI is built using Tkinter, allowing for easy interaction and visualization.

![ezgif com-optimize](https://github.com/user-attachments/assets/c573234a-ed16-45a2-b5ff-812d666e4d24)

![final](https://github.com/user-attachments/assets/2d72f4a4-4204-417e-981e-d367f3d3ceb9)



## Key Features
- **Real-time Pedestrian Detection:** Utilizes the YOLOv5 deep learning model for accurate and fast detection of pedestrians in video frames.
- **Object Tracking:** Tracks the detected pedestrians across frames using a custom tracking algorithm.
- **Area-Based Counting:** Counts pedestrians as they cross a specified polygonal area on the screen.
- **GUI Interface:** Provides a user-friendly interface for starting/stopping detection, switching between webcam and video files, and visualizing the pedestrian count.

## Main Libraries Used
- **[OpenCV](https://opencv.org/):** Used for video capture, image processing, and displaying the results.
- **[Tkinter](https://wiki.python.org/moin/TkInter):** Provides the graphical user interface for the application.
- **[PyTorch](https://pytorch.org/):** Facilitates loading the YOLOv5 model for pedestrian detection.
- **[Pillow](https://python-pillow.org/):** Used for image conversion and handling within the Tkinter GUI.
- **[YOLOv5](https://github.com/ultralytics/yolov5):** A pre-trained deep learning model for real-time object detection.



## Usage
- **Start Detection:** Click on the "Start" button to begin pedestrian detection.
- **Switch to Webcam:** Click on the "Webcam" button to use your webcam as the video source.
- **Upload Video:** Click on the "Upload" button to choose a video file (.mp4) for detection.
- **Set Area and Count:** Click on the "Count" button to set the area for pedestrian counting.

## Contributing
Feel free to open issues or submit pull requests if you have any ideas for improving the project.


