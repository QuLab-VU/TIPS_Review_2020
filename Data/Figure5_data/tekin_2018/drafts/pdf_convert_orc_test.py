#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 12:49:32 2019

@author: meyerct6
"""

# Import libraries 
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os 
import glob
import numpy as np 

fils = glob.glob('sub.pdf')

threshold = 130
for e,PDF_file in enumerate(fils):
	''' 
	Part #1 : Converting PDF to images 
	'''
	  
	# Store all the pages of the PDF in a variable 
	pages = convert_from_path(PDF_file,600) 
	  
	# Counter to store images of each page of PDF to image 
	image_counter = 1
	  
	# Iterate through all the pages stored above 
	for page in pages:
	        filename = "page_"+str(image_counter)+".jpg"
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
	outfile = "out_text_"+str(e)+".txt"
		  
	# Open the file in append mode so that  
	# All contents of all images are added to the same file 
	f = open(outfile, "a") 
	
	images = glob.glob("page_*.jpg")
	for i in images:
		with open("images.txt","a") as f:
			f.write(i+'\n')
	
	text = str(((pytesseract.image_to_string("images.txt"))))
	f.write(text)
	# Close the file after writing all the text. 
	f.close() 
	os.remove("images.txt")



		
