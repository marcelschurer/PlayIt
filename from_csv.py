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
#import sys

class application:

    def __init__(self,title):

        print("######################################   from_csv    ######################################")
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
        
        # Load the CSV file
        file_path = f".\CSV\{title}.csv"

        print('\n################', title, ' #################\n')

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

        # Convert numeric values that are currently strings ('0' or '1') back to integers
        for i in range(self.sheet.shape[0]):  # Iterate over the first dimension
            for j in range(self.sheet.shape[1]):  # Second dimension

                value = self.sheet[i, j, 1]
                if value == '0':
                    self.sheet[i, j, 1] = False
                elif value == '1':
                    self.sheet[i, j, 1] = True

        '''
        print('n_1 = ', self.sheet.shape[0])
        print('n_2 = ', self.sheet.shape[1])
        print('n_3 = ', self.sheet.shape[2])
        
        print(self.sheet[:, :, 0])
        print(self.sheet[:, :, 1])
        
        for i in range(self.sheet.shape[0]):  # Iterate over the first dimension
            for j in range(self.sheet.shape[1]):  # Second dimension
                for k in range(self.sheet.shape[2]):  # Third dimension
                    print(f"Element at ({i}, {j}, {k}): {self.sheet[i, j, k]} - Type: {type(self.sheet[i, j, k])}")
        '''
        #sys.exit()

    def listen(self):
        
        print('press <+> to play notes\n')
        
        # starting keyboard listener
        #self.keyboard_listener = KeyboardListener(on_press=self.on_press)
        #self.keyboard_listener.start()
        #self.keyboard_listener.join()

        print('\n### Listening for keyboard input ###\n')
        with KeyboardListener(on_press=self.on_press) as listener:
            listener.join()  # Wait for the listener to be stopped

    def on_press(self,key):

        # Kill switch
        if key == keyboard.Key.esc:
            print('TERMINATING')
            self.stop = True  # Set stop flag
            return False  # Stop the listener
            #return False
            #sys.exit()
        
        ##########################################################################################

        for i_beat in range(self.sheet.shape[0]):                                       # iterates over beats
            
            print("NOW PLAYING")
            time.sleep(self.t_divB)

            #empty array which save the currently played notes
            array_sheet = np.empty((0, 2), dtype=int)

            for i_pitch in range(self.sheet.shape[1]):                                  #iterates ofer pitch
                if isinstance(self.sheet[i_beat][i_pitch][0], str):                     #checks if pitch entry is string or nan

                    #searching comparing sheet array with key array
                    for i_key in range(self.keys.shape[0]):
                        if self.keys[i_key][2] == self.sheet[i_beat][i_pitch][0]:
                            self.press_key(i_key)                                       # pressing key

                            new_row = np.array([[i_pitch, i_key]])                      # saving the pressed key in empty array
                            array_sheet = np.vstack((array_sheet, new_row))

            #sys.exit()
            time.sleep(self.t-self.t_divB)                                              # hold note for this time

            for i in range(array_sheet.shape[0]):                                       # checking if key should be released based on array_sheet
                if self.sheet[i_beat][array_sheet[i][0]][1] == False:
                    control.release(self.keys[array_sheet[i][1]][0])           

        ##########################################################################################

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

