import pystray
from PIL import Image
import threading

class TrayIcon:
    def __init__(self, root, image_path):
        self.root = root
        self.icon = None
        self.image_path = image_path
        self.create_tray_icon()

    def create_tray_icon(self):
        # Load the image from the specified path
        image = Image.open(self.image_path)

        # Create the tray icon with default action
        self.icon = pystray.Icon(
            name="todo_tray_icon",
            icon=image,
            title="My To-Do App",
            menu=pystray.Menu(
                pystray.MenuItem("Open", self.restore_window, default=True),  # Set as default action
                pystray.MenuItem("Exit", self.exit_app)
            )
        )

        self.start_tray_icon()

    def start_tray_icon(self):
        # Start the system tray icon in a separate thread
        threading.Thread(target=self.icon.run, daemon=True).start()

    def restore_window(self, icon=None, item=None):
        # Restore the main Tkinter window
        self.root.after(0, self.root.deiconify)
        self.root.after(0, self.root.lift)  # Bring window to front
        self.root.after(0, self.root.focus_force)  # Force focus

    def exit_app(self, icon, item):
        # Safely quit the Tkinter app
        self.root.after(0, self.root.quit)