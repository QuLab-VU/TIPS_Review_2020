#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 12:49:32 2019

@author: meyerct6
"""

# Import libraries 
from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import numpy as np

PDF_file = 'page_'+str(sys.argv[1]) + '.pdf'
threshold = 200
''' 
Part #1 : Converting PDF to images 
'''	  
# Store all the pages of the PDF in a variable 
page = convert_from_path(PDF_file, 600)[0] 
# Counter to store images of each page of PDF to image 
image_counter = 1	  
# Iterate through all the pages stored above 
# Declaring filename for each page of PDF as JPG 
filename = "page_"+str(sys.argv[1])+".jpg"
page = page.convert('L')
data = np.asarray(page, dtype="int16" )
data[data<threshold]=0
data[data>=threshold]=255
page = Image.fromarray( np.asarray( np.clip(data,0,255), dtype="uint8"), "L" )
# Save the image of the page in system 
page.save(filename, 'JPEG') 	  
# Increment the counter to update filename 
image_counter = image_counter + 1 
''' 
Part #2 - Recognizing text from the images using OCR 
'''
# Variable to get count of total number of pages 
filelimit = image_counter-1 
# Creating a text file to write the output 
outfile = "out_text_"+str(sys.argv[1])+".txt"
# Open the file in append mode so that  
# All contents of all images are added to the same file 
f = open(outfile, "a") 
# Recognize the text as string in image using pytesserct 
text = str(((pytesseract.image_to_string(Image.open(filename))))) 
# Finally, write the processed text to the file. 
f.write(text) 
# Close the file after writing all the text. 
f.close() 



		
