from pdf import PDF
from PyQt5.QtWidgets import QApplication
import sys
import argparse
parser = argparse.ArgumentParser(description='PDF operation manager')
parser.add_argument('--s','--split',action='store_true',\
                    help='split a pdf of N pages into N individual pdfs')
parser.add_argument('--m', '--merge', action='store_true',\
                    help='Merge a set of pdfs into one')
parser.add_argument('--o', '--ocr', action='store_true',\
                    help='Performs ocr on a pdf and stores it as a text file')
                    
args = parser.parse_args()
app = QApplication(sys.argv)
pdf = PDF()
if args.s:
    pdf.pdfsplitter()
elif args.m:
    pdf.pdfmerger()
elif args.o:
    pdf.perform_ocr()
else:
    pass


    
