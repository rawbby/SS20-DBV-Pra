@ECHO OFF
@SETLOCAL

CD %0\..\..

CALL .\.venv\scripts\activate.bat
python -m dbvpra.gui
