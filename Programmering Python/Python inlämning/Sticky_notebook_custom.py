import customtkinter as ctk  # Import CustomTkinter for modern GUI widgets
import tkinter.messagebox  # Import messagebox for displaying pop-up messages to the user (compatible with CustomTkinter)
import json  # Import JSON module for saving and loading data persistently in a file

# Set a default color theme for better appearance (blue accents)
ctk.set_default_color_theme("blue")

# Dark mode
DARK_BG        = "#1e1e1e"   # whole window
DARK_TAB_BG    = "#2d2d2d"   # tab header background
DARK_TEXT_BG   = "#3a3a3a"   # note editor 

# Light mode
LIGHT_BG       = "#e5e5e5"   # window background
LIGHT_TEXT_BG  = "#ffffff"   # white editor

# Tab colors for light mode (blue with variations for visibility)
LIGHT_SEG_UNSELECTED        = "#3B8ED0"  # same as button normal
LIGHT_SEG_SELECTED          = "#1F6AA5"  # darker blue for selected
LIGHT_SEG_UNSELECTED_HOVER  = "#36719F"  # hover for unselected
LIGHT_SEG_SELECTED_HOVER    = "#144870"  # hover for selected

# Buttons default theme
BUTTON_FG      = None        # Let the blue theme decide

# Define a class to represent individual notes
class Note:
    def __init__(self, note_id, text=""):
        # Initialize the Note object with an ID and optional text
        self.note_id = note_id  # Attribute 1: Unique identifier for the note
        self.text = text        # Attribute 2: The content/text of the note

    #Method to update the notes text.
    def update_text(self, new_text):
           # Check if the new text is a string using isinstance for type validation
        if isinstance(new_text, str):  # Using isinstance for type checking
            self.text = new_text  # Update the text if valid
        else:
            # Raise an error if the input is not a string
            raise ValueError("Text must be a string.")

# Define the main application class that inherits from ctk.CTk to create the GUI window
class NoteApp(ctk.CTk):
    def __init__(self):
        # Call the parent class constructor to initialize the CustomTkinter window
        super().__init__()
        # Set the window title
        self.title("Sticky Notes")
        # Set the initial window size (increased for better button visibility)
        self.geometry("600x400")

        # Set the initial appearance mode to 'Dark' for better contrast (Dark Grey theme)
        ctk.set_appearance_mode("Dark")

        # Dictionary to store Note objects, with note_id as key and Note instance as value
        self.notes = {}  # Dictionary to store Note objects, key: note_id, value: Note object
        # Load any existing notes from the persistent file
        self.load_notes()  # Load persistent data

        # Create a frame to hold the buttons at the top of the window with some padding
        self.button_frame = ctk.CTkFrame(self)  # Button frame on top
        self.button_frame.pack(fill='x', pady=5)  # Pack with vertical padding for better spacing

        # Configure grid columns to expand equally for responsive buttons
        self.button_frame.columnconfigure((0, 1, 2, 3), weight=1)

        # Add buttons using grid for better resizing behavior
        ctk.CTkButton(self.button_frame, text="Add Note", command=self.add_note).grid(row=0, column=0, padx=5, sticky='ew')
        ctk.CTkButton(self.button_frame, text="Remove Note", command=self.remove_note).grid(row=0, column=1, padx=5, sticky='ew')
        ctk.CTkButton(self.button_frame, text="Clear Note", command=self.clear_note).grid(row=0, column=2, padx=5, sticky='ew')
        
        # Add the theme toggle button as an instance variable for dynamic text update
        initial_text = "Light Mode" if ctk.get_appearance_mode() == "Dark" else "Dark Mode"
        self.theme_button = ctk.CTkButton(self.button_frame, text=initial_text, command=self.toggle_theme)
        self.theme_button.grid(row=0, column=3, padx=5, sticky='ew')

        # Create a CTkTabview widget to handle multiple tabs (each tab is a note), with custom settings for better look
        self.notebook = ctk.CTkTabview(self, anchor="center", border_width=0, corner_radius=6) # Center tabs, rounded corners
        # Pack the tabview to expand and fill the available space
        self.notebook.pack(expand=True, fill='both')

        # Initialize the counter for the next note ID
        self.current_id = 1
        # Get a list of existing note IDs from the dictionary keys
        note_ids = list(self.notes.keys())  # Using list for note IDs
        if note_ids:
            # If there are existing notes, loop through sorted IDs and add tabs for each
            for i, note_id in enumerate(sorted(note_ids)):  # Using loop with enumerate on sorted list
                note = self.notes[note_id]  # Retrieve the note object
                self.add_tab(note.note_id, note.text)  # Add a tab for the note
            # Update the current_id to be one more than the maximum existing ID
            self.current_id = max(note_ids) + 1
        else:
            # If no notes exist, add an initial note
            self.add_note()  # Add initial note if none exist

        # Update colors initially
        self.update_colors()

        # Set up a protocol to call on_close when the window is closed (for saving data)
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle window close for saving

    #Function to add a new note.
    def add_note(self):
        # Get the next available note ID
        note_id = self.current_id
        # Create a new Note object
        new_note = Note(note_id)
        # Add the new note to the dictionary
        self.notes[note_id] = new_note
        # Add a new tab to the tabview for this note
        self.add_tab(note_id)
        # Select the newly added tab to switch to it immediately
        self.notebook.set(f"Note {note_id}")  # Switch to the new note
        # Increment the current ID for the next note
        self.current_id += 1
        # Display a message confirming the addition with the specific note ID
        self.display_message(f"Note {note_id} added successfully.")  # User feedback with specific note

    #Function to remove the currently selected note.
    def remove_note(self):
        # Get the currently selected tab name
        current_tab = self.notebook.get()
        if current_tab:  # If-statement to check if a tab is selected
            # Extract the note ID from the tab name
            try:
                note_id = int(current_tab.split()[1])  # Extract note_id
                # Remove the tab from the tabview
                self.notebook.delete(current_tab)
                # Delete the note from the dictionary
                del self.notes[note_id]  # Remove from dictionary
                # Sync any changes in text to the note objects
                self.sync_notes()  # Sync remaining notes
                # Renumber the remaining notes to fill any gaps in IDs
                self.renumber_notes()
                # Display a message confirming removal with the specific note ID
                self.display_message(f"Note {note_id} removed successfully.")  # User feedback with specific note
                # If no notes left, add a new one to avoid empty tabview
                if not self.notes:
                    self.add_note()
            except ValueError:
                # Display an error message if extraction fails
                self.display_message("Error removing note.")  # Error feedback
        else:
            # Display a message if no note is selected
            self.display_message("No note selected to remove.")

    #Function to clear the current notes text
    def clear_note(self):
        # Get the currently selected tab name
        current_tab = self.notebook.get()
        if current_tab:  # If-statement for condition
            # Get the frame widget for the current tab
            frame = self.notebook.tab(current_tab)
            # Get the text widget from the frames children
            text_widget = frame.winfo_children()[0] if frame.winfo_children() else None
            if isinstance(text_widget, ctk.CTkTextbox):  # Using isinstance to check if its a CTkTextbox widget
                # Delete all text from the widget
                text_widget.delete('1.0', 'end')
                # Extract the note ID
                try:
                    note_id = int(current_tab.split()[1])
                    # Update the note objects text to empty
                    self.notes[note_id].update_text("")  # Update using class method
                    # Display a message confirming clearing with the specific note ID
                    self.display_message(f"Note {note_id} cleared successfully.")  # User feedback with specific note
                except ValueError:
                    # Display an error if extraction fails
                    self.display_message("Error clearing note.")
        else:
            # Display a message if no note is selected
            self.display_message("No note selected to clear.")

    def add_tab(self, note_id, text=""):
        name = f"Note {note_id}"
        frame = self.notebook.add(name)

        # Pick the correct editor colour **right now**
        mode = ctk.get_appearance_mode()
        editor_bg = DARK_TEXT_BG if mode == "Dark" else LIGHT_TEXT_BG

        text_widget = ctk.CTkTextbox(
            frame,
            wrap="word",
            fg_color=editor_bg,          
        )
        text_widget.insert("end", text)
        text_widget.pack(expand=True, fill="both")

    #Function to display feedback to the user
    def display_message(self, message):
        # Show an info message box with the given message
        tkinter.messagebox.showinfo("Info", message)  # Using Tkinter messagebox for feedback

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")
        self.theme_button.configure(
            text="Light Mode" if ctk.get_appearance_mode() == "Dark" else "Dark Mode"
        )
        self.update_colors()          #Re apply the whole colour scheme

    #Apply the exact colour scheme 
    def update_colors(self):
        mode = ctk.get_appearance_mode()

        # Choose colors based on mode
        if mode == "Dark":
            win_bg      = DARK_BG
            editor_bg   = DARK_TEXT_BG
            seg_fg      = win_bg
            seg_unselected = win_bg
            seg_selected   = DARK_TAB_BG
            seg_unselected_hover = win_bg
            seg_selected_hover   = DARK_TAB_BG
        else:
            win_bg      = LIGHT_BG
            editor_bg   = LIGHT_TEXT_BG
            seg_fg      = win_bg
            seg_unselected = LIGHT_SEG_UNSELECTED
            seg_selected   = LIGHT_SEG_SELECTED
            seg_unselected_hover = LIGHT_SEG_UNSELECTED_HOVER
            seg_selected_hover   = LIGHT_SEG_SELECTED_HOVER

        # Main window
        self.configure(fg_color=win_bg)

        # Button frame
        self.button_frame.configure(fg_color=win_bg)

        # Notebook (tabview) 
        self.notebook.configure(
            fg_color=win_bg,
            segmented_button_fg_color=seg_fg,
            segmented_button_selected_color=seg_selected,
            segmented_button_unselected_color=seg_unselected,
            segmented_button_selected_hover_color=seg_selected_hover,
            segmented_button_unselected_hover_color=seg_unselected_hover,
        )

        # Every text editor in every tab
        for tab_name in self.notebook._tab_dict.keys():
            frame = self.notebook.tab(tab_name)
            if frame.winfo_children():
                txt = frame.winfo_children()[0]
                if isinstance(txt, ctk.CTkTextbox):
                    txt.configure(fg_color=editor_bg)

    #Sync text from widgets to note objects
    def sync_notes(self):
        # Get all tab names using the internal _tab_dict
        tab_names = list(self.notebook._tab_dict.keys())
        # Loop through all tab names
        for tab_name in tab_names:
            # Get the frame for the tab
            frame = self.notebook.tab(tab_name)
            if frame.winfo_children():  # Check if the frame has children
                # Get the text widget
                text_widget = frame.winfo_children()[0]
                if isinstance(text_widget, ctk.CTkTextbox):  # Check if its a CTkTextbox
                    # Get the current text from the widget (excluding trailing newline)
                    text = text_widget.get('1.0', 'end-1c')
                    # Extract note ID from tab name
                    try:
                        note_id = int(tab_name.split()[1])
                        if note_id in self.notes:  # If the note exists in the dictionary
                            # Update the notes text
                            self.notes[note_id].update_text(text)
                    except Exception as e:
                        # Print error if syncing fails
                        print(f"Error syncing note {note_id}: {e}")

    #Renumber remaining notes sequentially
    def renumber_notes(self):       
        # Get the current tab names and sort them by their ID
        tab_names = sorted(list(self.notebook._tab_dict.keys()), key=lambda x: int(x.split()[1]))
        # Create a new dictionary for renumbered notes
        new_notes = {}
        # Loop through sorted tab names with new sequential IDs starting from 1
        for new_id, old_name in enumerate(tab_names, 1):
            try:
                # Extract old ID
                old_id = int(old_name.split()[1])
                # Get the note object
                note = self.notes[old_id]
                # Update the notes ID to the new one
                note.note_id = new_id
                # Create new tab name
                new_name = f"Note {new_id}"
                # Only rename if the new name is different from the old name to avoid errors
                if new_name != old_name:
                    self.notebook.rename(old_name, new_name)
                # Add to new dictionary
                new_notes[new_id] = note
            except Exception as e:
                # Print error if renumbering fails
                print(f"Error renumbering note: {e}")
        # Replace the old notes dictionary with the new one
        self.notes = new_notes
        # Update current_id to the next available ID
        self.current_id = len(new_notes) + 1

    def on_close(self):
        # Call save_notes to persist data before closing
        self.save_notes()  # Save persistent data
        # Destroy the window
        self.destroy()

    #Save notes to file for persistence
    def save_notes(self):
        # Sync latest text changes to note objects
        self.sync_notes()  # Ensure latest text is in notes
        # Create a dictionary to hold data for saving
        data = {}
        # Loop through notes and add ID-text pairs to data
        for note_id, note in self.notes.items():  # Loop over dictionary items
            data[note_id] = note.text
        try:
            # Open the file in write mode
            with open('notes.json', 'w') as f:
                # Dump the data as JSON
                json.dump(data, f)  # Using json for key-value persistence
        except Exception as e:  # Try/except for error handling
            # Print error if saving fails
            print(f"Error saving notes: {e}")

    #Load notes from file for persistence
    def load_notes(self):
        try:
            # Open the file in read mode
            with open('notes.json', 'r') as f:
                # Load JSON data
                data = json.load(f)
                # Loop through loaded data and create Note objects
                for note_id, text in data.items():  # Loop over loaded data
                    self.notes[int(note_id)] = Note(int(note_id), text)
        except FileNotFoundError:
            # If file doesn't exist, start with empty notes
            self.notes = {}  # If file not found, start empty
        except Exception as e:
            # Print error and start with empty notes if loading fails
            print(f"Error loading notes: {e}")
            self.notes = {}

# Main block to run the application if the script is executed directly
if __name__ == "__main__":
    # Create an instance of NoteApp
    app = NoteApp()
    # Start the CustomTkinter main event loop
    app.mainloop()