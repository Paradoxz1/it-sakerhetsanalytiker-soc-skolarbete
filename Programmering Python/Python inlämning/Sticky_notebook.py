import tkinter as tk  # Import the main Tkinter module for GUI creation
from tkinter import ttk  # Import themed Tkinter widgets for a modern look, like Notebook
import tkinter.messagebox  # Import messagebox for displaying pop-up messages to the user
import json  # Import JSON module for saving and loading data persistently in a file

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

# Define the main application class that inherits from tk.Tk to create the GUI window
class NoteApp(tk.Tk):
    def __init__(self):
        # Call the parent class constructor to initialize the Tkinter window
        super().__init__()
        # Set the window title
        self.title("Sticky Notes")
        # Set the initial window size
        self.geometry("400x300")

        # Dictionary to store Note objects, with note_id as key and Note instance as value
        self.notes = {}  # Dictionary to store Note objects, key: note_id, value: Note object
        # Load any existing notes from the persistent file
        self.load_notes()  # Load persistent data

        # Create a frame to hold the buttons at the top of the window
        button_frame = tk.Frame(self)  # Button frame on top
        button_frame.pack(fill='x')  # Pack the frame to fill horizontally

        # Add buttons for adding, removing, and clearing notes, linking them to their respective methods
        tk.Button(button_frame, text="Add Note", command=self.add_note).pack(side='left', padx=5)
        tk.Button(button_frame, text="Remove Note", command=self.remove_note).pack(side='left', padx=5)
        tk.Button(button_frame, text="Clear Note", command=self.clear_note).pack(side='left', padx=5)

        # Create a Notebook widget to handle multiple tabs (each tab is a note)
        self.notebook = ttk.Notebook(self)
        # Pack the notebook to expand and fill the available space
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
        # Add a new tab to the notebook for this note
        self.add_tab(note_id)
        # Select the newly added tab to switch to it immediately
        self.notebook.select(self.notebook.tabs()[-1])  # Switch to the new note
        # Increment the current ID for the next note
        self.current_id += 1
        # Display a message confirming the addition with the specific note ID
        self.display_message(f"Note {note_id} added successfully.")  # User feedback with specific note

    #Function to remove the currently selected note.
    def remove_note(self):
        # Get the currently selected tab
        current_tab = self.notebook.select()
        if current_tab:  # If-statement to check if a tab is selected
            # Get the text of the current tab (e.g., "Note 1")
            note_text = self.notebook.tab(current_tab, "text")
            try:
                # Extract the note ID from the tab text
                note_id = int(note_text.split()[1])  # Extract note_id
                # Remove the tab from the notebook
                self.notebook.forget(current_tab)
                # Delete the note from the dictionary
                del self.notes[note_id]  # Remove from dictionary
                # Sync any changes in text to the note objects
                self.sync_notes()  # Sync remaining notes
                # Renumber the remaining notes to fill any gaps in IDs
                self.renumber_notes()
                # Display a message confirming removal with the specific note ID
                self.display_message(f"Note {note_id} removed successfully.")  # User feedback with specific note
            except ValueError:
                # Display an error message if extraction fails
                self.display_message("Error removing note.")  # Error feedback
        else:
            # Display a message if no note is selected
            self.display_message("No note selected to remove.")

    #Function to clear the current notes text
    def clear_note(self):
        # Get the currently selected tab
        current_tab = self.notebook.select()
        if current_tab:  # If-statement for condition
            # Get the frame widget for the current tab
            frame = self.notebook.nametowidget(current_tab)
            # Get the text widget from the frames children
            text_widget = frame.winfo_children()[0] if frame.winfo_children() else None
            if isinstance(text_widget, tk.Text):  # Using isinstance to check if its a Text widget
                # Delete all text from the widget
                text_widget.delete('1.0', 'end')
                # Get the tab text
                note_text = self.notebook.tab(current_tab, "text")
                try:
                    # Extract the note ID
                    note_id = int(note_text.split()[1])
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
        # Create a frame for the new tab
        frame = tk.Frame(self.notebook)
        # Create a Text widget inside the frame for note content
        text_widget = tk.Text(frame, wrap='word')  # wrap='word' to wrap at word boundaries
        # Insert the initial text into the widget
        text_widget.insert('end', text)
        # Pack the text widget to fill the frame
        text_widget.pack(expand=True, fill='both')
        # Add the frame as a new tab to the notebook with the appropriate title
        self.notebook.add(frame, text=f"Note {note_id}")

    #Function to display feedback to the user
    def display_message(self, message):
        # Show an info message box with the given message
        tk.messagebox.showinfo("Info", message)  # Using Tkinter for feedback

    #Sync text from widgets to note objects
    def sync_notes(self):
        # Loop through all tabs in the notebook
        for tab in self.notebook.tabs():
            # Get the frame for the tab
            frame = self.notebook.nametowidget(tab)
            if frame.winfo_children():  # Check if the frame has children
                # Get the text widget
                text_widget = frame.winfo_children()[0]
                if isinstance(text_widget, tk.Text):  # Check if its a Text widget
                    # Get the current text from the widget (excluding trailing newline)
                    text = text_widget.get('1.0', 'end-1c')
                    # Get the tab text
                    note_text = self.notebook.tab(tab, "text")
                    try:
                        # Extract note ID
                        note_id = int(note_text.split()[1])
                        if note_id in self.notes:  # If the note exists in the dictionary
                            # Update the notes text
                            self.notes[note_id].update_text(text)
                    except Exception as e:
                        # Print error if syncing fails
                        print(f"Error syncing note {note_id}: {e}")

    #Renumber remaining notes sequentially
    def renumber_notes(self):
        # Get the list of remaining tabs
        remaining_tabs = self.notebook.tabs()
        # Create a new dictionary for renumbered notes
        new_notes = {}
        # Loop through tabs with new sequential IDs starting from 1
        for new_id, tab in enumerate(remaining_tabs, 1):
            # Get the current tab text
            note_text = self.notebook.tab(tab, "text")
            try:
                # Extract old ID
                old_id = int(note_text.split()[1])
                # Get the note object
                note = self.notes[old_id]
                # Update the notes ID to the new one
                note.note_id = new_id
                # Add to new dictionary
                new_notes[new_id] = note
                # Update the tab title with the new ID
                self.notebook.tab(tab, text=f"Note {new_id}")
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
    # Start the Tkinter main event loop
    app.mainloop()