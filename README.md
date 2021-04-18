# Machine Learning - Chemical Toxicity Prediction Program
Language - Python  
Libraries - Numpy, pandas, sklearn, xgboost, lightgbm, imblearn

# Instructions to run the program

We have provided two options to run the chemical toxicity prediction program.

**Option 1:**
Run the complete script, that performs the feature selection using several models. This script may take a few hours to execute as our feature selection approach is quite exhaustive.

**Option 2:**
Run another script, that will use the results of feature selection(performed already and stored in a file). Since the feature selection process will not happen again, this script will be able to execute in a reasonable time.


**Follow these steps for Option 1**
* Take the clone of this repository or download as zip.
* Open the project on Jupyter Lab or any other python notebook/software. Go to the folder ‘Complete_Script_With_Feature_Selection’ and execute the script 'chemicaltoxicityprediction_falcons.py'
* Follow the same directory structure as the python script expects the dataset files in the parent directory 'Dataset' and the result will be stored in the 'Output' directory.
* The following dataset files will be required for execution: ‘test.csv’, ‘train.csv’ and ‘feamat.csv’.
* You can also open the notebook directly in Google Colab to view the results. Open the file 'ChemicalToxicityPrediction_FALCONS.ipynb' available in the ‘Complete_Script_With_Feature_Selection’ folder  
OR  
Open the Colab notebook through this link: [Colab Notebook1 - FALCONS](https://colab.research.google.com/drive/16dc0clcTqyQ3BGIV-cckkeb_6nj7dz97?usp=sharing#scrollTo=mREn6hq5CCQ_) 


**Follow these steps for Option 2**

* Take the clone of this repository or download as zip.
* Open the project on Jupyter Lab or any other similar software. Go to the folder ‘Script_With_Direct_Feature_Selection’ and execute the script 'chemicaltoxicityprediction_directfeatureselection_falcons.py'
* Follow the same directory structure as the python script expects the dataset files in the parent directory 'Dataset' and the result will be stored in the 'Output' directory.
* The following dataset files will be required for execution: ‘test.csv’, ‘train.csv’, ‘feamat.csv’ and 'Feature_Selected_Dataset.csv'.
* You can also open the notebook directly in Google Colab to view the results. Open the file 'ChemicalToxicityPrediction_DirectFeatureSelection_FALCONS.ipynb' available in the ‘Script_With_Direct_Feature_Selection’ folder  
OR  
Open the notebook through this link: [Colab Notebook2 - FALCONS](https://colab.research.google.com/drive/18OTgMBCycL5iNjWgm5mlwCQ1AYFRyBAY?usp=sharing)
