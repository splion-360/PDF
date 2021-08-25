import spacy as sp
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest
from pdf import App

class Summarize(App):
    def __init__(self):
        super().__init__()
    
    def get_file_and_lines(self):
        path = App.openFileNameDialog(self)
        if path == None:
            print("Terminated")
            return None

        self.stop = list(STOP_WORDS)
        with open(path,'r') as file:
            try:
                lines = file.readlines()
            except:
                print("Invalid file format")
                return
            linelist = []
            for line in lines:
                linelist.append(line.strip('\n'))
            
        filelines = ''.join(linelist)
        
        return filelines
            
    def load_spacy_nlp(self,filelines):
        nlp = sp.load("en_core_web_sm")
        self.docx = nlp(filelines)
    
    def word_frequency_count(self):
        word_frequency = {}
        for word in self.docx:
            if word.text not in self.stop:
                if word.text not in word_frequency.keys():
                    word_frequency[word.text] =  1
                else:
                    word_frequency[word.text]+=1
                    
        max_frequency = max(word_frequency.values())
        for word in word_frequency.keys():
            word_frequency[word] = word_frequency[word]/max_frequency
            
        return word_frequency
    
    def sentence_score_computer(self,word_frequency):
    
        sentence_scores = {} 
        sentence_list = [sentence for sentence in self.docx.sents]
        for sent in sentence_list:  
                for word in sent:
                    if word.text.lower() in word_frequency.keys():
                        if len(sent.text.split(' ')) < 30:
                            if sent not in sentence_scores.keys():
                                sentence_scores[sent] = word_frequency[word.text.lower()]
                            else:
                                sentence_scores[sent] += word_frequency[word.text.lower()]
        return sentence_scores
    
    
    def summariser(self,sentence_scores): 
        
        summarized_sentences = nlargest(5, sentence_scores, key=sentence_scores.get)
        final_sentences = [word.text for word in summarized_sentences ]
        summary = ' '.join(final_sentences)
        
        return summary