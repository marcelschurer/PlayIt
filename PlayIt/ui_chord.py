import tkinter as tk
from tkinter import messagebox

from ui_base import UIBase
from convert_chords import ConvertChords

class UIChord(UIBase):
    def __init__(self):
        super().__init__()

        # cases for save and load methods. Overrules default case in UIBase
        self.file_extension = ".chrd"
        self.file_type_desc = "Chord files"

        ################ Frame for chords ##################################################################
        self.frame_chords = tk.Frame(self, bg="salmon1", bd=2, relief="solid")
        self.frame_chords.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="ns")

        tk.Label(self.frame_chords, text="Chords", bg="salmon1").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.add_chord_button = tk.Button(self.frame_chords, text="Add Chord", command=self.add_chord)
        self.add_chord_button.grid(row=1, column=0, padx=5, pady=1)

        self.delete_chord_button = tk.Button(self.frame_chords, text="Delete Chord", command=self.delete_chord)
        self.delete_chord_button.grid(row=2, column=0, padx=5, pady=1)

        # List to store chords
        self.chords = []

        ################ Implementing Ryrhm frame for Chords ##################################################################
        new_label = tk.Label(self.frame_rthm, text=f"{1}", bg="lightgreen")
        new_label.config(font=("Arial", 6))
        new_label.grid(row=0, column=0, padx=1, pady=0, sticky="sw")

        # Insert the new label into the header labels list
        # Initialize table
        self.initialize_table()

        self.header_labels.insert(0, new_label)
        self.update_column_options()
        self.update_header_labels()

    def process_data(self, title, bpm, table_values):
        # Specific logic for processing chord data
        converter = ConvertChords(title, bpm, table_values)

        # Adding chords from UI
        converter.add_chord("R", [""])  # Rest or silence
        for chord_name, chord_notes in self.chords:
            converter.add_chord(chord_name, chord_notes)
            print(chord_name, ': ', chord_notes)

        # Perform conversion and save to CSV
        converter.conversion()
        converter.write_csv()

    def initialize_table(self):
        # Create initial columns
        for row in range(2):  # Create 2 rows initially
            row_entries = []
            for col in range(1):  # Create 1 initial column
                entry = tk.Entry(self.frame_rthm, width=4)
                entry.grid(row=row + 1, column=col, padx=1, pady=1)
                row_entries.append(entry)
            self.table_entries.append(row_entries)

    def add_chord(self):
        # Add chord functionality
        # Open a new window for chord input
        chord_window = tk.Toplevel(self)
        chord_window.title("Add Chord")

        # Labels and entries for chord name and list
        tk.Label(chord_window, text="Chord Name:").grid(row=0, column=0, padx=5, pady=5)
        chord_name_entry = tk.Entry(chord_window)
        chord_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(chord_window, text="Notes (comma-separated):").grid(row=1, column=0, padx=5, pady=5)
        chord_list_entry = tk.Entry(chord_window)
        chord_list_entry.grid(row=1, column=1, padx=5, pady=5)

        # Function to handle submission of chord
        def submit_chord():
            chord_name = chord_name_entry.get().strip()
            chord_list = chord_list_entry.get().strip()

            # Validate inputs
            if not chord_name:
                messagebox.showerror("Error", "Chord name cannot be empty!")
                return
            if not chord_list:
                messagebox.showerror("Error", "Chord list cannot be empty!")
                return

            # Add chord to the list and update the frame
            self.chords.append((chord_name, chord_list.split(',')))

            # Display the added chord in the chords frame
            self.update_chords_display()

            # Close the chord input window
            chord_window.destroy()

        # Submit button
        tk.Button(chord_window, text="Submit", command=submit_chord).grid(row=2, column=0, columnspan=2, pady=10)

    def delete_chord(self):
        # Delete chord functionality
        # Open a new window for chord deletion
        delete_window = tk.Toplevel(self)
        delete_window.title("Delete Chord")

        # List the available chords with indices for user selection
        tk.Label(delete_window, text="Select Chord to Delete:").grid(row=0, column=0, padx=5, pady=5)

        # Dropdown for selecting chord to delete
        selected_chord_index = tk.IntVar()
        if self.chords:  # Ensure there are chords to delete
            selected_chord_index.set(0)  # Default to the first chord
            chord_options = [f"{i+1}. {name}" for i, (name, _) in enumerate(self.chords)]
        else:
            chord_options = ["No chords available"]

        chord_menu = tk.OptionMenu(delete_window, selected_chord_index, *range(len(self.chords)))
        chord_menu.grid(row=1, column=0, padx=5, pady=5)

        # Function to confirm and delete the selected chord
        def confirm_delete():
            if not self.chords:
                messagebox.showerror("Error", "No chords available to delete!")
                return

            index_to_delete = selected_chord_index.get()
            if 0 <= index_to_delete < len(self.chords):
                self.chords.pop(index_to_delete)  # Remove the chord from the list
                self.update_chords_display()  # Update the display
                delete_window.destroy()  # Close the window
            else:
                messagebox.showerror("Error", "Invalid chord selection!")

        # Delete button
        tk.Button(delete_window, text="Delete", command=confirm_delete).grid(row=2, column=0, pady=10)

        # Cancel button
        tk.Button(delete_window, text="Cancel", command=delete_window.destroy).grid(row=3, column=0, pady=10)

    def update_chords_display(self):
        # Update the chord display in the frame
            # Clear existing widgets in the frame, but skip title and add button
        for widget in self.frame_chords.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text") == "Chords":
                continue
            if widget == self.add_chord_button:
                continue
            if widget == self.delete_chord_button:
                continue
            widget.destroy()

        # Display each chord starting from row 2 to avoid overlap
        for index, (name, chord_list) in enumerate(self.chords, start=1):
            tk.Label(self.frame_chords, text=f"{name}: {', '.join(chord_list)}", bg="salmon1", anchor="w").grid(
                row=index + 3, column=0, padx=5, pady=2, sticky="w"
            )

