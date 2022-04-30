---
marp: true
title: Group 10 Capstone Presentation
theme: gaia
---

# Title Slide
Title goes here

---

# Our Problem
OCR

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
pics go here

---

# Future Work
A lot(true)
