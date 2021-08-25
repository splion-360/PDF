from pdf import PDF
from PyQt5.QtWidgets import QApplication
import sys
import argparse
from summariser import Summarize
from colorama import Fore
import os
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(description='PDF operation manager',formatter_class=RawTextHelpFormatter)
parser.add_argument('--s','--split',action='store_true',\
                    help='split a pdf of N pages into N individual pdfs')
parser.add_argument('--m', '--merge', action='store_true',\
                    help='Merge a set of pdfs into one')
parser.add_argument('--o', '--ocr', action='store_true',\
                    help='Performs ocr on a pdf and stores it as a docx file')
parser.add_argument('--su','--summarize',action='store_true',\
                    help='Summarizes a given textfile')
parser.add_argument('--sa','--sumsave',action='store_true',\
                    help='Saves the summary as textfile (Optional). Use it along with --su. \nExample: python3 main.py --su --sa')         
args = parser.parse_args()
app = QApplication(sys.argv)
pdf = PDF()
if args.s:
    pdf.pdfsplitter()
elif args.m:
    pdf.pdfmerger()
elif args.o:
    pdf.perform_ocr()
elif args.su:
    summ = Summarize()
    filelines =  summ.get_file_and_lines()
    if filelines != None:
        summ.load_spacy_nlp(filelines)
        word_frequency = summ.word_frequency_count()
        sentence_scores = summ.sentence_score_computer(word_frequency)
        summary = summ.summariser(sentence_scores)
        fn = filelines.split(' ')
        sn = summary.split(' ')
        print()
        print(Fore.GREEN,f"Word count before summary: {len(fn)}")
        print()
        print(Fore.MAGENTA,"Summary:")
        print(Fore.YELLOW,f"{summary}")
        print()
        print(Fore.GREEN,f"Word count after summary: {len(sn)}")
        print()

        if args.sa:
            file = pdf.saveFileDialog()
            base = os.path.basename(file) + '.txt'
            path = os.path.join(os.path.dirname(file),base)
            with open(path,'w+') as file:
                file.write(summary)
                print(f'File written at {file}')

else:
    pass


    
