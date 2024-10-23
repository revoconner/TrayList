import customtkinter as ctk
import json
import os
from trayicon import TrayIcon  # Import the TrayIcon class from tray_icon.py
import pyglet
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1) #Set DPI awareness

DATA_FILE = "todo_list.json" #save data in this file

# Set the color theme for customtkinter
ctk.set_appearance_mode("Dark")  # Can be "System", "Dark", or "Light"
ctk.set_default_color_theme("blue")

pyglet.options['win32_gdi_font'] = True #Support for pyglet to use older GDI plus font

pyglet.font.add_file('Monoton-Regular.ttf') #Add Font file
myfont=('Monoton')

class TaskEntry(ctk.CTkFrame):
    def __init__(self, parent, text="", delete_callback=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.delete_callback = delete_callback
        self.text_var = ctk.StringVar(value=text)

        self.configure(fg_color="#111111")  

        # Text entry field with the same height as the button and a border color
        self.text_entry = ctk.CTkEntry(
            self,
            textvariable=self.text_var,
            height=45,  # Same height as the button
            border_width=2,
            border_color="#47204D",
            fg_color="#0B0B0B"   # Border color for the entry
        )
        self.text_entry.pack(
            side=ctk.LEFT, fill=ctk.X, expand=True, padx=5, pady=5 # Increased padding
        )

        # Delete button 
        self.delete_button = ctk.CTkButton(
            self,
            text="X",
            text_color="#A53232",
            command=self.delete_task,
            width=35,
            height=45,  # Set height to match the text entry
            fg_color="#111111",  # Custom background color for the button
            hover_color="#D14242",  # A lighter shade on hover for visual feedback
            corner_radius=5,
            border_width=1,
            border_color="#A53232"
        )
        self.delete_button.pack(
            side=ctk.RIGHT, padx=5, pady=5  # Increased padding
        )

        # Bind events
        self.text_entry.bind("<Return>", self.handle_return)
        self.text_entry.bind("<KeyRelease>", self.handle_key_release)
        self.text_var.trace("w", self.update_delete_button)

    def handle_return(self, event=None):
        """Handle Return key press - create new entry if there's text"""
        if self.text_var.get():
            self.master.add_empty_task()
            self.master.save_tasks()  # Also save when creating new entry

    def handle_key_release(self, event=None):
        """Handle any key release - save the current state"""
        # Don't trigger save on Return key as it's handled separately
        if event.keysym != 'Return':
            self.master.save_tasks()

    def delete_task(self):
        if self.delete_callback:
            self.delete_callback(self)
            self.master.save_tasks()  # Save after deletion

    def update_delete_button(self, *args):
        if self.text_var.get():
            self.delete_button.configure(state=ctk.NORMAL)
        else:
            self.delete_button.configure(state=ctk.DISABLED)

class ToDoList(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Tray List")
        self.geometry("500x600")

        # Create a label to display at the top left
        self.title_label = ctk.CTkLabel(
            self,
            text="Tray     List",
            font=(myfont, 36),
            text_color="#73327D" # Font and size
        )
        self.title_label.pack(
            anchor=ctk.W, padx=5, pady=5  # Align with the text entry
        )
        
        self.tasks = []
        self.load_tasks()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Set the frame's background color to blue
        self.configure(fg_color="#111111") 
        
    def add_empty_task(self):
        new_task = TaskEntry(self, delete_callback=self.delete_task)
        new_task.pack(
            fill=ctk.X, padx=5, pady=5  # Increased padding between tasks
        )
        self.tasks.append(new_task)

    def delete_task(self, task):
        if task in self.tasks:
            task.pack_forget()
            self.tasks.remove(task)

    def save_tasks(self):
        tasks_data = [task.text_var.get() for task in self.tasks if task.text_var.get()]
        with open(DATA_FILE, "w") as f:
            json.dump(tasks_data, f)

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                tasks_data = json.load(f)
            for text in tasks_data:
                new_task = TaskEntry(
                    self, text=text, delete_callback=self.delete_task
                )
                new_task.pack(
                    fill=ctk.X, padx=5, pady=5  # Increased padding
                )
                self.tasks.append(new_task)

        self.add_empty_task()  # Add one empty task for new input

    def on_closing(self):
        self.save_tasks()  # Save the current tasks before closing
        self.withdraw()  # Hide to tray

# Initialize the ToDoList application
root = ToDoList()

# Initialize the system tray icon
tray_icon = TrayIcon(root, "image.png")

# Hide the app at startup
root.withdraw()  # Hide the window completely

# Define a function to hide to tray instead of closing completely
def on_closing():
    root.save_tasks()
    root.withdraw()  # Hide the window to minimize to tray

# Set the closing protocol to hide to the tray
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the customtkinter event loop
root.mainloop()