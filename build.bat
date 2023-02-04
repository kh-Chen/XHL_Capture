.\venv\Scripts\pyinstaller.exe -F -w main.py
xcopy .\vlc-3.0.16\ .\dist\XHL_Capture\vlc-3.0.16\ /s/y/q
copy config.ini .\dist\XHL_Capture\config.ini
copy crypt.jar .\dist\XHL_Capture\crypt.jar
copy .\dist\main.exe .\dist\XHL_Capture\main.exe