import cv2
import os
import pytesseract
from pdf2image import convert_from_path
import sys
import numpy as np
from io import BytesIO
from PIL import Image
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import re

config = r'--psm 4'

#assumes corners are topLeft.x, topleft.y, bottomright.x, bottomright.y
def extractText(image, corners, verbose = False):
    im = np.array(image)
    #print(im.shape)
    #print(corners)

    #Crops and smooths the images
    cropped = im[int(corners[1]):int(corners[3]), int(corners[0]):int(corners[2])]
    cropped = cv2.blur(cropped, (3,2))
    cropped =  cv2.bilateralFilter(cropped,3,200,10)
        
    # Simple image to string
    text = pytesseract.image_to_string(cropped, config=config)
    text = text.strip()
    
    #Removes leading and training non alpha numeric characters. Think this solves more problems than it creates
    text = re.sub(r"^\W+", '', text)
    text = re.sub(r"\W+$", '', text)

    if verbose:
        cv2.imshow( 'im',cropped)
        cv2.waitKey(1500)

    return text
    
#args[1] = template file
#args[2] = output file name
#The remaining args are the pdf files to be parsed    
def extractImages(args, verbose=False):
    out = '' #used to hold the full output

    #Extracts args
    template = args[0]
    outFile = open(args[1], "w") #overwrites the old file
    files= args[2:]
    
    #Saves the lines from the template
    templateLines = open(template, 'r').readlines()
    
    header = ''
    


    #Loops through each of the given files
    for f in files:
        
        page = convert_from_path(f)
        for p in page:
            f=BytesIO()
            p.save(f,format="png")
            f.seek(0)
            image = Image.open(f)
            
            maxEntries = 1      #Presumably the file has at least 1 entry
            i = 0
            while i < maxEntries:       #While Loop for multiple entries
                line = ''
                header = '' #Its really only needed to do this once but I'm lazy                 
                    
                print(pytesseract.image_to_osd(image))
            
                #loops through each of the lines in the template
                for tl in templateLines:
                    params = tl.strip().split('|') #Breaks the line into each component
                    header += params[0]+','
                    print(params)
                    
                    #If there isn't anything to write to the output file just prints a ","
                    if len(params) == 1:
                        line += ','
                
                    #This just saves the parameters if not given a bounding box. Might be a bad idea to include commas in this
                    elif len(params) == 2:
                        line += params[1] + ','
                    
                    #This actually extracts the text from the pdf to put in the csv
                    elif len(params) == 5:
                        s = extractText(image, params[1:],verbose)
                        
                        #If there are two \ns in a row, removes one. Assumes that this should never happen
                        previous = ''
                        c = 0
                        while c < len(s):
                            if s[c] == previous and s[c] == '\n':
                                s = s[:c] + s[c+1:]
                                c-=1
                            if c >= 0:
                                previous = s[c]
                            c+=1
                            
                        currEntries = s.count('\n') + 1    #Each newline implies the existence of an additional entry within a bounding box
                        
                        if currEntries > maxEntries:        #The current bounding box has more entries than the previous maximum
                            maxEntries = currEntries

                        if currEntries > 1:                 #Does this bounding box has more than one entry
                            splitS = s.split('\n')
                            if len(splitS) > i: 
                                s = splitS[i]       #Chooses the current entry to print
                        print(currEntries, '\n', s)
                        line+=s+','           
                
                    else:
                        print('Should not have gotten here')                                 
                i += 1
                #Adds the line minus the last , to the output file
                out += line[:-1] + '\n'

    #Writes out the text
    header = header[:-1] + '\n'
    outFile.write(header)
    outFile.write(out)
    outFile.close()
    
    return out

def drawImage():
    #set up
    window = tk.Tk()
    window.title("OCR")
    window.geometry('500x500')
    verbose = tk.IntVar()

    #fuctions
    def getTemplate():
        filetypes = (('text files', '*.txt'),('All files', '*.*'))
        templateFileName = fd.askopenfilenames(title='Open PDF images to scan', initialdir='./', filetypes = filetypes)
        templateTxtBox.delete(0, 'end')
        templateTxtBox.insert('end', templateFileName)

    def getOutput():
        filetypes = (('text files', '*.csv *.txt'),('All files', '*.*'))
        outputFileName = fd.askopenfilenames(title='Open PDF images to scan', initialdir='./', filetypes = filetypes)
        oPTxtBox.delete(0, 'end')
        oPTxtBox.insert('end', outputFileName)
        
    def getPDF():
        filetypes = (('text files', '*.pdf'),('All files', '*.*'))
        pdfFileNames = fd.askopenfilenames(title='Open PDF images to scan', initialdir='./', filetypes = filetypes)
        pdfTxtBox.delete(0, 'end')
        pdfTxtBox.insert('end', pdfFileNames)

    def runOCR():
        args = [templateTxtBox.get(), oPTxtBox.get(), pdfTxtBox.get()]
        outputText = extractImages(args, verbose = verbose.get())
        OCRReturnBox.delete('1.0', 'end')
        OCRReturnBox.insert('end', outputText)

    OCRReturnBox = tk.Text(window, height=20, width=60)

    #stylign the scene
    templateTxtBox = tk.Entry(window,width=50)
    oPTxtBox = tk.Entry(window,width=50)
    pdfTxtBox = tk.Entry(window,width=50)
    templateButton = tk.Button(window, text="Select Template", command=getTemplate)
    outputButton = tk.Button(window, text="Enter Output name", command=getOutput)
    pdfButton = tk.Button(window, text="Select Files to OCR", command=getPDF)
    runButton = tk.Button(window, text="Run OCR", command=runOCR)
    verbosity = tk.Checkbutton(window, text='Show Images',variable=verbose, onvalue=1, offvalue=0)
    verbosity.grid(column = 1, row = 3)
    templateTxtBox.grid(column=1, row=0)
    oPTxtBox.grid(column=1, row=1)
    pdfTxtBox.grid(column=1, row=2)
    templateButton.grid(column=2, row=0)
    outputButton.grid(column=2, row=1)
    pdfButton.grid(column=2, row=2)
    runButton.grid(column=2, row=3)
    OCRReturnBox.grid(column=1, row=4, columnspan =3)

    #keep window open and draws screen
    window.mainloop()
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        del sys.argv[0]
        print(extractImages(sys.argv, verbose = True))
    else:
        drawImage()
