# -*- coding: utf-8 -*-
"""ChemicalToxicityPrediction_FALCONS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16dc0clcTqyQ3BGIV-cckkeb_6nj7dz97
"""

# Authors - Sahil Aneja, Rahul Ananda Bijai
# Team - FALCONS
# This python program is used to predict the toxicity outcome of a set of chemicals

# Importing all the required packages
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import xgboost
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split,KFold,cross_val_score
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report,f1_score
from sklearn.feature_selection import RFE,SelectFromModel,SelectKBest,chi2

# Loading Train Dataset
train_data = pd.read_csv("./Dataset/train.csv")

train_data.head(n=10)

# Loading Test Dataset
test_data = pd.read_csv("./Dataset/test.csv")

test_data.head(n=10)

# New train dataframe after splitting the 'Id' field
splitted_train_data = train_data["Id"].str.split(";", n = -1, expand = True) 
train_data["c_id"]= splitted_train_data[0] 
train_data["assay_id"]= splitted_train_data[1] 
train_data.head(n=10)

#  New test dataframe after splitting the 'Id' field 
splitted_test_data = test_data["x"].str.split(";", n = -1, expand = True)
test_data["c_id"]= splitted_test_data[0] 
test_data["assay_id"]= splitted_test_data[1] 
test_data.head(n=10)

# Loading Features Dataset
features_data = pd.read_csv("./Dataset/feamat.csv")
features_data.head(n=10)

# Merging Train Dataset with Feature Dataset on c_id and V1
new_train_data=pd.merge(train_data, features_data, left_on='c_id', right_on='V1', how='left', indicator=True)
new_train_data.head(n=10)
print(new_train_data)

# Merging Test Dataset with Feature Dataset on c_id and V1
new_test_data=pd.merge(test_data, features_data, left_on='c_id', right_on='V1', how='left', indicator=True)
new_test_data.head(n=10)
print(new_test_data)

# Deleting dataframes which are of no use now, to clean up some memory
del test_data 
del train_data
del features_data
del splitted_train_data
del splitted_test_data

# Check for columns having only one unique value in newly created train dataset and remove them.
nunique_train  = new_train_data.apply(pd.Series.nunique)
cols_to_drop_train = nunique_train[nunique_train == 1].index
new_train_data = new_train_data.drop(cols_to_drop_train, axis=1)
new_train_data.info()

# Check for columns having only one unique value in newly created test dataset and remove them.
nunique = new_test_data.apply(pd.Series.nunique)
cols_to_drop = nunique[nunique == 1].index
new_test_data = new_test_data.drop(cols_to_drop, axis=1)
new_test_data.info()

# Removing Id, c_id and V1 from the Train Dataset
new_train_data=new_train_data.drop(['Id','c_id','V1'], axis = 1) 
new_train_data.head()

# Removing x, c_id and V1 from the Test Dataset
new_test_data=new_test_data.drop(['x','c_id','V1'], axis = 1) 
new_test_data.head()

# Check for any columns having infinite values in Train Dataset
floatset=new_train_data.select_dtypes(exclude=['object'])
col_names=floatset.columns.to_series()[np.isinf(floatset).any()]
print(col_names)

# Finding the max value in column V15 for train dataset and replacing the infinte value by max value
column = new_train_data.loc[new_train_data['V15'] != np.inf, 'V15']
max_value = column.max()
print(max_value)
new_train_data['V15'].replace(np.inf,max_value,inplace=True)

# Check for any columns having infinite values in Test Dataset
floatset=new_test_data.select_dtypes(exclude=['object'])
col_names=floatset.columns.to_series()[np.isinf(floatset).any()]
print(col_names)

# Finding the max value in column V15 for test dataset and replacing the infinte values to max value
column = new_test_data.loc[new_test_data['V15'] != np.inf, 'V15']
max_value = column.max()
print(max_value)
new_test_data['V15'].replace(np.inf,max_value,inplace=True)

# Drop the columns from train set which are not available in test set except 'Expected'
train_columns = new_train_data.columns
test_columns = new_test_data.columns
remove_columns = train_columns.difference(test_columns)
print(remove_columns)
# Don't remove 'Expected' column
remove_columns = remove_columns.delete(0)
new_train_data = new_train_data.drop(columns=remove_columns)
new_train_data.info()

new_test_data.info()

# Data normalization with sklearn for Train Dataset. Ignoring 'Expected' from getting normalized
x = new_train_data.drop('Expected', axis = 1).values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
train = pd.DataFrame(x_scaled)
firstCol = new_train_data["Expected"]
train = train.join(firstCol)
train.head()

# Data normalization with sklearn for Test Dataset
y = new_test_data.values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
y_scaled = min_max_scaler.fit_transform(y)
test = pd.DataFrame(y_scaled)
test.head()

train_df_corr = train.drop(['Expected'], axis=1)

# Function for generating the correlation
def get_correlation(data, threshold):
    col_corr = set()
    corr_matrix =data.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j])> threshold:
                colname = corr_matrix.columns[i]
                col_corr.add(colname)
    return col_corr

# Getting Correlation of Train Dataset with a threshold of 0.7
corr_feature = get_correlation(train_df_corr, 0.7)
corr_feature

# Dropping columns/features based on correlation from Test and Train Datasets
X=train_df_corr.drop(corr_feature,axis=1)
test=test.drop(corr_feature,axis=1)

# Initializing y which would be used for Feature Selection Process

y = train["Expected"]

# Deleting dataframs which are of no use now, to clean up some memory
del new_train_data
del new_test_data
del train
del train_df_corr

# Feature Selection Process begins and initializing the number of features that each method should give
num_feats = 50

#Feature Selection using RFE and estimators as Decision Tree Classifier 
rfe_selector_DT = RFE(estimator=DecisionTreeClassifier(random_state= 0), n_features_to_select=num_feats, verbose=5)
rfe_selector_DT.fit(X, y)
rfe_support_DT = rfe_selector_DT.get_support()
rfe_feature_DT = X.loc[:,rfe_support_DT].columns.tolist()
print(str(len(rfe_feature_DT)), 'selected features')

#Feature Selection using RFE and estimators as Random Forest Classifier
rfe_selector_RF = RFE(estimator=RandomForestClassifier(n_jobs=-1, random_state= 0), n_features_to_select=num_feats, verbose=5)
rfe_selector_RF.fit(X, y)
rfe_support_RF = rfe_selector_RF.get_support()
rfe_feature_RF = X.loc[:,rfe_support_RF].columns.tolist()
print(str(len(rfe_feature_RF)), 'selected features')

#Feature Selection using RFE and estimators as XGB Classifier
rfe_selector_XGB = RFE(estimator=XGBClassifier(n_jobs=-1, random_state= 0), n_features_to_select=num_feats, verbose=5)
rfe_selector_XGB.fit(X, y)
rfe_support_XGB = rfe_selector_XGB.get_support()
rfe_feature_XGB = X.loc[:,rfe_support_XGB].columns.tolist()
print(str(len(rfe_feature_XGB)), 'selected features')

#Feature Selection using RFE and estimators as LGBM Classifier
rfe_selector_LGBM = RFE(estimator=LGBMClassifier(n_jobs=-1, random_state= 0), n_features_to_select=num_feats, verbose=5)
rfe_selector_LGBM.fit(X, y)
rfe_support_LGBM = rfe_selector_LGBM.get_support()
rfe_feature_LGBM = X.loc[:,rfe_support_LGBM].columns.tolist()
print(str(len(rfe_feature_LGBM)), 'selected features')

#Feature Selection with SelectFromModel using Decision Tree Classifer
SFM_selector_DT = SelectFromModel(DecisionTreeClassifier(random_state= 0), max_features=num_feats)
SFM_selector_DT.fit(X, y)
SFM_support_DT = SFM_selector_DT.get_support()
SFM_feature_DT = X.loc[:,SFM_support_DT].columns.tolist()
print(str(len(SFM_feature_DT)), 'selected features')

#Feature Selection with SelectFromModel using Random Forest Classifer
SFM_selector_RF = SelectFromModel(RandomForestClassifier(n_jobs=-1, random_state= 0), max_features=num_feats)
SFM_selector_RF.fit(X, y)
SFM_support_RF = SFM_selector_RF.get_support()
SFM_feature_RF = X.loc[:,SFM_support_RF].columns.tolist()
print(str(len(SFM_feature_RF)), 'selected features')

#Feature Selection with SelectFromModel using XGB Classifer
SFM_selector_XGB = SelectFromModel(XGBClassifier(n_jobs=-1, random_state= 0), max_features=num_feats)
SFM_selector_XGB.fit(X, y)
SFM_support_XGB = SFM_selector_XGB.get_support()
SFM_feature_XGB = X.loc[:,SFM_support_XGB].columns.tolist()
print(str(len(SFM_feature_XGB)), 'selected features')

#Feature Selection with SelectFromModel using Light GBM Classifier
SFM_selector_LGBM = SelectFromModel(LGBMClassifier(n_jobs=-1, random_state= 0), max_features=num_feats)
SFM_selector_LGBM.fit(X, y)

SFM_support_LGBM = SFM_selector_LGBM.get_support()
SFM_feature_LGBM = X.loc[:,SFM_support_LGBM].columns.tolist()
print(str(len(SFM_feature_LGBM)), 'selected features')

# Feature Selection with SelectKBest using chi
chi_selector = SelectKBest(chi2, k=num_feats)
chi_selector.fit(X, y)
chi_support = chi_selector.get_support()
skb_chi = X.loc[:,chi_support].columns.tolist()
print(str(len(skb_chi)), 'selected features')

feature_name = X.columns
# Combining all feature Selection results and creating a new dataset for feature importance
feature_selection_dataset = pd.DataFrame({'Feature':feature_name, 'RFE_DT':rfe_support_DT, 'RFE_RF':rfe_support_RF, 'RFE_XGB':rfe_support_XGB, 'RFE_LGBM':rfe_support_LGBM, 'SFM_DT':SFM_support_DT,
'SFM_RF':SFM_support_RF, 'SFM_XGB':SFM_support_XGB, 'SFM_LGBM':SFM_support_LGBM, 'SKB_CHI':chi_support})

# Counting selected times for each feature
feature_selection_dataset = feature_selection_dataset.fillna(0)
feature_selection_dataset= feature_selection_dataset*1
fet= feature_selection_dataset['Feature']
feature_selection_dataset= feature_selection_dataset.drop(['Feature'], axis=1)
feature_selection_dataset['Total'] = feature_selection_dataset.sum(axis=1)
feature_selection_dataset['Feature'] = fet
feature_selection_dataset = feature_selection_dataset.sort_values(['Total'] , ascending=False)
feature_selection_dataset.index = range(1, len(feature_selection_dataset)+1)

# Selecting the features which were suggested by atleast 3 models. The count for such features came out to be 80.
total_features_selected= feature_selection_dataset.head(80)
total_features_selected= total_features_selected['Feature']

# Based on Feature Selection, converted our train and test data set
X_final = X[total_features_selected]
y_final = y
test_final = test[total_features_selected]

test_final = test_final.values

test_final.shape

# Train test Split
X_train, X_test, y_train, y_test = train_test_split(X_final,y_final, test_size = 0.20, random_state = 0)
X_train.shape,X_test.shape

# Initializing Smote for Oversampling
smote = SMOTE(random_state= 0)

# Appled Smote on X_train and y_train
X_train, y_train = smote.fit_sample(X_train,y_train)

X_test = X_test.values
y_test = y_test.values

# Using XGB Classifier with hyperparameter tuning to train the model and performing internal validation
classifier = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
              colsample_bynode=1, colsample_bytree=0.8, gamma=1.4,
              learning_rate=0.1, max_delta_step=0, max_depth=16,
              min_child_weight=5, missing=None, n_estimators=700, n_jobs=-1,
              nthread=None, objective='multi:softmax', random_state=0,
              reg_alpha=0, reg_lambda=1, scale_pos_weight=1, seed=None,
              silent=None, subsample=0.8, verbosity=1, num_class = 2)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
print(confusion_matrix(y_test,y_pred))
print('Accuracy: ',accuracy_score(y_test, y_pred))
print(classification_report(y_test,y_pred))
print('F1 Score: ',f1_score(y_test, y_pred, average='macro'))

# Predicting the test dataset and saving it in a csv file for the submission
predictions = classifier.predict(test_final)
test_data = pd.read_csv("./Dataset/test.csv")
output = pd.DataFrame({'Id': test_data.x, 'Predicted': predictions})
output.to_csv('./Output/Chemical_Toxicity_Prediction.csv', index=False)
print("Submission done!")