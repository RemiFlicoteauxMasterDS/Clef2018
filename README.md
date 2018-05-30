# CLEF e-Health 2018 Task 1 
## Multilingual Information Extraction - ICD10 coding

The goal of the task is to automatically assign ICD10 codes to the text content of death certificates.

Task Description :  [CLEF 2018 eHealth 2018](https://sites.google.com/view/clef-ehealth-2018/task-1-multilingual-information-extraction-icd10-coding?authuser=0)

## Summary the Work

### Dictionary


A dictionary was produced by concatenating different ICD 10 thesauri available:
- ICD 10 classification (https://www.bfs.admin.ch/bfs/fr/home/statistiques/sante/nomenclatures/medkk/instruments-codage-medical.assetdetail.1180187.html)
- ICD 10 index (Vol 2) (https://www.bfs.admin.ch/bfs/fr/home/statistiques/sante/nomenclatures/medkk/instruments-codage-medical.assetdetail.1180186.html)
- Snomed CT French version (http://esante.gouv.fr/services/referentiels/referentiels-d-interoperabilite/snomed-35vf)
- Orphanet (http://www.orphadata.org/cgi-bin/inc/ordo_orphanet.inc.php/)
- CépiDC dictionnaries (https://sites.google.com/view/clef-ehealth-2018/task-1-multilingual-information-extraction-icd10-coding?authuser=0)

This knowledge base was used for preprocessing and to enrich learning training set.

[Notebook](https://github.com/RemiFlicoteauxMasterDS/Clef2018/blob/master/Dictionaries.ipynb)

### Death certificate text prepocesing
After tokenisation, only words from the dictionary were selected for learning. The rejected words have been proposed to an automatic spelling corrector (with the wording of the dictionary as the repository).

[Notebook](https://github.com/RemiFlicoteauxMasterDS/Clef2018/blob/master/Preprocessing%20clef%20texts.ipynb)

### Classification
Two classifiers were used. The main objective was to use machine learning algorithm, but due to week representation in the ICD original classification, we used a complementary classifier based on word recognition.

Finaly we use :
- Neural net with 1 embedding layer and three 1D convolution layers with various kernel size
- Rule base classifier based on an index word/ICD code, the gain was neverless very small on final results.

[Notebook](https://github.com/RemiFlicoteauxMasterDS/Clef2018/blob/master/Clef%202018%20-%20Conv1D%20network%20and%20word%20recognition.ipynb)

Data for dictionaries and classification task to be download from the cited organisations.

Références
- Suominen, Hanna and Kelly, Liadh and Goeuriot, Lorraine and Kanoulas, Evangelos and Azzopardi, Leif and Spijker, Rene and Li, Dan and Névéol, Aurélie and Ramadier, Lionel and Robert, Aude and Palotti, Joao and Jimmy and Zuccon, Guido. Overview of the CLEF eHealth Evaluation Lab 2018. CLEF 2018 - 8th Conference and Labs of the Evaluation Forum, Lecture Notes in Computer Science (LNCS), Springer, September 2018.
- Pierre Zweigenbaum and Thomas Lavergne, Hybrid methods for ICD-10 coding of death certificates,  CLEF eHealth 2017
- Mohamed Dermouche, Vincent Looten, Rémi Flicoteaux, Sylvie Chevret, Julien Velcin and Namik Taright, ICD10 Code Extraction from Death Certificates, CLEF eHealth 2016
- Yoon Kim, Convolutional Neural Networks for Sentence Classification, EMNLP 2014.
