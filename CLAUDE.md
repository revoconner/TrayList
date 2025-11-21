# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TrayList is a simple system tray to-do list application with two implementations:
- **Python version** (primary): Built with customtkinter, pystray, and tkinter
- **C++ version** (in Cpp/ directory): Built with wxWidgets (less complete)

The Python version is the main implementation. Users write tasks and they auto-save to `todo_list.json`. The app minimizes to the system tray on close.

## Development Commands

### Python Version

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run the application:**
```bash
python todo.py
```

**Build executable:**
```bash
build.bat
```
This runs PyInstaller with the `traylist.spec` configuration. The built application appears in `dist\TrayList\TrayList.exe`.

### C++ Version

The C++ implementation in the `Cpp/` directory uses wxWidgets. See `Cpp/cmake.txt` for build instructions.

## Code Architecture

### Python Implementation

**Main files:**
- `todo.py` - Main application entry point and UI logic
- `trayicon.py` - System tray icon management using pystray
- `todo_list.json` - Data persistence (auto-generated at runtime)

**Key classes:**

1. **ToDoList (todo.py)** - Main application class extending `ctk.CTk`
   - Manages the task list window
   - Handles JSON persistence via `save_tasks()` and `load_tasks()`
   - Uses `on_closing()` to hide to tray instead of exiting
   - Dark theme with custom colors (#111111 background, #73327D purple accent)

2. **TaskEntry (todo.py)** - Individual task widget extending `ctk.CTkFrame`
   - Contains a text entry field and delete button
   - Auto-saves on key release (except Enter key)
   - Enter key creates a new empty task below
   - Delete button only enabled when text is present

3. **TrayIcon (trayicon.py)** - System tray integration
   - Runs in a separate daemon thread
   - Right-click menu: "Open" (default) and "Exit"
   - Uses `image.png` as the tray icon

**UI Styling:**
- Uses customtkinter in Dark mode
- Custom font: Monoton-Regular.ttf (pyglet font rendering)
- DPI awareness set via `windll.shcore.SetProcessDpiAwareness(1)`
- Color scheme: dark backgrounds with purple accents

**Data flow:**
- Tasks auto-save to JSON on every keystroke, task creation, and deletion
- App starts hidden in system tray
- Closing the window hides it to tray (doesn't exit)
- Must use tray menu "Exit" to fully quit

### C++ Implementation

Located in `Cpp/` directory with wxWidgets-based implementation:
- `todolist.cpp/hpp` - Main frame and task entry widgets
- `trayicon.cpp/hpp` - Tray icon management
- Similar architecture to Python version but less complete

## Required Assets

- `image.png` - System tray icon (bundled in PyInstaller build)
- `icon.ico` - Application icon for Windows
- `Monoton-Regular.ttf` - Custom font for title (bundled in PyInstaller build)

## PyInstaller Configuration

The `traylist.spec` file includes:
- Data files: font and image bundled into build
- Hidden imports for PIL, customtkinter, pystray, pyglet
- Directory-based build (not single-file)
- Console disabled for GUI-only app
- Duplicate removal function for cleaner builds
