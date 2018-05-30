import numpy as np
import pandas as pd
from sklearn.metrics import recall_score,precision_score,fbeta_score
class evaluation():

    def __init__(self):
        ##Prepare vectors of words from vocabulary
        self.cols=['Threshold',
                  'Mean of pred codes',
                  'Mean of true codes',
                  'Mean of true positives',
                  'Mean of false positives',
                  'Mean of false negatives',
                  'Precision',
                  'Recall',
                  'F1-Score',
                  'F2-Score'
                  ]
    
    
    def prepare_results(self):
        return pd.DataFrame(columns=self.cols)
    
    def get_metrics(self,true,pred,threshold=0.1):
        
        n_sample=true.shape[0]
        
        num_codes = np.mean(np.sum(np.apply_along_axis(lambda x: x==1,0,pred),axis=1))
        num_true_codes = np.mean(np.sum(np.apply_along_axis(lambda x: x==1,0,true),axis=1))
        
        rec=recall_score(true,pred,average='micro')
        pre=precision_score(true,pred,average='micro')
        f1=fbeta_score(true,pred,1,average='micro')
        f2=fbeta_score(true,pred,2,average='micro')
        
        pred=np.where(pred==0,-2,1)
        res=pred+true
        #true negatives : res = -2
        true_negatives = np.mean(np.sum(np.apply_along_axis(lambda x: x==-2,0,res),axis=1))
        #false_negatives : res = -1
        false_negatives = np.mean(np.sum(np.apply_along_axis(lambda x: x==-1,0,res),axis=1))
        #false_positives : res = 1
        false_positives = np.mean(np.sum(np.apply_along_axis(lambda x: x==1,0,res),axis=1))
        # true_positives : res=2
        true_positives = np.mean(np.sum(np.apply_along_axis(lambda x: x==2,0,res),axis=1))
        

        #result tab
        result={'Threshold' : threshold,
                'Mean of pred codes':round(num_codes,1),
                'Mean of true codes':round(num_true_codes,1),
                'Mean of true positives':round(np.mean(true_positives)),
                'Mean of false positives':round(np.mean(false_positives),1),
                'Mean of false negatives':round(np.mean(false_negatives),1),
                'Precision' :round( pre*100,1),
                'Recall' : round(rec*100,1),
                'F1-Score':round(f1*100,1),
                'F2-Score':round(f2*100,1)
                }  
        return result

            
    def GetMetricsFromHotEncoder(self,ytrue,ypred,threshold=0.1):
        
        pred=self.GetPredFromThreshold(ypred,threshold)
        pred=pred.astype(int)
        
        return self.get_metrics(ytrue,pred,threshold)
    
    
    def GetPredFromThreshold(self,ypred,threshold=0.15):
        
        return np.where(ypred>threshold,1,0)