from PyPDF2 import PdfFileWriter, PdfFileReader , PdfFileMerger
from PyQt5.QtWidgets import QWidget, QFileDialog
import os
import pytesseract as pt
import pdf2image as pi
from PIL import Image
from tqdm import tqdm
from docx2pdf import convert
import warnings
from colorama import Fore
warnings.filterwarnings("ignore")

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height) 

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open", "","All Files (*);; Text (*.txt);; PDF (*.pdf)", options=options)
        if fileName:
            return fileName
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"Open", "","All Files (*);; Text (*.txt);; PDF (*.pdf)", options=options)
        if files:
            return files
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save as","","All Files (*);; Text (*.txt);; PDF (*.pdf)", options=options)
        if fileName:
            return fileName
    

class PDF(App):
    def __init__(self):
        super().__init__()
    
    def pdfmerger(self):
        merger = PdfFileMerger()
        pdflist = App.openFileNamesDialog(self)
        if pdflist == None:
            print(Fore.YELLOW,"Terminated")
            return

        for pdf in pdflist:
            merger.append(pdf)
            
        outputname = App.saveFileDialog(self)
        
        merger.write(outputname)
        print(Fore.GREEN,'DONE !!!')
        print()
        print(Fore.GREEN,f"Merged and saved at {outputname}")
        
        merger.close()
        
    def pdfsplitter(self):
        filepath = App.openFileNameDialog(self)

        if filepath == None:
            print(Fore.YELLOW,"Terminated")
            return

        inputpdf = PdfFileReader(open(filepath, "rb"))
        path = App.saveFileDialog(self)
        base = os.path.dirname(path)
        
        for i in range(inputpdf.numPages):
            c = i+1
            output = PdfFileWriter()
            output.addPage(inputpdf.getPage(i))
            with open(f"{os.path.join(base,os.path.basename(path))}%s.pdf" % c, "wb") as outputStream:
                output.write(outputStream)
        print(Fore.GREEN,'DONE !!!')
        print()
        print(Fore.GREEN,f"Split and saved at {os.path.dirname(filepath)}")

    def perform_ocr(self):
        image_counter = 1
        path = App.openFileNameDialog(self)
        if path == None:
            print(Fore.YELLOW,"Terminated")
            return 
        pages = pi.convert_from_path(path,dpi=500)

        for page in tqdm(pages,desc = 'Converting to images: Please Wait!!!'):
            filename = "page_"+str(image_counter)+".jpg"
            page.save(filename,'JPEG')
            image_counter+=1
        print(Fore.GREEN,'DONE !!!')
        filelimit = image_counter-1

        path = App.saveFileDialog(self)
        file = os.path.basename(path)+'.txt'
        outfile = os.path.join(os.path.dirname(path),file)
        f = open(outfile, "a")
        
        for i in tqdm(range(1, filelimit + 1),desc='Performing OCR: Please Wait!!!'):
            filename = "page_"+str(i)+".jpg"     
            text = str(((pt.image_to_string(Image.open(filename)))))
            text = text.replace("-\n", '')    
            f.write(text)

            if os.path.exists(filename):
                os.remove(filename)    
        print(Fore.GREEN,'DONE !!!')
        print()
        f.close()
        print(Fore.GREEN,f"OCR performed and saved at {os.path.dirname(outfile)}")


    def doctopdf(self):
        doclist = App.openFileNamesDialog(self)

        if doclist == None:
            print(Fore.YELLOW,"Terminated")
            return
        savedir = App.saveFileDialog(self)
        pathname = os.path.dirname(savedir)
        i = 0
        for doc in tqdm(doclist):
            outname = os.path.basename(doc)[:-4] + 'pdf'
            finalpath = os.path.join(pathname,outname)
            try:
                convert(doc,finalpath)
            except OSError:
                print(Fore.RED,'Only mac and windows')
                break
            i+=1
        if i == len(doclist):
            print(Fore.GREEN,'DONE !!!')
        else:
            print(Fore.RED,'Could not convert!!!')



    def rotatepdf(self,degreetorotate,flag='CW'):
        pdf = App.openFileNameDialog(self)
        if pdf == None:
            print(Fore.YELLOW,"Terminated")
            return
        rotate_reader = PdfFileReader(open(pdf, 'rb'))
        rotate_writer = PdfFileWriter()
        savedir = App.saveFileDialog(self)
        pathname = os.path.dirname(savedir)

        for pagenum in tqdm(range(rotate_reader.numPages)):
            page = rotate_reader.getPage(pagenum)
            if flag=='CW':
                page.rotateClockwise(degreetorotate)
            else:
                page.rotateCounterClockwise(degreetorotate)
            rotate_writer.addPage(page)

        outname = os.path.basename(pdf)[:-4]+'_rotated.pdf'
        with open(os.path.join(pathname,outname),'wb') as file:
            rotate_writer.write(file)
        print(Fore.GREEN,'DONE !!!')





