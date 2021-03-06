import win32api
import time
import pandas as pd
import keyboard
import os
import winsound

from datetime import datetime
from .capture_helper import CaptureHelper
from .joystick_helper import JoyStick

class DataHelper:
    def __init__(self, title):
        self.title = title
        self.COUNTDOWN_TIME = 5
        self.PICKLE_PATH = f'./data/{title}.pkl'

    def countdown(self):
        t = self.COUNTDOWN_TIME
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1

    def start_recording(self):
        # 1. Check if pickle db exists. If not, create empty dataframe
        if not os.path.isfile(self.PICKLE_PATH):
            df = pd.DataFrame()
            pd.to_pickle(df, self.PICKLE_PATH)

        # 2. Create empty dataframe to append to
        data = pd.read_pickle(self.PICKLE_PATH)

        # 3. Initialize image recorder & joystick session
        capture_helper = CaptureHelper()
        movement_session = JoyStick()

        # 4. Start Countdown
        self.countdown()
        print("Recording Started!")
        print("Press 'Esc' key to Stop")
        winsound.PlaySound("*", winsound.MB_OK)
        
        # 5. Loop through recorder
        while True:
            
            # 6. Initialize blank values
            frame_data = pd.DataFrame({
                'w': 0,
                's': 0,
                'a': 0,
                'd': 0,
                'e': 0,
                'q': 0,
                'r': 0,
                'f': 0,
                'Space': 0,
                'Shift': 0,
                'lmb': 0,
                'rmb': 0,
                'time': datetime.now().timestamp(),       
                'dfc': 0, # Distance from center
                'mouse_x': 0,
                'mouse_y': 0,
                'slope': 0,
                'intercept': 0,
                'img': ''
            }, index=[0]) 
            
            try:       
                if keyboard.is_pressed('Esc'):
                    print("Recording Stopped!")
                    break
                
                # Movement
                if keyboard.is_pressed('w'):
                    frame_data['w'] = 1
                if keyboard.is_pressed('s'):
                    frame_data['s'] = 1
                if keyboard.is_pressed('a'):
                    frame_data['a'] = 1
                if keyboard.is_pressed('d'):
                    frame_data['d'] = 1
                    
                # Actions
                if keyboard.is_pressed('e'):
                    frame_data['e'] = 1
                if keyboard.is_pressed('Space'):
                    frame_data['Space'] = 1
                if keyboard.is_pressed('Shift'):
                    frame_data['Shift'] = 1
                    
                # Mouse
                state_left = win32api.GetAsyncKeyState(0x01)
                if state_left < 0:
                    frame_data['lmb'] = 1
                state_right = win32api.GetAsyncKeyState(0x02)
                if state_right < 0:
                    frame_data['rmb'] = 1
                
                # Spells
                if keyboard.is_pressed('q'):
                    frame_data['q'] = 1
                if keyboard.is_pressed('r'):
                    frame_data['r'] = 1      
                if keyboard.is_pressed('f'):
                    frame_data['f'] = 1
                
                
                # Grab image
                img, id = capture_helper.frame_grab()
                frame_data['img'] = img
                
                # Grab mouse
                mouse_data = movement_session.mouse_info()
                frame_data['dfc'] = mouse_data[0]
                frame_data['mouse_x'] = mouse_data[1]
                frame_data['mouse_y'] = mouse_data[2]
                frame_data['slope'] = mouse_data[3]
                frame_data['intercept'] = mouse_data[4]
                                         
                # Save results to pickle file
                data = data.append(frame_data, ignore_index = True)
            except:
                
                break
        # Save Information to pickle
        print("Cleaning Up & Packaging Data..")
        pd.to_pickle(data, self.PICKLE_PATH)
        winsound.PlaySound("*", winsound.MB_OK)
        print("Done")

    def unpack_images(self):
        raise NotImplementedError
    
    def pack_images(self):
        raise NotImplementedError