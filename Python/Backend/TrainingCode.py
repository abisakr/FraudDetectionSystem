import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.impute import SimpleImputer
import joblib

# Dataset link
# https://www.kaggle.com/datasets/amanalisiddiqui/fraud-detection-dataset?resource=download

creditcard_dataset = pd.read_csv('/content/AIML Dataset.csv')
new_data=creditcard_dataset.drop(['step','nameOrig','nameDest','isFlaggedFraud'], axis=1)
# creditcard_dataset.info()
# creditcard_dataset['Class'].value_counts()

# creditcard_dataset.head()


numeric_features = [
   'amount', 'oldbalanceOrg', 'newbalanceOrig',
    'oldbalanceDest', 'newbalanceDest'
]
categorical_features=['type']

#Creating Preprocessing Pipelines
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)

    ])

# new_dataset['Class'].value_counts()
# new_dataset.head()
X = new_data.drop(['isFraud'], axis=1)
Y = new_data['isFraud']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)


tuning_pipeline = Pipeline(steps=[
    ('pre',preprocessor),
    ('mdl',LogisticRegression(class_weight='balanced',max_iter=2000))
])


param_grid = {
    'mdl__C': [0.01, 0.1, 1, 10],
    'mdl__solver': ['lbfgs', 'liblinear']
}

grid_search = GridSearchCV(
    estimator=tuning_pipeline,
    param_grid=param_grid,
    cv=5,
    scoring='recall', # Focus tuning on catching the maximum amount of fraud
    n_jobs=-1
)
grid_search.fit(X_train,Y_train)
best_tuned_pipeline = grid_search.best_estimator_
predited_val=grid_search.predict(X_test)

score = accuracy_score(Y_test, predited_val)
print("Accuracy:", score)

print("\n--- Confusion Matrix ---")
print(confusion_matrix(Y_test, predited_val))

print("\n--- Classification Report ---")
print(classification_report(Y_test, predited_val))

joblib.dump(best_tuned_pipeline, 'creditcard_fraud_detection_model.pkl')
print("\nModel saved successfully as 'creditcard_fraud_detection_model.pkl'!")