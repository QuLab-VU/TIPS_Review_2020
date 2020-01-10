#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 14:47:50 2019

@author: meyerct6
"""
from PyPDF2 import PdfFileReader,PdfFileWriter
import os


act_pdf_file = '41540_2018_69_MOESM2_ESM.pdf'

def pdf_splitter(index, src_file):
    with open(src_file, 'rb') as act_mls:
        reader = PdfFileReader(act_mls)
        writer = PdfFileWriter()
        writer.addPage(reader.getPage(index))
        out_file = os.path.join('page_'+str(index)+'.pdf')
        with open(out_file, 'wb') as out_pdf: writer.write(out_pdf)

for x in range(300): pdf_splitter(x, act_pdf_file)

for x in range(300):
    with open("commands.txt","a") as f:
        f.write("python pdf_convert_orc.py " + str(x) + "\n")