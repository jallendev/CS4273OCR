# OCR Capstone Project
## Setup
In theory, run WindowsSetup.bat to get everything set up for Windows <br>
For Linux or Mac, WindowsSetup.bat contains a list of all dependencies that are needed to be installed.

## To Run
Call `python3 extractText.py templateFileName.txt outputFileName.csv pdf1.pdf pdf2.pdf ...` <br>
Where the user can give an arbitrary (greater than 0) number of PDFs for the program to parse

## Template File
The template file is | seperated fields where <br>
The first field is the column header <br>
After that there are three options: <br>
* 1st: There are no other fields if nothing is to be inserted for a specific column <br>
* 2nd: There can be a second field with random text if the column is to always be filled with the same text <br>
* 3rd: There are four additional fields that specifies the bounding box where the code will extract text from the PDFs: <br>
- The first additional field is the top left x coordinate of the bounding box 
- The second additional field is the top left y coordinate of the bounding box
- The third additional field is the bottom right x coordinate of the bounding box
- The fourth additional field is the bottom right y coordinate of the bounding box
