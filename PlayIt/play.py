# KEYBARD
# https://www.onlinepianist.com/virtual-piano

import pandas as pd
from pynput.keyboard import Listener as KeyboardListener
from pynput.keyboard import Key, Controller
from pynput import keyboard
control = Controller()
#import pynput
import time
import numpy as np
import pygetwindow as gw
#import sys

class Play:

    def __init__(self,title):

        print("################   from_csv    ################")
        self.title = title
        self.stop = False  # Flag to stop the program

        #array which contains all the keys
        #self.keys[:][0] -> output value for online Keyboard
        #self.keys[:][1] -> 0 = white key, 1 = black key
        #self.keys[:][2] -> note
        self.keys = np.array([['1','0','c2'],['1','1','c#2'],
                              ['2','0','d2'],['2','1','d#2'],
                              ['3','0','e2'],
                              ['4','0','f2'],['4','1','f#2'],
                              ['5','0','g2'],['5','1','g#2'],
                              ['6','0','a2'],['6','1','a#2'],
                              ['7','0','b2'],
                              
                              ['8','0','c3'],['8','1','c#3'],
                              ['9','0','d3'],['9','1','d#3'],
                              ['0','0','e3'],
                              ['q','0','f3'],['q','1','f#3'],
                              ['w','0','g3'],['w','1','g#3'],
                              ['e','0','a3'],['e','1','a#3'],
                              ['r','0','b3'],
                              
                              ['t','0','c4'],['t','1','c#4'],
                              ['y','0','d4'],['y','1','d#4'],
                              ['u','0','e4'],
                              ['i','0','f4'],['i','1','f#4'],
                              ['o','0','g4'],['o','1','g#4'],
                              ['p','0','a4'],['p','1','a#4'],
                              ['a','0','b4'],
                              
                              ['s','0','c5'],['s','1','c#5'],
                              ['d','0','d5'],['d','1','d#5'],
                              ['f','0','e5'],
                              ['g','0','f5'],['g','1','f#5'],
                              ['h','0','g5'],['h','1','g#5'],
                              ['j','0','a5'],['j','1','a#5'],
                              ['k','0','b5'],
                              
                              ['l','0','c6'],['l','1','c#6'],
                              ['z','0','d6'],['z','1','d#6'],
                              ['x','0','e6'],
                              ['c','0','f6'],['c','1','f#6'],
                              ['v','0','g6'],['v','1','g#6'],
                              ['b','0','a6'],['b','1','a#6'],
                              ['n','0','b6'],
                              ['m','0','c7']])
        
    def convert_to_play(self):

        # Load the CSV file
        file_path = f".\CSV\{self.title}.csv"

        print('\n################', self.title, ' #################\n')

        # time per minimum beat
        self.t = float(pd.read_csv(file_path, skiprows=3, nrows=1, sep=";").iloc[0, 1])
        self.t_divB = self.t/1000000

        df = pd.read_csv(file_path, sep=';', skiprows=7)

        # transforming to numpy array
        self.sheet = df.to_numpy()

        print('minimum beat = ', self.t, 's')
        print('duration = ', (self.sheet.shape[0])*self.t, 's')

        #deleting first seven rows and two coumns 
        #self.sheet = np.delete(self.sheet, np.s_[0:7], axis=0)
        self.sheet = np.delete(self.sheet, [0,1], 1)
        print(self.sheet)
        # Reshape the array into 3D
        # self.sheet.shape[0] -> minimum beats
        # self.sheet.shape[1] -> different notes
        # self.sheet[:, :, 0] -> pitch (string)
        # self.sheet[:, :, 1] -> note lengths (bool)
        rows, cols = self.sheet.shape

        assert cols % 2 == 0, "The number of columns must be even!"  # Ensure even number of columns
        self.sheet = self.sheet.reshape(rows, cols // 2, 2)  # Reshape into (rows, half columns, 2)
        
        for i in range(self.sheet.shape[0]):  # Iterate over the first dimension
            for j in range(self.sheet.shape[1]):  # Second dimension
                #stripping whitespaces
                if isinstance(self.sheet[i, j, 0], str):  # Check if the pitch value is a string
                    self.sheet[i, j, 0] = self.sheet[i, j, 0].strip()
                # Convert numeric values that are currently strings ('0' or '1') back to integers
                value = self.sheet[i, j, 1]
                if value == '0':
                    self.sheet[i, j, 1] = False
                elif value == '1':
                    self.sheet[i, j, 1] = True

    def play(self):
        print("PLAY")

        # Activate the target window
        window_title = "Virtual Piano - Online Piano Keyboard | OnlinePianist - Google Chrome"
        window = gw.getWindowsWithTitle(window_title)
        if window:
            window[0].activate()
        else:
            print(f"Window with title '{window_title}' not found.")
            return

        print("Now sleeping")
        time.sleep(1)  # Initial sleep for setup
        
        # Precompute key mappings: note -> index in self.keys
        key_mapping = {self.keys[i][2]: i for i in range(self.keys.shape[0])}

        for i_beat in range(self.sheet.shape[0]):  # Iterate over beats
            print(f"NOW PLAYING Beat {i_beat + 1}/{self.sheet.shape[0]}")
            time.sleep(self.t_divB)

            # Collect keys to press and release
            pressed_keys = []

            for i_pitch in range(self.sheet.shape[1]):  # Iterate over pitches
                pitch = self.sheet[i_beat][i_pitch][0]
                if isinstance(pitch, str):  # Ensure it's a string (not NaN)
                    i_key = key_mapping.get(pitch)
                    if i_key is not None:
                        self.press_key(i_key)  # Press the key
                        pressed_keys.append((i_pitch, i_key))  # Track pressed keys

            # Hold the note
            time.sleep(self.t - self.t_divB)

            # Release keys based on the sheet's information
            for i_pitch, i_key in pressed_keys:
                if not self.sheet[i_beat][i_pitch][1]:  # Check if the note should be released
                    control.release(self.keys[i_key][0])
            

        print('\n###                               EOF                                ###\n')
        return False

    def press_key(self,n):

        # command for the keyboard outputs
        #checks the value of the second entry in the keys array and decides if a white or black key should be pressed
        if self.keys[n][1] == '0':
            control.press(self.keys[n][0])           
        elif self.keys[n][1] == '1':
            with control.pressed(Key.shift):
                control.press(self.keys[n][0])

