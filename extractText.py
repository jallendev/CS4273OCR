import cv2
import os
import pytesseract
import configparser

#config = r'--psm 7'

def extractText(imName, topLeftCorner, topRightCorner, verbose = False):
    im = cv2.imread(imName,0)
    cropped = im[topLeftCorner[1]:topRightCorner[1], topLeftCorner[0]:topRightCorner[0]]
    
    if verbose:
        cv2.imshow( 'im',cropped)
        
    # Simple image to string
    text = pytesseract.image_to_string(cropped)#, config=config)
    text = text.strip()

    if verbose:
        print(text)
        cv2.waitKey(5000)

    return text
    
def extractDir(dirName, configFile, verbose=False):
    strings = []
    
    config = configparser.ConfigParser()
    config.read(configFile)
    topLeftX = int(config['BOUNDING_BOXES']['topLeftX'])
    topLeftY = int(config['BOUNDING_BOXES']['topLeftY'])
    bottomRightX = int(config['BOUNDING_BOXES']['bottomRightX'])
    bottomRightY = int(config['BOUNDING_BOXES']['bottomRightY'])
    
    for f in os.listdir(dirName):
        imName = dirName + '/' + f
        s = extractText(imName, [topLeftX,topLeftY], [bottomRightX,bottomRightY], verbose=verbose)
        strings.append(s)
    return strings
    
if __name__ == '__main__':
    extractText('images/bestCase.png', [0, 0], [850,201], verbose=True)
    #extractText('images/bestCase.png', [0,0], [196,57], verbose=True)
    #print(extractDir('images', 'config.ini'))
