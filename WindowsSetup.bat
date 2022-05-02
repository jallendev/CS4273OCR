@echo off


:start
cls

set python_ver=39

python ./get-pip.py

cd \
cd \python%python_ver%\Scripts\
pip install opencv-python
pip install pytesseract
pip install pdf2image
pip install numpy
pip install pillow

pause
exit