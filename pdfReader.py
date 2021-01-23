from PyPDF2 import PdfFileWriter, PdfFileReader
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
import pandas as pd
import os,sys
import xlrd
import math
import xlwt
import re
import numpy as np
from dateutil.parser import parse
import operator
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import (
               DictionaryObject,
               NumberObject,
               FloatObject,
               NameObject,
               TextStringObject,
               ArrayObject
               )

class Document:
    
    def __init__(self,fileName,fPath):

        """
        Documents class constructer deceleration
        """
        
        self.fileName = fileName
        self.fPath = fPath
        self.fType = 0   
        self.content = []
        self.coordcont = []
       
    def readFile(self):
        """
        This Function check the file type and call the
        called the function according to matched file type
        """
        if self.fType ==1:
            self.readPdf()


    def readPdf(self):
        file1 = os.path.join(self.fPath,self.fileName)
        fp = open(file1,'rb')
        parser = PDFParser(fp)
        document = PDFDocument(parser)
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
        rsrcmgr = PDFResourceManager()
        device = PDFDevice(rsrcmgr)
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        lt = []
        lt1 = []

        def parse_obj(lt_objs,pageNo):

            for obj in lt_objs:
                try:
                    if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                       lt.append(obj.get_text().replace('\n', ''))
                       lt1.append([obj.get_text().replace('\n', '').strip(),int(obj.bbox[0]),int(obj.bbox[1]),int(obj.bbox[3]),pageNo+1])
                       #print(pageNo + 1,int(obj.bbox[2]),int(obj.bbox[3]),obj.get_text().replace('\n', '').strip())

                except:
                    pass


        for pageNumber,page in enumerate(PDFPage.get_pages(fp)):
            try:

                interpreter.process_page(page)
                layout = device.get_result()
                parse_obj(layout._objs,pageNumber)

            except:
                pass
                
        self.coordcont = lt1
        self.content = lt
        return self.content
        

    def findFileType(self):

        ff = self.fileName.split('.')
        ff[1] = ff[1].lower()
        if ff[1] == 'pdf':            
            self.fType = 1

        

                    
            
if __name__ == '__main__':
    
    inpPdfDir = r'path to dir with pdf files'
   
    for folder, subfolder, filenames in os.walk(inpPdfDir):
        for f in filenames :
            
            print(f,"---------------")
            oDoc = Document(f,folder)
            oDoc.findFileType()
            oDoc.readFile()

            if oDoc.fType == 1:
                print("yahooo")
                
                
            
        
    
    
    
