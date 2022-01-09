from mss import mss
import cv2, os
import numpy as np
import uuid

# Used for rapid mouse position capture
from ctypes import windll, Structure, c_long, byref

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

# Convert image in memory
# Grab screen

class CaptureHelper:
    def __init__(self, M_WIDTH=1920, M_HEIGHT=1080):
        self.frame = None
        self.WINDOW_NAME = ""
        self.RESIZE_DIMENSION = 768
        self.SAVE_PATH = os.path.join('images')
        self.WINDOW_HEIGHT = M_WIDTH # Monitor Width
        self.WINDOW_WIDTH = M_HEIGHT # Monitor Height
        self.CAPTURE_TOP_POS = None
        self.CAPTURE_BOTTOM_POS = None
        self.init_screensize()

    # Returns dimentions of the primary display
    def init_screensize(self):
        user32 = windll.user32
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    # Returns a single video frame using mss.
    def frame_grab(self):
        id = str(uuid.uuid4())
        
        # Use mss li
        with mss() as sct:
            # Define a region you want to capture
            region = {'top': 0, 'left': 0, 'width': self.WINDOW_WIDTH, 'height': self.WINDOW_HEIGHT}
            img = sct.grab(region)
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
            
            # Resize Frame
            resized_frame = cv2.resize(frame,(self.RESIZE_DIMENSION,self.RESIZE_DIMENSION))
            cv2.imwrite(os.path.join(self.SAVE_PATH, f'{id}.jpg'), resized_frame)
            return resized_frame, id
        
    # Returns mouse position in { x, y } object
    def mouse_pos_query(self):
        pt = POINT()
        windll.user32.GetCursorPos(byref(pt))
        return { "x": pt.x, "y": pt.y}
            
    # Save Images
    def save(self, image):
        cv2.imwrite(self.SAVE_PATH + uuid.uuid4(), image)

    
        
#ch = CaptureHelper()
#ch.RESIZE_DIMENSION
#frame, _ = ch.frame_grab()

#cv2.imshow('image',frame)
#cv2.waitKey(0)