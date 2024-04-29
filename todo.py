import tkinter as tk
import json
import os
from trayicon import TrayIcon  # Import the TrayIcon class from tray_icon.py

DATA_FILE = "todo_list.json"

class TaskEntry(tk.Frame):
    def __init__(self, parent, text="", delete_callback=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.delete_callback = delete_callback
        self.text_var = tk.StringVar(value=text)

        self.text_entry = tk.Entry(self, textvariable=self.text_var)
        self.text_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.delete_button = tk.Button(
            self, text="Delete", command=self.delete_task
        )
        self.delete_button.pack(side=tk.RIGHT)

        self.text_entry.bind("<Return>", self.save_entry)
        self.text_var.trace("w", self.update_delete_button)

    def save_entry(self, event=None):
        if self.text_var.get():
            self.master.add_empty_task()

    def delete_task(self):
        if self.delete_callback:
            self.delete_callback(self)

    def update_delete_button(self, *args):
        if self.text_var.get():
            self.delete_button.configure(state=tk.NORMAL)
        else:
            self.delete_button.configure(state=tk.DISABLED)


class ToDoList(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("To-Do List")
        self.geometry("300x400")

        self.tasks = []
        self.load_tasks()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_empty_task(self):
        new_task = TaskEntry(self, delete_callback=self.delete_task)
        new_task.pack(fill=tk.X, padx=3, pady=1)
        self.tasks.append(new_task)

    def delete_task(self, task):
        if task in self.tasks:
            task.pack_forget()
            self.tasks.remove(task)

    def save_tasks(self):
        # Get the current task text to save
        tasks_data = [task.text_var.get() for task in self.tasks if task.text_var.get()]
        with open(DATA_FILE, "w") as f:
            json.dump(tasks_data, f)

    def load_tasks(self):
        # Load tasks from the JSON file if it exists
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                tasks_data = json.load(f)
            for text in tasks_data:
                new_task = TaskEntry(self, text=text, delete_callback=self.delete_task)
                new_task.pack(fill=tk.X, padx=3, pady=1)
                self.tasks.append(new_task)

        self.add_empty_task()  # Add one empty task for new input

    def on_closing(self):
        self.save_tasks()  # Save the current tasks before closing
        self.destroy()


root = ToDoList()

# Initialize the system tray icon
tray_icon = TrayIcon(root, "image.png")

# Hide the app at startup
root.withdraw()  # Use withdraw() to completely hide the window

# Define a function to hide to tray instead of closing completely
def on_closing():
    root.save_tasks()
    root.withdraw()  # Hide the window to minimize to tray

# Set the closing protocol to hide to the tray
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
root.mainloop()
