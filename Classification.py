import numpy as np
import re
from itertools import compress
from collections import Counter
from sklearn import preprocessing
from TextPreprocessing import *
from utils_ import *

class ClassificationPreprocessing:
    
    def __init__(self):
        
        self.tp=TextPreprocessing()
        self.encoder = preprocessing.MultiLabelBinarizer()
        self.word_classes_indexes={}

    
    def fit_from_text(self,ref_file):
        sentences=[]
        cl=[]
        origin=[]
        with open(ref_file, 'r', encoding="utf-8") as f:
                next(f)
                for line in f:
                    line_=line.split(';')
                    if line_[1]=='T':
                        c=line_[7]
                        c=re.sub(r'[\+\.\-†*!\s]','',c)
                        cl.append(c)


        self.encoder.fit(cl)
        self.n_classes=len(self.encoder.classes_)
        self.class_to_index= dict(zip(self.encoder.classes_, range(self.n_classes)))
     
    
    def fit(self,y):
        
        self.encoder.fit(y)
        self.n_classes=len(self.encoder.classes_)
        self.class_to_index= dict(zip(self.encoder.classes_, range(self.n_classes)))
        
    
    def fit_word_indexes(self,index,c_index,class_to_exclude=[]):
        
        for c,s in zip(c_index,index):
            if c not in class_to_exclude:
                s=self.tp.tokenizer(s)

                for w in s:

                    if w not in self.word_classes_indexes:
                        self.word_classes_indexes[w]=set()


                    self.word_classes_indexes[w].update([self.class_to_index[c]])
        
        
        #np.save('word_codes_indexes',self.word_codes_indexes)
        print('Index word size =',len(self.class_to_index))

        

