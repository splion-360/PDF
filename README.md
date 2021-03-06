# PDF
### __A repository for performing simple PDF operations__
This package makes use of dialogboxes created using 
[Qt Widgets](https://pythonspot.com/pyqt5-file-dialog/) of **PyQt5** package

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
## **Setup**:
#### **Basic Setup**:

  * Clone this repository into your local machine
  * Install the required packages using the code `pip install -r requirements.txt` from the command line
  
#### **spaCy Setup**:
* _spaCy_ is an open-source software library for advanced natural language processing, written in the programming languages Python and Cython.
  For the spacy setup, you can follow the webguide provided in the official site of [spaCy](https://spacy.io/usage)
* The scope of the package for this repository is to summarise the contents of a text file


  * Activate the python command line and type the following commands subsequently,\
    `pip install -U pip setuptools wheel`\
    `pip install -U spacy`\
    `python -m spacy download en_core_web_sm`


## **Usage**:
  * Open the command line and navigate to the cloned repository and run  `python main.py -h` to know about the usage of the helper functions 
  * Follow the steps given in the script to achieve required tasks

  
>*Note*:
>> Python versions may vary. Please run `python --version` before running the [main](./main.py) script. Also, the `perform_ocr` function is compatible only with Linux           >> Operating Systems due to the `Poppler` package issues. This will be rectified later 

  
