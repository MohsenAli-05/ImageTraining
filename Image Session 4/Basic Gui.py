import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import numpy as np

class MainWindow(QWidget): #This class inherits from QWidget, which is the base class for all UI objects in PyQt. 
    #This class will contain the window where the webcam feed and its masked version will be displayed.
    def __init__(self):
        super(MainWindow, self).__init__() #calls the initilaizer of the base class QWidget to initialize the window

        self.VBL = QVBoxLayout()  #Layout manager that arranges child widgets in a vertically
        self.HBL = QHBoxLayout()  # Horizontal layout for side-by-side video display

        # here we're creating a label to display the original video feed
        self.FeedLabel = QLabel() #QLabel is a widget that can display text or images
        self.HBL.addWidget(self.FeedLabel) #add the widget to the horizontal layout

        #and here the masked video
        self.MaskLabel = QLabel()
        self.HBL.addWidget(self.MaskLabel)

        #note: A label in the context of graphical user interfaces (GUIs) refers to a widget or element that
        #displays text, an image, or both,without allowing direct interaction from the user.
        #It's commonly used to show information or data to the user in a visual format.

        # Add the horizontal layout with both videos to the main vertical layout
        self.VBL.addLayout(self.HBL)

        # Create pause/play button
        self.PausePlayBTN = QPushButton("Pause") #QPushButton is a widget that allows the user to interact with the application.
        self.PausePlayBTN.clicked.connect(self.TogglePausePlay) #connect the button to the function TogglePausePlay
        self.VBL.addWidget(self.PausePlayBTN) 

        # Create sliders for HSV bounds
        self.HueLowerSlider = self.create_slider(0, 179, 5, "Hue Lower") #create_slider is a self-made function that creates a slider with a given range and initial value
        self.HueUpperSlider = self.create_slider(0, 179, 15, "Hue Upper")
        self.SatLowerSlider = self.create_slider(0, 255, 150, "Saturation Lower")
        self.SatUpperSlider = self.create_slider(0, 255, 255, "Saturation Upper")
        self.ValLowerSlider = self.create_slider(0, 255, 150, "Value Lower")
        self.ValUpperSlider = self.create_slider(0, 255, 255, "Value Upper")

        # Worker to handle webcam feed
        self.Worker1 = Worker1() 
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.setLayout(self.VBL)

        self.is_paused = False  # Initialize the pause state

    def create_slider(self, min_val, max_val, init_val, label_text):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(init_val)
        slider.setTickInterval(1)

        # Create label for the slider
        label = QLabel(label_text)
        h_layout = QHBoxLayout() #explained in explanations.txt
        h_layout.addWidget(label)
        h_layout.addWidget(slider)
        self.VBL.addLayout(h_layout)

        return slider

    def TogglePausePlay(self):
        """Toggle between pause and play states."""
        if self.is_paused:
            self.PausePlayBTN.setText("Pause") #change the button text
            self.Worker1.start()  # Restart video feed
        else:
            self.PausePlayBTN.setText("Play")
            self.Worker1.stop()  # Stop video feed temporarily
        self.is_paused = not self.is_paused #toggle the pause state

    def ImageUpdateSlot(self, frame):
        """Handle the incoming frame and apply mask based on HSV sliders."""
        # Get HSV bounds from the sliders
        hue_lower = self.HueLowerSlider.value() #get calue men el slider
        hue_upper = self.HueUpperSlider.value()
        sat_lower = self.SatLowerSlider.value()
        sat_upper = self.SatUpperSlider.value()
        val_lower = self.ValLowerSlider.value()
        val_upper = self.ValUpperSlider.value()

        # Create mask based on HSV ranges
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_bound = np.array([hue_lower, sat_lower, val_lower])
        upper_bound = np.array([hue_upper, sat_upper, val_upper])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

        # Convert to RGB for displaying in QLabel
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        masked_frame_rgb = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2RGB)

        # Convert OpenCV images (RGB) to QImage for display
        original_qt_image = QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)
        #fel 7etta di, QImage converts the NumPy array into a QImage object, which can be displayed in a PyQt widget
        masked_qt_image = QImage(masked_frame_rgb.data, masked_frame_rgb.shape[1], masked_frame_rgb.shape[0], QImage.Format_RGB888)
        #parameters: raw pixel data, width, height, and format of the image

        # Display images in QLabel widgets
        self.FeedLabel.setPixmap(QPixmap.fromImage(original_qt_image).scaled(640, 480, Qt.KeepAspectRatio)) #explained in explanations.txt
        self.MaskLabel.setPixmap(QPixmap.fromImage(masked_qt_image).scaled(640, 480, Qt.KeepAspectRatio))

class Worker1(QThread): #A subclass of QThread that handles background tasks such as video capture without freezing the UI.
    ImageUpdate = pyqtSignal(np.ndarray) #A custom signal used to send the captured video frames (in np.ndarray format)
                                         #from the worker thread to the main UI thread.
    def run(self): #run functions executes lama benestakhdem start() 3ala el thread
        self.ThreadActive = True #just a flag used to know if the thread is running
        Capture = cv2.VideoCapture(0) 
        while self.ThreadActive:
            ret, frame = Capture.read() #Capture el video 3ady zay ma bena3mel fel cv2 normally
            if ret:
                self.ImageUpdate.emit(frame) #send the frame to the main thread using the ImageUpdate signal

    def stop(self): #stops the worker thread
        self.ThreadActive = False
        self.quit()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())
