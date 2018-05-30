import string
import numpy as np
import re
from itertools import compress
from collections import Counter
from string import punctuation
from utils_ import *

### Functions for text preprocessing dedicated  with some particularities for ICD classification

class TextPreprocessing():

    def __init__(self):
        
        ##Prepare vectors of words from vocabulary

        self.characters = string.printable
        self.token_index = {}
        self.corrector_dict={}
        
        ###Stop word from specific file
        self.stop_word='dictionaries/stop_words.txt'
        for i,c in enumerate(self.characters[10:(31*2)]):
            self.token_index[c]=i
            self.stop_words=[]
            with open(self.stop_word, 'r', encoding="utf-8") as f:
                for line in f:
                    self.stop_words.append(line.replace('\n',''))
                    
    
        ###Acronyms to replace into texts
        self.acronyms_file='dictionaries/cim_abv'
        self.acronyms={}
        with open(self.acronyms_file, 'r', encoding="utf-8") as f:
            for line in f:
                line_=line.split(';')
                self.acronyms[line_[0]]=line_[1].replace('\n','')
        
        ##composed words
        self.comp_words=[]
        self.rev_comp_words={}
    
   
    
    def simple_tokenizer(self,s,pc=punctuation):
        
        s=re.sub(r"d'|l'",'',s.lower())
        
        pattern = r"[{}]".format(pc+'\s')
        
        words=[w for w in re.split(pattern,s)
                    if   w not in self.stop_words
                    and  not re.search(r'\d',w)
                    and len(w)>0]

        return words
    
    def tokenizer(self,s,pc=punctuation):
        
        for abv_,repl_ in self.acronyms.items():
            regex=re.compile(r'\b'+abv_+r'\b')
            s=re.sub(regex,repl_,s.lower())
        
        s=re.sub(r"d'|l'|n'",'',s.lower())
        
        words=self.simple_tokenizer(s,pc)
        
        #replace composed words by their single word decompostion
        for w in words:
            if w in self.comp_words:
                words.remove(w)
                words=words+re.split('-',self.rev_comp_words[w])
       
       
        return words
    
    
    #fit build vocabularies
    def fit_corrector(self,corrector_dict):
        
        self.corrector_dict=corrector_dict
        self.ref_vec_of_charc=[self.character_count_vector(cw) for cw in self.corrector_dict]
        self.freq_w=Counter(self.corrector_dict)
        
        
    ###word automatic correction
    
    ##Preselection is made by computing a Distance between 2 vector
    ## made of a character count of each word

    #From a non word respond a vector of selected word which have distance less n
    #with non word, distance measured by the character count vectors of word from dictionnary
    

    def best_correction(self,word,n=4):
        candidates=self.close_character_distance_words(word,n)
        nb_cand=len(candidates)
        if nb_cand==0:
            return word
        elif nb_cand==1:
            return candidates[0]
        else:
            l=[[self.levenshtein_distance(word,c),(1/(self.freq_w[c]+.01)),c] for c in candidates]
            l.sort()
            return l[0][2]
        
    
    ###One hot style encoding method to get a preselection of words
    ###which will be passed to home made Levenshtein Distance

    ##Prepare a vector of characters that will be used by next function
    ## 1 x 1 vector where all character as an index
    ## will be use to build word vectors

    def character_count_vector(self,w):
        i=0
        w_vec=np.zeros(len(self.characters[10:(31*2)]))
        for char in w:
                index =  self.token_index.get(char)
                if index is not None:
                    w_vec[index]+=1
        if i==0:
            l_w_vec=np.array([w_vec])
        else:
            l_w_vec=np.append(l_w_vec,[w_vec],axis=0)
        i+=1
        return l_w_vec
    
    
    ###Selection of close words
    def close_character_distance_words(self,non_word,n=4,vocab=None):
        
        if vocab==None:
            vocab=self.corrector_dict
            
        candidates_vec=self.ref_vec_of_charc-self.character_count_vector(non_word)
        candidates=list(compress(vocab, np.sum(abs(candidates_vec),-1)<n))
        return candidates

    ###word distance
    def levenshtein_distance(self,s1,s2):
        mat=np.zeros([len(s1)+1,len(s2)+1])
        for i in range(len(s1)+1):
            mat[i, 0] = i
        for j in range(len(s2)+1):
            mat[0, j] = j
        for i in range(1,len(s1)+1):
            for j in range(1,len(s2)+1):
                #print(str(i)+'-'+str(j))
                if s1[i-1]==s2[j-1]:
                    mat[i,j]=min(mat[i-1,j]+1,mat[i,j-1]+1,mat[i-1,j-1])
                else:
                    mat[i,j]=min(mat[i-1,j]+1,mat[i,j-1]+1,mat[i-1,j-1]+1)
        return(mat[i,j])

    ####Dealing with writting habits in ICD classification
    #### - synomyns are in square brajket
    #### - precisions are in parenthesis
    ####Functions to explode text in barkets and build new entries in the thesaurus 
    
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




