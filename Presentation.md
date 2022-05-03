---
marp: true
size: 16:9
theme: gaia
---

# OCR Machine Learning

<hr style="border: 3px solid gray">

- Team 4
- Wahid Haidari, Joseph Allen, Ezekiel House, Khalil Albattashi


--- 

# The Problem

<hr style="border: 3px solid gray">

- Process dental forms to gather data
- Input: Dental Insurance EOBs
- Output: Excel .csv file with needed data for analysis

![width:900px height:250px](./assets/original.jpg)

---

# The Approach

<hr style="border: 3px solid gray">

**Setup**
    - Enable Google Vision API
    - Use API to analyze documents
    - Output via python script to .csv
**Structure**
    - Team 4 focused on creation of test cases to train API
    - Other teams focused on other possible APIs and an interface for the application
    
---

# Test Cases

<hr style="border: 3px solid gray">

    OCR data
- Used actual scanned documents to make the test cases
- Used photoshop
- Added noise, made blur, changed the angles and brightness
- Combined different characterestics to make new test cases:
e.g. blur+noise, angle+brightness, noise+angles, etc.
- three documents, each 23 edits (3*23=69 test cases) 
---
# Test Cases

![width:350px](./assets/Document1/noise1-blur2.jpg)&nbsp;&nbsp;![width:350px](./assets/Document1/noise1-angle2.jpg)&nbsp;&nbsp;![width:350px](./assets/Document3/brightness2.jpg)

---

# Why Google Cloud Vision API

<hr style="border: 3px solid gray">

**Pros**
- More supported languages
- Better performance in real-world scenarios

**Cons**
- Overlaid text
- Cost

---

<center>
<span style="font-size:2em; font-weight:bold; margin: 0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);">Tech</span>
</center>