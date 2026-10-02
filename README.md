# AI Fraud Detection System

A full-stack web application that detects potentially fraudulent financial transactions in real time using an **XGBoost Machine Learning model**.

The project combines a responsive **React + TypeScript frontend** with a lightweight **Python Flask REST API**. The trained XGBoost model analyzes transaction information and classifies a transaction as either **Fraud** or **Non-Fraud**.

## Features

* **XGBoost Fraud Detection:** Uses an `XGBClassifier` to learn complex patterns between transaction amounts, balances, transaction types, and fraudulent activity.

* **Imbalanced Data Handling:** The dataset contains significantly fewer fraudulent transactions than legitimate transactions. `scale_pos_weight` is used to give greater importance to the minority fraud class during model training.

* **High Fraud Recall:** The trained model achieved a fraud recall of approximately **99.51%**, detecting **1,635 out of 1,643** fraud transactions in the test set.

* **End-to-End ML Pipeline:** The saved model contains preprocessing and classification in a single pipeline. Numerical features are processed using median imputation and standardization, while transaction type is processed using one-hot encoding.

* **Real-Time Prediction:** Users can enter transaction details through the frontend and receive an immediate Fraud or Non-Fraud prediction.

* **Modern UI:** A responsive interface built with React, TypeScript, Vite, and Tailwind CSS displays transaction results using clear visual alerts.

* **REST API:** A Flask backend accepts transaction information through POST requests and sends it to the trained model for classification.

---

## Machine Learning Model

The project uses **XGBoost (Extreme Gradient Boosting)** for binary classification.

XGBoost builds multiple decision trees sequentially. Each new tree attempts to correct errors made by previous trees, allowing the model to learn complex relationships between transaction features.

### Input Features

The model uses the following transaction information:

* `amount` — Transaction amount
* `oldbalanceOrg` — Sender's balance before the transaction
* `newbalanceOrig` — Sender's balance after the transaction
* `oldbalanceDest` — Receiver's balance before the transaction
* `newbalanceDest` — Receiver's balance after the transaction
* `type` — Transaction type

The target variable is:

* `isFraud`
  * `0` = Non-Fraud
  * `1` = Fraud

---

## Handling Class Imbalance

The training dataset is highly imbalanced:

```text
Non-Fraud Training Samples: 5,083,526
Fraud Training Samples:         6,570
```

The class-weight ratio was calculated as:

```text
scale_pos_weight = Non-Fraud Samples / Fraud Samples

scale_pos_weight = 5,083,526 / 6,570

scale_pos_weight ≈ 773.75
```

This gives additional importance to fraud cases during XGBoost training and helps the model detect rare fraudulent transactions.

---

## Model Performance

The XGBoost model produced the following results on the held-out test dataset:

```text
Accuracy: 0.9965965278454473
Accuracy Percentage: 99.6597%
```

### Confusion Matrix

```text
[[1266558    4323]
 [      8    1635]]
```

This represents:

* **1,266,558 True Negatives** — legitimate transactions correctly classified as non-fraud.
* **4,323 False Positives** — legitimate transactions incorrectly classified as fraud.
* **8 False Negatives** — fraudulent transactions incorrectly classified as legitimate.
* **1,635 True Positives** — fraudulent transactions correctly detected.

### Classification Report

```text
              precision    recall  f1-score   support

           0     1.0000    0.9966    0.9983   1270881
           1     0.2744    0.9951    0.4302      1643

    accuracy                         0.9966   1272524
   macro avg     0.6372    0.9959    0.7142   1272524
weighted avg     0.9991    0.9966    0.9976   1272524
```

### Performance Interpretation

The model achieved a **99.51% recall for fraudulent transactions**, meaning that it successfully identified almost all fraud cases in the test dataset.

However, fraud precision was **27.44%**, indicating that the model also generated false-positive fraud alerts. This reflects a deliberate emphasis on recall caused by the strong class weighting: the model prioritizes minimizing missed fraud cases.

Because the dataset is highly imbalanced, overall accuracy alone should not be used to evaluate the model. **Precision, recall, F1-score, and the confusion matrix** provide more meaningful information about fraud-detection performance.

---

## Tech Stack

### Frontend

* React 18
* TypeScript
* Vite
* Tailwind CSS

### Backend

* Python 3
* Flask
* Flask-CORS

### Machine Learning

* XGBoost
* Scikit-Learn
* Pandas
* NumPy
* Joblib

---

## Dataset

The project uses the **Fraud Detection Dataset** available on Kaggle.

Dataset:

https://www.kaggle.com/datasets/amanalisiddiqui/fraud-detection-dataset?resource=download

The dataset contains financial transaction records and information such as transaction type, amount, sender and receiver balances, and fraud labels.

---

## Project Structure

```text
FraudDetectionApp/
├── node_modules/
├── public/
├── Python_Backend/
│   ├── app.py
│   ├── creditcard_fraud_detection_xgboost_model.pkl
│   └── TrainingCode.py
├── src/
│   ├── assets/
│   │   ├── react.svg
│   │   └── vite.svg
│   ├── components/
│   │   └── FraudDetection.tsx
│   ├── App.tsx
│   ├── index.css
│   └── main.tsx
├── .gitignore
├── eslint.config.js
├── index.html
├── package-lock.json
├── package.json
├── postcss.config.mjs
├── README.md
├── tsconfig.app.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

---

## How the System Works

```text
User enters transaction details
            ↓
React Frontend
            ↓
POST /api/predict
            ↓
Flask Backend
            ↓
Preprocessing Pipeline
            ↓
XGBoost Model
            ↓
Fraud / Non-Fraud Prediction
            ↓
Result displayed to the user
```

The frontend collects transaction information and sends it to the Flask API. The backend converts the input into a Pandas DataFrame and passes it through the saved preprocessing and XGBoost pipeline. The prediction is then returned to the frontend as a JSON response.

---

## Running the Project

### 1. Install Backend Dependencies

```bash
pip install flask flask-cors pandas numpy scikit-learn xgboost joblib
```

### 2. Start the Flask Backend

Navigate to the backend directory:

```bash
cd Python_Backend
```

Run:

```bash
python app.py
```

The Flask API will run locally on:

```text
http://127.0.0.1:5000
```

### 3. Install Frontend Dependencies

From the main project directory:

```bash
npm install
```

### 4. Start the Frontend

```bash
npm run dev
```

Open the local URL provided by Vite in your browser.

---

## API Endpoint

### Predict Transaction

```text
POST /api/predict
```

Example request:

```json
{
  "amount": 485000,
  "oldbalanceOrg": 485000,
  "newbalanceOrig": 0,
  "oldbalanceDest": 0,
  "newbalanceDest": 485000,
  "type": "TRANSFER"
}
```

Example response:

```json
{
  "status": "success",
  "is_fraud": true
}
```

---

## Model File

The trained XGBoost pipeline is serialized using Joblib and stored as:

```text
creditcard_fraud_detection_xgboost_model.pkl
```

The Flask backend loads this model when the application starts and uses it to perform real-time transaction predictions.

---

## Limitations

The model is intended as a machine-learning project and demonstration system rather than a production banking fraud-detection service.

The model's high fraud recall comes with a relatively high number of false-positive alerts. Future improvements could include threshold optimization, additional feature engineering, hyperparameter tuning, probability calibration, and comparison with other gradient-boosting algorithms such as LightGBM and CatBoost.