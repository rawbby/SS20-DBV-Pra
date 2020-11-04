@ECHO OFF
@SETLOCAL

CD %0\..\..

python -m pip install --upgrade pip
python -m venv --copies .venv
CALL .\.venv\Scripts\activate.bat

python -m pip install --upgrade pip
python -m pip install --upgrade -r .\dbvpra\requirements.txt
