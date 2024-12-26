
import numpy as np
import csv
import os

from chord import Chord
from convert_base import ConvertBase

class ConvertChords(ConvertBase):

    def __init__(self, title, bpm, table_values):
        super().__init__(title, bpm)
        print("################   convert_chords    ################")
        
        # Input data from UI
        self.chord_list = table_values

        # converting to numpy array and transposing
        self.chord_list = np.array(self.chord_list).T

        # Remove spaces from all strings in the array
        self.chord_list = np.char.replace(self.chord_list, ' ', '')

        # filling the chord column with the last previous chord
        last_string = "R"
        for i in range(self.chord_list.shape[0]):
            if self.chord_list[i, 0]:                   # Check if the current value is non-empty
                last_string = self.chord_list[i, 0]
            self.chord_list[i, 0] = last_string

        """
        # Iterate over columns
        for i in range(self.chord_list.shape[0]):
            print(self.chord_list[i, 0], ', ', self.chord_list[i, 1])  # Access each chord in the first row

        print(self.chord_list[0, 0])
        print(self.chord_list[0, 1])
        """
        
        # Initialize empty chord collection
        self.chords = {}
        """
        # Format of the Chord map (Class each)
        self.chords = {
                        "Em": ['e3', 'b3', 'g3'],
                        "C": ['c3', 'e3', 'g3'],
                        "G": ['g3', 'b3', 'd3', 'g4'],
                        "R": ['']
                      }
        """
    def add_chord(self, chord_name, notes):
        """
        Adds a new chord to the collection of chords as a `Chord` object.
        """
        self.chords[chord_name] = Chord(chord_name, notes)
    
    def conversion(self):

        # finding the shortest beat in the composition
        self.shortest_beat = self.beats_min["f"]
        for i in range(self.chord_list.shape[0]):
            if self.beats_min[self.chord_list[i][1]] < self.shortest_beat:
                self.shortest_beat = self.beats_min[self.chord_list[i][1]]
        
        print('shortest beat = ', self.shortest_beat)

        self.t_per_measure = 4*60/int(self.bpm)
        self.t_per_beat = self.t_per_measure*self.shortest_beat
        # Position of the first note
        pos = 0

        # Initialize an empty list to collect rows
        self.csv_sheet = []

        # Iterate through lines of `chord_list`
        for i_chord in range(self.chord_list.shape[0]):

            # Number of measures
            no_measure = int((pos - (pos % 1)) + 1)

            # Initialize beat_arr as an empty list to store rows
            beat_arr = []

            # Iterate through the length of the beat
            for i_beat in range(int(self.beats_abs[self.chord_list[i_chord][1]] / self.shortest_beat)):

                # Determine the number on the minimum beat scale
                no_min = int((pos + i_beat * self.shortest_beat) / self.shortest_beat + 1)

                # Collect note rows
                note_row = []
                for i_note in range(len((self.chords[self.chord_list[i_chord][0]]).get_notes())):
                    # Check if its the last duration of the shortest beat
                    if i_beat == self.beats_abs[self.chord_list[i_chord][1]] / self.shortest_beat - 1:
                        note = [(self.chords[self.chord_list[i_chord][0]]).get_notes()[i_note], 0]
                    else:
                        note = [(self.chords[self.chord_list[i_chord][0]]).get_notes()[i_note], 1]

                    note_row.extend(note)
                    #print("note_row = \n", note_row)

                # Combine measure number, min beat, and notes into a single row
                beat_row = [no_measure, no_min] + note_row
                beat_arr.append(beat_row)  # Append each row to beat_arr

                #print("beat_row = \n", beat_row)

            # Convert beat_arr to a NumPy array before adding to csv_sheet
            self.csv_sheet.append(np.array(beat_arr))

            # Update position (for next beat)
            try:
                pos += self.beats_abs[self.chord_list[i_chord][1]]
                #print("pos = \n", pos)
            except IndexError:
                #print("THIS SHOULD ONLY HAPPEN AT THE END")
                break

        # Convert csv_sheet to a NumPy array
        self.csv_sheet = np.array(self.csv_sheet, dtype=object)  # Use `dtype=object` for nested arrays