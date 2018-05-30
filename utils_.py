import numpy as np
import re

def build_vocabulary(tokenized_sequences,START_VOCAB=[]):

    rev_vocabulary= START_VOCAB
    unique_tokens = set()
    
    for tokens in tokenized_sequences:
        unique_tokens.update(tokens)
    
    rev_vocabulary += sorted(unique_tokens)
    vocabulary = {}
        
    for i, token in enumerate(rev_vocabulary):
        vocabulary[token] = i
    
    
    return vocabulary, rev_vocabulary
    
    
def vectorize_corpus(tokenize_sent,max_length,vocab={}):

    n_sentences=len(tokenize_sent)

    vect_corpus = np.zeros(shape=(n_sentences, max_length), dtype=np.int32)
    numbered_tokens = zip(range(n_sentences), tokenize_sent)

    for i,tokens in numbered_tokens:
        
        if len(tokens)==0:
            vect_corpus[i,:]=0
        
        else:
            default=0
            token_ids = [vocab.get(t, default) for t in tokens]
            token_ids = token_ids[:max_length]
            vect_corpus[i, -len(token_ids):] = token_ids

    
    return vect_corpus