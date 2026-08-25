pip install pymupdf
pip install pyinstaller
pyinstaller --onefile --windowed --clean --exclude-module matplotlib --exclude-module numpy --exclude-module pandas pdf2up.py
pause