@ECHO OFF
@SETLOCAL

CD %0\..\..

CALL .\.venv\scripts\activate.bat
CALL pyside2-uic .\dbvpra\gui\window.ui > .\dbvpra\gui\Ui_window.py
