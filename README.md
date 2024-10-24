# Tray List
A simple list app that resides in your system tray icon. 

## Description
I made it so I can look over my daily tasks for work. It's not pretty and is very basic. It's written with Python 3.11 and tkinter.


<img width="377" alt="image" src="https://github.com/user-attachments/assets/c12ce1ef-77c1-4ced-af71-6286ac723779">


## How to use
- Just unzip somewhere and and run the **TrayList.exe** to open the app. 
- To start with windows, you can create a task scheduler event for the app, or create a shortcut of TrayList.exe and move that to the startup folder of windows. It is usually in **C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup**
- The app will now run in your tray, to open click on it.
- Whenever you type something in the list, it is saved instantly. To create new entries, press the Return/Enter key.
![image](https://github.com/user-attachments/assets/39dc70b9-e28f-481f-9b75-6b8294f73c24)



## C++ Version
A C++ version is in the works in a different branch called **C++**. It's a work in progress.

## How to build
1. Install python 3 and above.
2. Run the build.bat as administrator (admin permission is optional but preferred)


## Changelog
1. v1.0 Made app
2. v1.2 Redesign with Ctkinter
3. v1.3 Opens with left single click, instead having to right click and selecting open. Saves everything without having to press enter.
