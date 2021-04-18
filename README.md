# Instructions to run the program

We are providing two options to run the chemical toxicity prediction program.

**Option 1:**
Run the complete script, that performs the feature selection using several models. This script may take a few hours to execute as our feature selection approach is quite exhaustive.

**Option 2:**
Run another script, that will use the results of feature selection(performed already and stored in a file). Since the feature selection process will not happen again, this script will be able to execute in a reasonable time.


**Follow these steps for Option 1**
* Download the python script from the Google Colab Notebook (ChemicalToxicityPrediction_FALCONS.ipynb)                  
[Colab Notebook1 - FALCONS](https://colab.research.google.com/drive/16dc0clcTqyQ3BGIV-cckkeb_6nj7dz97?usp=sharing#scrollTo=mREn6hq5CCQ_)  
OR  
Take the python script from the folder ‘Complete_Script_With_Feature_Selection’.  
Script: chemicaltoxicityprediction_falcons.py

* Open this script on Jupyter Lab or any other software you are using.

* Import the dataset files ‘test.csv’, ‘train.csv’ and ‘feamat.csv’ which are available in the 'Dataset' folder.

* Run the program.


**Follow these steps for Option 2**

* Download the python script from the Google Colab Notebook (ChemicalToxicityPrediction_DirectFeatureSelection_FALCONS.ipynb) 
[Colab Notebook2 - FALCONS](https://colab.research.google.com/drive/18OTgMBCycL5iNjWgm5mlwCQ1AYFRyBAY?usp=sharing)  
OR  
Take the python script from the folder ‘Script_With_Direct_Feature_Selection’.  
Script: chemicaltoxicityprediction_directfeatureselection_falcons.py

* Open this script on Jupyter Lab or any other software you are using.

* Import the dataset files ‘test.csv’, ‘train.csv’, ‘feamat.csv’ and ‘Feature_Selected_Dataset.csv’ which are available in the 'Dataset' folder.

* Run the program.
