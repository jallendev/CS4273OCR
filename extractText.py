import cv2
import os
import pytesseract
from pdf2image import convert_from_path
import sys
import numpy as np
from io import BytesIO
from PIL import Image

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

    if verbose:
        cv2.imshow( 'im',cropped)
        cv2.waitKey(5000)

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
    
    maxEntries = 1      #Presumably the file has at least 1 entry

    #Loops through each of the given files
    for f in files:
        i = 0
        while i < maxEntries:       #While Loop for multiple entries
            line = ''
            header = '' #Its really only needed to do this once but I'm lazy
        
            #Opens the pdf and converts the first page to an image, only done on the first pass
            if i == 0:
                page = convert_from_path(f)
                f=BytesIO()
                page[3].save(f,format="png")
                f.seek(0)
                image = Image.open(f)
        
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
                    currEntries = s.count('\n') + 1     #Each newline implies the existence of an additional entry within a bounding box
                    
                    if currEntries > maxEntries:        #The current bounding box has more entries than the previous maximum
                        maxEntries = currEntries

                    if currEntries > 1:                 #Does this bounding box has more than one entry
                        splitS = s.split('\n')
                        s = splitS[i]       #Chooses the current entry to print
                    print(s)
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
    
if __name__ == '__main__':
    del sys.argv[0]
    print(extractImages(sys.argv, verbose = True))
