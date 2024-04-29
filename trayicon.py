import pystray
from PIL import Image
import threading

class TrayIcon:
    def __init__(self, root, image_path):
        self.root = root
        self.icon = None
        self.image_path = image_path  # Store the image path
        self.create_tray_icon()

    def create_tray_icon(self):
        # Load the image from the specified path
        image = Image.open(self.image_path)

        # Define menu actions
        menu = pystray.Menu(
            pystray.MenuItem("Open", self.restore_window),
            pystray.MenuItem("Exit", self.exit_app),
        )

        # Create the tray icon
        self.icon = pystray.Icon("todo_tray_icon", image, "My To-Do App", menu)
        self.start_tray_icon()

    def start_tray_icon(self):
        # Start the system tray icon in a separate thread
        threading.Thread(target=self.icon.run, daemon=True).start()

    def restore_window(self, icon, item):
        # Restore the main Tkinter window
        self.root.after(0, self.root.deiconify)

    def exit_app(self, icon, item):
        # Safely quit the Tkinter app
        self.root.after(0, self.root.quit)
