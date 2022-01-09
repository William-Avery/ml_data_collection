import win32api
import time
import pandas as pd
import keyboard
import pickle

from datetime import datetime
from .capture_helper import CaptureHelper


class DataHelper:
    def __init__(self):
        self.DATABASE_FILENAME = 'serialized_data.pkl'
        
    def frame_to_json(self):
        raise NotImplementedError


    def countdown(self):
        t = 3
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1

    def init_datarecorder(self):
        # Open up pickle file database
        pkl_file = open(self.DATABASE_FILENAME, 'wb')
        
        # Initialize image recorder
        capture_helper = CaptureHelper()

        # Start Countdown
        self.countdown()
        print("Recording Started!")
        
        while True:
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
                'path': ''
            }, index=[0]) 

            try:  # used try so that if user pressed other than the given key error will not be shown         
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
                _, id = capture_helper.frame_grab()
                frame_data['path'] = f'/images/{id}.png'
                
                # Save results to pickle file
                pickle.dump(frame_data, pkl_file, pickle.HIGHEST_PROTOCOL)
            except:
                break
        pkl_file.close()
        
    def Test(self):
        raise NotImplementedError
            