# SS20-DBV-Pra

This Project was created in the course "[Praktikum Digitale Bildverarbeitung](https://www.vsa.informatik.uni-siegen.de/en/praktikum-digitale-bildverarbeitung)" by Robert Andreas Fritsch in summer 2020.\
The course was led by [Prof. Dr. Michael M&ouml;ller](https://www.vsa.informatik.uni-siegen.de/en/moeller-michael).

## LICENSE

See [LICENSE](./LICENSE)

## Requirements

- Python3
- Pip3

### Python Requirements

see [requirements.txt](./dbvpra/requirements.txt)

Notice that numpy 1.19.4 currently (Nov. 2020) fails to pass a sanity check due to a bug in the windows runtime.\
see [bug](https://developercommunity.visualstudio.com/content/problem/1207405/fmod-after-an-update-to-windows-2004-is-causing-a.html)

Therefor numpy == 1.19.3 is used explicitly.\
Later numpy >= 1.19.4 should be used again.

### Boost pytorch

If you want pytorch to use cuda choose [requirements_no_cuda.txt](./dbvpra/requirements_no_cuda.txt) over [requirements.txt](./dbvpra/requirements.txt)\
and install pytorch as described [here](https://pytorch.org/get-started/locally/#start-locally).

## Build and Run (windows)

Setup virtual environment
```bat
python -m venv --copies .venv
CALL .\.venv\Scripts\activate.bat

python -m pip install --upgrade pip
python -m pip install --upgrade -r .\dbvpra\requirements.txt
```

Generate ui script
```bat
CALL pyside2-uic .\dbvpra\gui\window.ui > .\dbvpra\gui\Ui_window.py
```

Run the gui
```bat
python -m dbvpra.gui
```

Notice: You can also ```CALL ".\scripts\*.bat"```!

## Authors

- Robert Andreas Fritsch [info@robert-fritsch.de](mailto:info@robert-fritsch.de)
