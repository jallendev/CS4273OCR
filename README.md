# OCR Capstone Project
## Setup
In theory, run WindowsSetup.bat to get everything set up for Windows <br>
For Linux or Mac, WindowsSetup.bat contains a list of all dependencies that are needed to be installed. <br>
This program has only been successfully run on Linux. This is due to a depenency with pdf2images not working on Windows

## To Run
Call `python3 extractText.py` <br>
Once the GUI is up, select the template file, the output csv file (which will be overwritten) and the PDF file(s) to be scanned in and select run. <br>

## Template File
The template file is | seperated fields where <br>
The first field is the column header <br>
After that there are three options: <br>
1. There are no other fields if nothing is to be inserted for a specific column <br>
2. There can be a second field with random text if the column is to always be filled with the same text <br>
3. There are four additional fields that specifies the bounding box where the code will extract text from the PDFs: <br>
    - The first additional field is the top left x coordinate of the bounding box 
    - The second additional field is the top left y coordinate of the bounding box
    - The third additional field is the bottom right x coordinate of the bounding box
    - The fourth additional field is the bottom right y coordinate of the bounding box

## Future Work
Needs to be able to run on Windows (possibly by changing the pdf2image library to a different library?) <br>
Needs to be able to create a template with a GUI <br>
Needs to be able to detect and correct for skewing in the PDFs
