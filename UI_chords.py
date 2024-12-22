import tkinter as tk
from tkinter import messagebox

from from_csv import application
from convert_chords import Convert_Chords

def compile_action():
    try:
        # Get the integer value from the input field
        title = str(string_entry.get())
        bpm = int(integer_entry.get())

        # Dynamically gather the string values from the table
        table_values = []
        for row in range(len(table_entries)):  # Iterate over rows
            table_row = []
            for col in range(len(table_entries[row])):  # Iterate over columns
                table_row.append(table_entries[row][col].get())
            table_values.append(table_row)

        # Process the values (for demonstration, just print them)
        print("Title = ", title)
        print("bpm = ", bpm)
        print("Table Values:", table_values)

    except ValueError:
        messagebox.showerror("Error", "Sumthin' Appen'd")

    runApp = Convert_Chords(title, bpm, table_values)
    runApp.conversion()
    runApp.write_csv()

    runApp = application(title)
    runApp.listen()

def add_column():
    # Get the selected column index where the new column will be added
    col_index = selected_add_column.get()

    # Create a new label for the column header
    new_label = tk.Label(frame2, text=f"{col_index + 1}", bg="lightgreen")
    new_label.config(font=("Arial", 6))
    new_label.grid(row=0, column=col_index, padx=1, pady=0, sticky="sw")

    # Shift existing labels to the right
    for shift_col in range(len(header_labels) - 1, col_index - 1, -1):
        existing_label = header_labels[shift_col]
        existing_label.grid(row=0, column=shift_col + 1)

    # Insert the new label into the header labels list
    header_labels.insert(col_index, new_label)

    # Create a list to store the new column's entries
    col_entries = []

    # For each row, add a new entry and shift subsequent entries to the right
    for row_index in range(len(table_entries)):
        # Create a new entry for the new column
        new_entry = tk.Entry(frame2, width=4)
        new_entry.grid(row=row_index + 1, column=col_index, padx=1, pady=1)  # Row index +1 for labels

        # Store the new entry in the new column list
        col_entries.append(new_entry)

        # Shift existing entries to the right
        for shift_col in range(len(table_entries[row_index]) - 1, col_index - 1, -1):
            existing_entry = table_entries[row_index][shift_col]
            existing_entry.grid(row=row_index + 1, column=shift_col + 1)

        # Insert the new entry into the table data structure
        table_entries[row_index].insert(col_index, new_entry)

    # Update column selection options
    update_column_options()

    # Update header label text for all columns to reflect the new indices
    update_header_labels()

def delete_selected_column():
    # Get the selected column index
    col_index = selected_delete_column.get()
    if col_index is None or col_index >= len(table_entries[0]):
        messagebox.showerror("Error", "No valid column selected!")
        return

    # Remove the header label for the specified column
    header_labels[col_index].grid_forget()
    header_labels.pop(col_index)

    # Shift remaining labels to the left
    for shift_col in range(col_index, len(header_labels)):
        header_labels[shift_col].grid(row=0, column=shift_col)

    # Remove all entries in the specified column
    for row_index in range(len(table_entries)):
        entry = table_entries[row_index][col_index]
        entry.grid_forget()  # Remove from the UI
        table_entries[row_index].pop(col_index)  # Remove from the data structure

    # Shift remaining columns to the left
    for row_index in range(len(table_entries)):
        for shift_col in range(col_index, len(table_entries[row_index])):
            entry = table_entries[row_index][shift_col]
            entry.grid(row=row_index + 1, column=shift_col)

    # Update column selection options
    update_column_options()

    # Update header label text for all columns to reflect the new indices
    update_header_labels()

def update_header_labels():
    for index, label in enumerate(header_labels):
        label.config(text=f"{index + 1}")  # Update to reflect new column indices

def update_column_options():
    # Update the dropdown menus for column selection
    column_options = list(range(len(table_entries[0]) + 1))  # +1 for the "end" option
    
    # Update the add column dropdown
    column_menu_add["menu"].delete(0, "end")
    for col in column_options:
        column_menu_add["menu"].add_command(label=col, command=lambda value=col: selected_add_column.set(value))

    column_options = list(range(len(table_entries[0])))

    # Update the delete column dropdown
    delete_column_options = list(range(1, len(table_entries[0]) + 1))  # 1-based indexing
    column_menu["menu"].delete(0, "end")
    for col in delete_column_options:
        column_menu["menu"].add_command(
            label=col, command=lambda value=col - 1: selected_delete_column.set(value)  # Match 0-based index
        )

# Create the main application window
print("######################################   UI_chords    ######################################")
root = tk.Tk()
root.title("UI Chords")

# Frame 1: First grid layout
frame1 = tk.Frame(root, bg="lightblue", bd=2, relief="solid")
frame1.grid(row=0, column=0, padx=10, pady=10, sticky="w")

tk.Label(frame1, text="Title = ").grid(row=0, column=0, padx=5, pady=5)
string_entry = tk.Entry(frame1)
string_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame1, text="bpm = ").grid(row=1, column=0, padx=5, pady=5)
integer_entry = tk.Entry(frame1)
integer_entry.grid(row=1, column=1, padx=5, pady=5)

# Frame 2: Second grid layout
frame2 = tk.Frame(root, bg="lightgreen", bd=2, relief="solid")
frame2.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Table structure
table_entries = []
header_labels = []

new_label = tk.Label(frame2, text=f"{1}", bg="lightgreen")
new_label.config(font=("Arial", 6))
new_label.grid(row=0, column=0, padx=1, pady=0, sticky="sw")

# Insert the new label into the header labels list
header_labels.insert(0, new_label)
update_header_labels()

# Create initial columns
for row in range(2):  # Create 2 rows initially
    row_entries = []
    for col in range(1):  # Create 1 initial column
        entry = tk.Entry(frame2, width=4)
        entry.grid(row=row+1, column=col, padx=1, pady=1)
        row_entries.append(entry)
    table_entries.append(row_entries)

# Frame 3: Controls
frame3 = tk.Frame(root, bg="lightyellow", bd=2, relief="solid")
frame3.grid(row=2, column=0, padx=10, pady=10, sticky="w")

# Add Column button
add_column_button = tk.Button(frame3, text="Add Column", command=add_column)
add_column_button.grid(row=0, column=0, padx=5, pady=1)

# Dropdown for selecting column to add the new column before
selected_add_column = tk.IntVar()
selected_add_column.set(0)
column_menu_add = tk.OptionMenu(frame3, selected_add_column, 0)
column_menu_add.grid(row=1, column=0, padx=5, pady=1)

# Delete Column button
delete_column_button = tk.Button(frame3, text="Delete Column", command=delete_selected_column)
delete_column_button.grid(row=0, column=1, padx=5, pady=1)

# Dropdown for selecting column to delete
selected_delete_column = tk.IntVar()
selected_delete_column.set(1)
column_menu = tk.OptionMenu(frame3, selected_delete_column, 0)
column_menu.grid(row=1, column=1, padx=5, pady=1)

# Compile Button
compile_button = tk.Button(frame3, text="Compile", command=compile_action)
compile_button.grid(row=0, column=2, padx=5, pady=1)

# Update column options for both add and delete dropdowns
update_column_options()

# Start the Tkinter event loop
root.mainloop()
