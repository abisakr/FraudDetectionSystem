# AI Fraud Detection System

A full-stack web application that detects fraudulent financial transactions in real-time using a tuned Machine Learning model. The project features a sleek, responsive React frontend (styled with Tailwind CSS) and a lightweight Python Flask API that serves the trained scikit-learn classification pipeline.

## Features
* **High-Recall Detection:** Uses a Logistic Regression classifier with balanced class weights, optimized via Grid Search Cross-Validation to maximize the capture rate of rare fraudulent transactions.
* **End-to-End Pipeline:** The saved ML model handles its own data preprocessing (scaling numerical balances and one-hot encoding transaction types) directly from raw user input.
* **Modern UI:** A clean, glassmorphism-inspired interface built with React, TypeScript, and Tailwind CSS that provides dynamic visual alerts (red/green) based on transaction safety.
* **REST API:** A Flask backend that handles POST requests, processes transaction features, and returns real-time security classifications.

## Tech Stack
**Frontend:**
* React 18
* TypeScript
* Vite
* Tailwind CSS

**Backend / Machine Learning:**
* Python 3
* Flask & Flask-CORS
* Scikit-Learn
* Pandas & NumPy
* Joblib (Model Serialization)

---

## Project Structure

```text
FraudDetectionApp/
├── node_modules/
├── public/
├── Python_Backend/
│   ├── app.py
│   ├── creditcard_fraud_detection_model.pkl
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