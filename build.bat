@echo off
echo Cleaning old builds...
rmdir /s /q build
rmdir /s /q dist
echo Installing Requirements...
pip install -r requirements.txt
echo Building application...
pyinstaller traylist.spec
echo Build complete!
echo.
echo The application folder is located in: dist\TrayList
echo You can run the application by executing TrayList.exe in that folder
pause