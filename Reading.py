import io
import os
import csv
from timeit import default_timer
from tkinter.ttk import Separator

from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'vision-344918-7fec18e902f4.json'

    
client = vision.ImageAnnotatorClient()

FILE_NAME = 'center.jpg'
FOLDER_PATH = r'C:\Users\ezeki\OneDrive\Desktop\Google Vision\Vision\Images'

with io.open(os.path.join(FOLDER_PATH, FILE_NAME), 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.text_detection(image=image)
annotations = response.text_annotations

arr = []
arr1 = []

# Keys to find information in extracted array
keys = ["NPI:", "PLAN:", "CLIENT/ID", "SUBCLIENT", "PRODUCT"]
# 2D Array to store information
results = [["NPI"], ["PLAN"], ["CLIENT/ID"], ["SUBCLIENT"], ["PRODUCT"]]

ann = ''.join(annotations[0].description)

# Adds annotaion descriptions while skipping 0 (OLD METHOD)
for x in range(1, len(annotations)):
    arr.append(annotations[x].description)

# Looks for keywords and their associated values (OLD METHOD)
for x in range (0, len(arr)):
    for y in keys:
        if y in arr[x]:
            # NPI: CASE
            if y == "NPI:":
                results[0].append(arr[x + 1])

            # PLAN: CASE
            elif y == "PLAN:":
                i = 1
                while(arr[x+i] != '\n'):
                    if(':' in arr[x+i]):
                        break
                    results[1].append(arr[x + i])
                    i += 1

            # CLIENT/ID CASE
            elif y == "CLIENT/ID":
                results[2].append(arr[x+1])


# Creates an array of strings, each containing a line of data
temp = []
for x in range(0, len(ann)):
    if(ann[x] != '\n'):
        temp.append(ann[x])
    
    elif(ann[x] == '\n'):
        str1 = ''.join(temp)
        arr1.append(str1)
        del str1
        temp.clear()

# Opens new text and erases its previous contents
f = open('C:/Users/ezeki/OneDrive/Desktop/Google Vision/Vision/Output/output.txt', 'w')
f.truncate(0)

# Writes each line of data
for x in arr1:
    f.write(x + '\n')

f.close

# Writes to CSV.
f1 = open('C:/Users/ezeki/OneDrive/Desktop/Google Vision/Vision/Output/output.csv', 'a')
f1.truncate(0)
# writer = csv.writer(f1, delimiter = ',', lineterminator=' ')
writer = csv.writer(f1, lineterminator = '\n')
writer.writerow(arr1)
f1.close