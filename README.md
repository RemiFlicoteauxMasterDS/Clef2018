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

This repository was used for preprocessing and to enrich learning training set.

### Death certificate text prepocesing
After tokenisation, only words from the dictionary were selected for learning. The rejected words have been proposed to an automatic spelling corrector (with the wording of the dictionary as the repository).

### Classification
Two classifiers were used. The main objective was to use machine learning algorithm, but due to week representation in the ICD original classification, we used a complementary classifier based on word recognition.

Finaly we use :
- Neural net with 1 embedding layer and three 1D convolution layers with various kernel size
- Rule base classifier based on an index word/ICD code

Data for dictionaries and classification task to be download from the cited organisations.
