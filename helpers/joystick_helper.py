import math
from scipy.stats import linregress
from ctypes import windll, Structure, c_long, byref

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

class JoyStick:
    def __init__(self):
        self.RADIUS = 2
        
    def screen_center(self):
        user32 = windll.user32
        win_width, win_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        x = win_width * 0.5
        y = win_height * 0.5
        return x, y


    def mouse_position(self):
        pt = POINT()
        windll.user32.GetCursorPos(byref(pt))
        return pt.x, pt.y
    
    # Get the distance between mouse and center
    def mouse_info(self):
        screen_x, screen_y = self.screen_center()
        mouse_x, mouse_y = self.mouse_position()
        
        screen = [screen_x, screen_y]
        mouse = [float(mouse_x), float(mouse_y)]
        distance_from_center = math.sqrt(((int(screen_x)-int(mouse_x))**2)+((int(screen_y)-int(mouse_y))**2))
        slope, intercept, r_value, p_value, std_err = linregress(screen, mouse)
            
        return distance_from_center, mouse_x, mouse_y, slope, intercept
            
