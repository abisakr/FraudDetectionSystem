import pandas as pd
import numpy as np

from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

import joblib


# Loading the credit card fraud dataset
creditcard_dataset = pd.read_csv('/content/AIML Dataset.csv')


# Dropping columns that are not required for model training
new_data = creditcard_dataset.drop(
    ['step', 'nameOrig', 'nameDest', 'isFlaggedFraud'],
    axis=1
)


# creditcard_dataset.info()
# creditcard_dataset['isFraud'].value_counts()
# creditcard_dataset.head()


# Numeric features used for model training
numeric_features = [
    'amount',
    'oldbalanceOrg',
    'newbalanceOrig',
    'oldbalanceDest',
    'newbalanceDest'
]


# Categorical feature
categorical_features = ['type']


# Creating Preprocessing Pipelines

# Numeric preprocessing:
# Missing values are filled using the median
# StandardScaler is used to scale numeric values
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])


# Categorical preprocessing:
# Missing values are filled using the most frequent category
# OneHotEncoder converts categorical values into numeric form
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(
        drop='first',
        handle_unknown='ignore'
    ))
])


# Combining numeric and categorical preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)


# new_data['isFraud'].value_counts()
# new_data.head()


# Separating features and target variable
X = new_data.drop(['isFraud'], axis=1)
Y = new_data['isFraud']


# Splitting dataset into training and testing data
# stratify=Y keeps the same fraud/non-fraud proportion
X_train, X_test, Y_train, Y_test = train_test_split(
    X,
    Y,
    test_size=0.2,
    stratify=Y,
    random_state=2
)


# Calculating class imbalance
# scale_pos_weight helps XGBoost pay more attention to fraud cases
number_non_fraud = (Y_train == 0).sum()
number_fraud = (Y_train == 1).sum()

scale_pos_weight = number_non_fraud / number_fraud

print("Non-Fraud Training Samples:", number_non_fraud)
print("Fraud Training Samples:", number_fraud)
print("Scale Pos Weight:", scale_pos_weight)


# Creating XGBoost pipeline
xgboost_pipeline = Pipeline(steps=[

    ('pre', preprocessor),

    ('mdl', XGBClassifier(

        # Number of boosting trees
        n_estimators=300,

        # Maximum depth of each tree
        max_depth=6,

        # Learning rate
        learning_rate=0.05,

        # Percentage of training rows used for each tree
        subsample=0.8,

        # Percentage of features used for each tree
        colsample_bytree=0.8,

        # Handles imbalanced fraud data
        scale_pos_weight=scale_pos_weight,

        # Evaluation metric
        eval_metric='logloss',

        # Random state for reproducibility
        random_state=2,

        # Use all CPU cores
        n_jobs=-1
    ))
])


# Training the XGBoost model
xgboost_pipeline.fit(
    X_train,
    Y_train
)


# Making predictions
predicted_val = xgboost_pipeline.predict(X_test)


# Calculating accuracy
score = accuracy_score(
    Y_test,
    predicted_val
)


print("\n--- Accuracy ---")
print("Accuracy:", score)
print(
    "Accuracy Percentage:",
    round(score * 100, 4),
    "%"
)


# Confusion Matrix
# [[True Negative, False Positive],
#  [False Negative, True Positive]]

print("\n--- Confusion Matrix ---")

print(
    confusion_matrix(
        Y_test,
        predicted_val
    )
)


# Classification Report
# Shows precision, recall,
# F1-score and support

print("\n--- Classification Report ---")

print(
    classification_report(
        Y_test,
        predicted_val,
        digits=4
    )
)


# Saving the trained XGBoost model
joblib.dump(
    xgboost_pipeline,
    'creditcard_fraud_detection_xgboost_model.pkl'
)


print(
    "\nModel saved successfully as "
    "'creditcard_fraud_detection_xgboost_model.pkl'!"
)