import tkinter as tk
from tkinter import messagebox, filedialog
import configparser

from play import Play

class UIBase(tk.Tk):
    def __init__(self):
        super().__init__()

        # default cases for save and load methods. Will get overruled by inheriting classes
        self.file_extension = ".cfg"  # Default file extension
        self.file_type_desc = "Config files"  # Default file type description

        ################ Frame for general settings #########################################################
        self.frame_set = tk.Frame(self, bg="lightblue", bd=2, relief="solid")
        self.frame_set.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        tk.Label(self.frame_set, text="Title = ").grid(row=0, column=0, padx=5, pady=5)
        self.string_entry = tk.Entry(self.frame_set)
        self.string_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_set, text="bpm = ").grid(row=1, column=0, padx=5, pady=5)
        self.integer_entry = tk.Entry(self.frame_set)
        self.integer_entry.grid(row=1, column=1, padx=5, pady=5)

        ################ Frame for options ##################################################################
        self.frame_optn = tk.Frame(self, bg="lightyellow", bd=2, relief="solid")
        self.frame_optn.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Buttons and dropdowns for columns
        self.add_column_button = tk.Button(self.frame_optn, text="Add Column", command=self.add_column)
        self.add_column_button.grid(row=0, column=0, padx=5, pady=1)

        self.selected_add_column = tk.IntVar()
        self.selected_add_column.set(0)
        self.column_menu_add = tk.OptionMenu(self.frame_optn, self.selected_add_column, 0)
        self.column_menu_add.grid(row=1, column=0, padx=5, pady=1)

        self.delete_column_button = tk.Button(self.frame_optn, text="Delete Column", command=self.delete_column)
        self.delete_column_button.grid(row=0, column=1, padx=5, pady=1)

        self.selected_delete_column = tk.IntVar()
        self.selected_delete_column.set(1)
        self.column_menu = tk.OptionMenu(self.frame_optn, self.selected_delete_column, 0)
        self.column_menu.grid(row=1, column=1, padx=5, pady=1)

        # Save and Load buttons
        self.save_button = tk.Button(self.frame_optn, text="Save", command=self.save_to_cfg)
        self.save_button.grid(row=0, column=2, padx=5, pady=1)

        self.load_button = tk.Button(self.frame_optn, text="Load", command=self.load_from_cfg)
        self.load_button.grid(row=1, column=2, padx=5, pady=1)

        # Compile Button
        compile_button = tk.Button(self.frame_optn, text="Compile", command=self.compile_action)
        compile_button.grid(row=0, column=3, padx=5, pady=1)

        # Play Button
        play_button = tk.Button(self.frame_optn, text="PlayIt", command=self.play_action)
        play_button.grid(row=1, column=3, padx=5, pady=1)

        ################  Frame for rhythm table ##################################################################
        self.frame_rthm = tk.Frame(self, bg="lightgreen", bd=2, relief="solid")
        self.frame_rthm.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Table data
        self.table_entries = []
        self.header_labels = []

    def compile_action(self):
        # Process and compile data
        try:
            # Get the integer value from the input field
            self.title, bpm, table_values = self.get_entries()

            # Process the values (for demonstration, just print them)
            print("Title = ", self.title)
            print("bpm = ", bpm)
            print("Table Values:", table_values)

        except ValueError:
            messagebox.showerror("Error", "Sumthin' Appen'd")
        """
        converter = ConvertChords(self.title, bpm, table_values)
        # adding Chords from UI
        converter.add_chord("R", [""])  # Rest or silence
        for i in range(len(self.chords)):
            converter.add_chord(self.chords[i][0],self.chords[i][1])
            print(self.chords[i][0], ': ', self.chords[i][1])
        converter.conversion()
        converter.write_csv()
        """
        # Delegate specific processing to the child class
        self.process_data(self.title, bpm, table_values)

    def process_data(self, title, bpm, table_values):
        """
        Placeholder method to be overridden by child classes.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def play_action(self):
        runApp = Play(self.title)
        runApp.listen()

    def add_column(self):
        # Add column functionality
        # Get the selected column index where the new column will be added
        col_index = self.selected_add_column.get()

        # Create a new label for the column header
        new_label = tk.Label(self.frame_rthm, text=f"{col_index + 1}", bg="lightgreen")
        new_label.config(font=("Arial", 6))
        new_label.grid(row=0, column=col_index, padx=1, pady=0, sticky="sw")

        # Shift existing labels to the right
        for shift_col in range(len(self.header_labels) - 1, col_index - 1, -1):
            existing_label = self.header_labels[shift_col]
            existing_label.grid(row=0, column=shift_col + 1)

        # Insert the new label into the header labels list
        self.header_labels.insert(col_index, new_label)

        # Create a list to store the new column's entries
        col_entries = []

        # For each row, add a new entry and shift subsequent entries to the right
        for row_index in range(len(self.table_entries)):
            # Create a new entry for the new column
            new_entry = tk.Entry(self.frame_rthm, width=4)
            new_entry.grid(row=row_index + 1, column=col_index, padx=1, pady=1)  # Row index +1 for labels

            # Store the new entry in the new column list
            col_entries.append(new_entry)

            # Shift existing entries to the right
            for shift_col in range(len(self.table_entries[row_index]) - 1, col_index - 1, -1):
                existing_entry = self.table_entries[row_index][shift_col]
                existing_entry.grid(row=row_index + 1, column=shift_col + 1)

            # Insert the new entry into the table data structure
            self.table_entries[row_index].insert(col_index, new_entry)

        # Update column selection options
        self.update_column_options()

        # Update header label text for all columns to reflect the new indices
        self.update_header_labels()

    def delete_column(self):
        # Delete column functionality
        # Get the selected column index
        col_index = self.selected_delete_column.get()
        if col_index is None or col_index >= len(self.table_entries[0]):
            messagebox.showerror("Error", "No valid column selected!")
            return

        # Remove the header label for the specified column
        self.header_labels[col_index].grid_forget()
        self.header_labels.pop(col_index)

        # Shift remaining labels to the left
        for shift_col in range(col_index, len(self.header_labels)):
            self.header_labels[shift_col].grid(row=0, column=shift_col)

        # Remove all entries in the specified column
        for row_index in range(len(self.table_entries)):
            entry = self.table_entries[row_index][col_index]
            entry.grid_forget()  # Remove from the UI
            self.table_entries[row_index].pop(col_index)  # Remove from the data structure

        # Shift remaining columns to the left
        for row_index in range(len(self.table_entries)):
            for shift_col in range(col_index, len(self.table_entries[row_index])):
                entry = self.table_entries[row_index][shift_col]
                entry.grid(row=row_index + 1, column=shift_col)

    # Update column selection options
    def update_column_options(self):
        # Update the dropdown menus for column selection
        column_options = list(range(len(self.table_entries[0]) + 1))  # +1 for the "end" option
    
        # Update the add column dropdown
        self.column_menu_add["menu"].delete(0, "end")
        for col in column_options:
            self.column_menu_add["menu"].add_command(label=col, command=lambda value=col: self.selected_add_column.set(value))

        column_options = list(range(len(self.table_entries[0])))

        # Update the delete column dropdown
        delete_column_options = list(range(1, len(self.table_entries[0]) + 1))  # 1-based indexing
        self.column_menu["menu"].delete(0, "end")
        for col in delete_column_options:
            self.column_menu["menu"].add_command(
                label=col, command=lambda value=col - 1: self.selected_delete_column.set(value)  # Match 0-based index
            )  

    def clear_all_columns(self):

        # Remove all header labels except the first one
        for header_label in self.header_labels[1:]:  # Skip the first column
            header_label.grid_forget()
        self.header_labels = self.header_labels[:1]  # Keep only the first column's label

        # Remove all table entries except those in the first column
        for row in self.table_entries:
            for entry in row[1:]:  # Skip the first column
                entry.grid_forget()
            del row[1:]  # Keep only the first column's entries

        # Update column options
        self.update_column_options() 

    # Update header label text for all columns to reflect the new indices
    def update_header_labels(self):
        for index, label in enumerate(self.header_labels):
            label.config(text=f"{index + 1}")  # Update to reflect new column indices

    def save_to_cfg(self):
        # Save configuration to file
        try:
            self.title, bpm, table_values = self.get_entries()

            # Create a configparser object
            config = configparser.ConfigParser()
            config['GENERAL'] = {
                'Title': self.title,
                'BPM': bpm
            }

            # Add table values as a separate section
            config['TABLE'] = {f'Row{i}': ','.join(row) for i, row in enumerate(table_values)}

            # Add chords to the config
            config['CHORDS'] = {}
            for i, (chord_name, chord_list) in enumerate(self.chords):
                # Save each chord's name and list of chord values as a comma-separated string
                config['CHORDS'][f'Chord_{i+1}'] = f"{chord_name}:{','.join(chord_list)}"

            # Open save dialog
            file_path = filedialog.asksaveasfilename(defaultextension=self.file_extension, filetypes=[(self.file_type_desc, self.file_extension)])
            if not file_path:
                return

            # Write to file
            with open(file_path, 'w') as configfile:
                config.write(configfile)

            messagebox.showinfo("Success", "Data saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

    def load_from_cfg(self):
        # Load configuration from file
        try:
            # Open load dialog
            file_path = filedialog.askopenfilename(filetypes=[(self.file_type_desc, self.file_extension)])
            if not file_path:
                return

            # Create a configparser object and read the file
            config = configparser.ConfigParser()
            config.read(file_path)

            # Load general data
            self.title = config['GENERAL']['Title']
            bpm = config['GENERAL']['BPM']

            # Load table values
            table_values = [row.split(',') for row in config['TABLE'].values()]

            # Load chords
            self.chords.clear()  # Clear any existing chords
            for key in config['CHORDS']:
                chord_data = config['CHORDS'][key]
                chord_name, chord_list_str = chord_data.split(':')
                chord_list = chord_list_str.split(',')
                self.chords.append((chord_name, chord_list))

            # Update UI with loaded chords
            self.update_chords_display()

            # Update title and bpm entries
            self.string_entry.delete(0, tk.END)
            self.string_entry.insert(0, self.title)

            self.integer_entry.delete(0, tk.END)
            self.integer_entry.insert(0, bpm)

            # Adjust table size if necessary
            self.clear_all_columns()

            # Rebuild the table with new values
            for row_index, row_values in enumerate(table_values):
                for col_index, value in enumerate(row_values):
                    # Ensure the column exists
                    if col_index >= len(self.table_entries[row_index]):
                        # Add a new header label if necessary
                        if len(self.header_labels) <= col_index:
                            new_label = tk.Label(self.frame_rthm, text=f"{col_index + 1}", bg="lightgreen")
                            new_label.config(font=("Arial", 6))
                            new_label.grid(row=0, column=col_index, padx=1, pady=0, sticky="sw")
                            self.header_labels.append(new_label)

                        # Add a new entry to the table
                        new_entry = tk.Entry(self.frame_rthm, width=4)
                        new_entry.grid(row=row_index + 1, column=col_index, padx=1, pady=1)
                        self.table_entries[row_index].append(new_entry)

                    # Populate the entry with the loaded value
                    self.table_entries[row_index][col_index].delete(0, tk.END)
                    self.table_entries[row_index][col_index].insert(0, value)

            # Update header labels and column options
            self.update_header_labels()
            self.update_column_options()

            messagebox.showinfo("Success", "Data loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def get_entries(self):
        # Get general data from UI
        self.title = self.string_entry.get()
        bpm = self.integer_entry.get()
        table_values = [[entry.get() for entry in row] for row in self.table_entries]

        return self.title, bpm, table_values

