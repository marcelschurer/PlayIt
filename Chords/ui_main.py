#from ui_chord import UIChord
#
#if __name__ == "__main__":
#    root = UIChord()
#    root.mainloop()

import tkinter as tk
from ui_chord import UIChord
from ui_tab_sheet import UITabSheet

class UIMain:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Main Selection Interface")

        # Create and configure main frame
        self.frame = tk.Frame(self.root, width=300, height=200)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create a label for the interface
        self.label = tk.Label(self.frame, text="Select an Option", font=("Arial", 14, "bold"))
        self.label.pack(pady=10)

        # Variable to track the selected option
        self.selected_option = tk.StringVar(value="Chords")

        # Create radio buttons for options
        self.options = ["Chords", "Tabs", "Sheet"]
        for option in self.options:
            tk.Radiobutton(
                self.frame,
                text=option,
                variable=self.selected_option,
                value=option,
                font=("Arial", 12),
                command=self.on_option_selected
            ).pack(anchor=tk.W, padx=20, pady=5)

        # Button to proceed with the selected option
        self.proceed_button = tk.Button(
            self.frame, text="Proceed", command=self.run_selected_option, font=("Arial", 12, "bold")
        )
        self.proceed_button.pack(pady=20)

        self.root.mainloop()

    def on_option_selected(self):
        """Update label or perform actions based on the selected option."""
        print(f"Selected Option: {self.selected_option.get()}")

    def run_selected_option(self):
        """Run the appropriate UI class based on the selected option."""
        selected = self.selected_option.get()
        self.root.destroy()  # Close the main interface

        if selected == "Chords":
            UIChord()  # Launch the UIChords interface
        elif selected == "Tabs":
            UITabSheet()  # Launch the UITabSheet interface
        elif selected == "Sheet":
            UITabSheet()  # Launch the UITabSheet interface
        else:
            print("No option Selected")

# Run the application
if __name__ == "__main__":
    UIMain()
