import numpy as np
import re
from itertools import compress
from collections import Counter
from sklearn import preprocessing
from utils_ import *
from TextPreprocessing import *
### Functions for text preprocessing dedicated  with some particularities for ICD classification

class FeatureExtractor():

    def __init__(self):
        
        self.token_index = {}
        self.dictionary={}
        self.text_preprocessing=TextPreprocessing()

        
        
    def fit(self,sentences,START_VOCAB=[]):
        
        tokenized_sent = [self.text_preprocessing.tokenizer(s) for s in sentences]
        self.dictionary, self.rev_dictionary = build_vocabulary(tokenized_sent,START_VOCAB)
                



    def barket_removal(self,s):

        all_=re.findall('\((.*?)\)',s)

        if len(all_)!=0:

            all_=[w for w in all_]+['']

            _s_=[]
            s_=re.split(r'\(.*?\)',s)
            if ' ' in s_:
                s_.remove(' ')

            for i,sp in enumerate(all_):
                s__=''

                for j,w in enumerate(s_):
                    if j==0:
                        s__=w+sp

                    else:
                        s__=s__+w

                s__=re.sub(r'\s{2,}',' ',s__)
                _s_.append(s__)

            return(_s_)
        else:
            return([s])
    
    def square_barket_removal(self,s):
        all_= re.findall('\[(.*?)\]',s)

        if len(all_)!=0:
            _s_=[]
            all_=[w for w in all_]

            for i,sp in enumerate(all_):


                s_=re.split(r'\[.*?\]',s)
                if ' ' in s_:
                    s_.remove(' ')
                del s_[-0]
                s___=sp+' '.join(s_)
                s___=re.sub(r'\s{2,}',' ',s___)
                _s_.append(s___)

                s_=re.split(r'\[.*?\]',s)
                if ' ' in s_ and len(s_)>2:
                    s_.remove(' ')

                s___=' '.join(s_)
                s___=re.sub(r'\s{2,}',' ',s___)
                _s_.append(s___)

                s___=s_[0]+sp+s_[1]
                s___=re.sub(r'\s{2,}',' ',s___)
                _s_.append(s___)
            return(_s_+all_)

        else:
            return [s]
    
    def features_from_tokens(self,tokenize_sent,max_length):
        
        return vectorize_corpus(tokenize_sent,max_length,self.dictionary)

        

