---
marp: true
title: Group 10 Capstone Presentation
theme: gaia
---

# Project 6: OCR <!--- fit --->
<!-- _class: invert -->
# Members: Reza Torbati, Ethan Womack, Marissa Zuyus, Christian McBane, Isaac Spiers <!-- align="center"-->

---

# Problem Overview
- For our project, we were tasked with using OCR to solve the problem of converting data from a pdf to data that can be entered directly into a csv file
- Our overall goal was to use a picture of a form with information and extract the data in a way that could be easily transfered to an editable file 
- The forms vary and are not all formatted the same way, and therefore we needed a way to extract data from user specified locations that depend on the form type

---

# Our Solution
- Using OCR
- Picking a Library 
- Pytesseract

---

# Backend
Extracting the text from images is easy
```
    config = '--psm 4' # sets the config
    
    #Gets exact image and smooths the lines
    cropped = im[int(corners[1]):int(corners[3]), int(corners[0]):int(corners[2])]
    cropped = cv2.blur(cropped, (3,2))
    cropped =  cv2.bilateralFilter(cropped,3,200,10)
        
    # extracts the text from the image
    text = pytesseract.image_to_string(cropped, config=config)
    text = text.strip()
```
Other code just ensures the extracted text goes in the csv correctly

---

# FrontEnd/Demo
- GUI demonstration
 
    ![empty gui](https://i.imgur.com/L1zFts7.png)
    ![gui after selecting paths](https://i.imgur.com/usJsIbf.png)
    ![gui after getting results](https://i.imgur.com/RpZf2ax.png)
- CMD demonstration
 
    ![a comandline example of the program running](https://i.imgur.com/xLJJ73q.png)
---

# Future Work
- A lot of work remains
  - Ensure Multi-OS Compatability
  - python-poppler
- Improve Image Recognition
- GUI Improvements
  - Visuals / Intuitiveness
  - Save Templates
- Other Possible Formats for the Program?
  - iOS/Android Application
  - Web App
