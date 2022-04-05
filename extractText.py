import cv2
import os
import pytesseract
from pdf2image import convert_from_path
import sys
import numpy as np
from io import BytesIO
from PIL import Image

#config = r'--psm 7'

#assumes corners are topLeft.x, topleft.y, bottomright.x, bottomright.y
def extractText(image, corners, verbose = False):
    im = np.array(image)
    print(im.shape)
    print(corners)

    cropped = im[int(corners[1]):int(corners[3]), int(corners[0]):int(corners[2])]
    cropped = cv2.blur(cropped, (3,2))
    #cropped = cv2.medianBlur(cropped, 3)
    cropped =  cv2.bilateralFilter(cropped,3,200,10)
    
    if verbose:
        cv2.imshow( 'im',cropped)
        
    # Simple image to string
    text = pytesseract.image_to_string(cropped)#, config=config)
    text = text.strip()

    if verbose:
        print(text)
        cv2.waitKey(5000)

    return text
    
#args[1] = template file
#args[2] = output file name
#The remaining args are the pdf files to be parsed    
def extractImages(args, verbose=False):
    out = ''
    
    template = args[0]
    outFile = open(args[1], "a")
    files= args[2:]
    
    #Saves the lines from the template
    templateLines = open(template, 'r').readlines()
    
    #Loops through each of the given files
    for f in files:
        line = ''
        
        #Opens the pdf and converts the first page to an image
        page = convert_from_path(f)
        f=BytesIO()
        page[0].save(f,format="png")
        f.seek(0)
        image = Image.open(f)
        
        #loops through each of the lines in the template
        for tl in templateLines:
            params = tl.strip().split() #Breaks the line into each component
            
            #If there isn't anything to write to the output file just prints a ,
            if len(params) == 1:
                line += ','
            
            #This just saves the parameters if not given a bounding box
            elif not params[1].isnumeric() or len(params) != 5:
                line += params[1]
                for p in params[2:]:
                    line+= ' ' + p 
                line += ','
                
            #This actually extracts the text from the pdf to put in the csv
            else:
                s = extractText(image, params[1:],verbose)
                print(s)
                line+=s+','                                            
        
        #Adds the line minus the last , to the output file
        out += line[:-1] + '\n'

    outFile.write(out)
    outFile.close()
    return out
    
if __name__ == '__main__':
    #extractText('images/bestCase.png', [0, 0], [850,201], verbose=True)
    #extractText('images/bestCase.png', [0,0], [196,57], verbose=True)
    del sys.argv[0]
    print(extractImages(sys.argv, True))
