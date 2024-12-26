
import numpy as np
import csv
import os

class ConvertBase():

    def __init__(self, title, bpm):
        super().__init__()
        
        # Input data from UI
        self.title = title
        self.bpm = bpm

        # map of minimum beat lengths (for example e. = 3*s => min(e.) = 1/16)
        self.beats_min = {
                        "f" : 1,
                        "h.": 1/4,
                        "h" : 1/2,
                        "q.": 1/8,
                        "q" : 1/4,
                        "e.": 1/16,
                        "e" : 1/8,
                        "s.": 1/32,
                        "s" : 1/16
                        }
        
        # map of absolute beat lengths (for example e. = 3*s => abs(e.) = 3*1/16 = 1/8+1/16)
        self.beats_abs = {
                        "f" : 1,
                        "h.": 1/2+1/4,
                        "h" : 1/2,
                        "q.": 1/4+1/8,
                        "q" : 1/4,
                        "e.": 1/8+1/16,
                        "e" : 1/8,
                        "s.": 1/16+1/32,
                        "s" : 1/16
                        }

    def write_csv(self):

        #Debugging Output
        print("csv_sheet.shape = ", self.csv_sheet.shape)
        for row in self.csv_sheet:
            print(row)

        filename = f".\CSV\{self.title}.csv"

        if os.path.exists(filename):
            os.remove(filename)
            print(f"Existing file {filename} deleted.")

        # Open the file for writing
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file, delimiter=";")  # Use tab as delimiter

            # Write metadata as comments
            writer.writerow(["self.title"])
            writer.writerow(["# bpm =", self.bpm, "#1/min"])
            writer.writerow(["# minimum beat =", self.shortest_beat])
            writer.writerow([])
            writer.writerow(["# time per measure", round(self.t_per_measure, 3), "#s"])
            writer.writerow(["# time per minimum beat", round(self.t_per_beat, 3), "#s"])
            writer.writerow([])

            #dynamic header
            longest_row_len = max(len(row) for i in self.csv_sheet for row in i)
            
            header = ["#measure", "#nr minimum beat"]  # Fixed part
            for i in range(1, (longest_row_len - 2) // 2 + 1):  # Dynamic part
                header.append(f"#note {i}")
                header.append(f"#duration {i}")
            writer.writerow(header)

            # Flatten and write the rows
            for beat_arr in self.csv_sheet:
                for row in beat_arr:
                    flat_row = []
                    for item in row:
                        # Convert all elements to strings to avoid issues
                        flat_row.append(str(item))
                    writer.writerow(flat_row)

            print(f"Data saved to {filename}")