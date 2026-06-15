# FraudShield
multi fraud detection system (CREDIT and UPI based detection)
## Problem Statement
Digital payment systems such as UPI and credit cards are increasingly vulnerable to fraudulent transactions, resulting in financial losses and security risks. Traditional methods often fail to detect suspicious activities in real time. This project aims to develop a machine learning-based fraud detection system that analyzes transaction data, identifies potentially fraudulent activities, generates risk scores, and provides real-time monitoring through an interactive dashboard.

### Datasets
**Digital Payment Fraud Detection Benchmark** This dataset simulates a large-scale digital payments ecosystem with realistic transactional, behavioral, and risk-driven fraud signals. It is designed as a benchmark dataset for fraud detection under temporal concept drift.

URL: https://www.kaggle.com/datasets/rohit8527kmr7518/digital-payment-fraud-detection-benchmark
**Credit Card Fraud Detection Dataset 2023** This dataset contains credit card transactions made by European cardholders in the year 2023. It comprises over 550,000 records, and the data has been anonymized to protect the cardholders' identities.

URL: https://www.kaggle.com/datasets/nelgiriyewithana/credit-card-fraud-detection-dataset-2023
isFraud: Indicates whether the transaction is fraudulent (1) or not (0)
### Model
**Credit Card Fraud Detection Model**
Algorithm: XGBoost Classifier
Preprocessing: StandardScaler,Exploratory Data Analysis (EDA) Feature Engineering
Data visualization: Matplotlib, seaborn
Models Evaluated: Logistic Regression, Support Vector Machine (SVC), XGBoost
Selected Model: XGBoost (chosen for superior fraud detection performance)
Output: Fraud prediction with probability-based risk scoring
Model File: fraud_model.pkl
**UPI Fraud Detection Model**
Algorithm: Support Vector Classifier (SVC)
Kernel: RBF (Radial Basis Function)
Preprocessing: StandardScaler integrated within a Scikit-learn Pipeline, Feature Engineering
Data visualization: Matplotlib, seaborn,Exploratory Data Analysis (EDA)
Models Evaluated: K-Nearest Neighbors (KNN), SVC, XGBoost
Selected Model: SVC with probability estimation enabled
Output: Fraud prediction, fraud probability, and risk level classification
Model File: fraud_upi_model.pkl
### Deployment
The fraud detection model is deployed using Render

streamlit Application Link: [FraudShield](https://fraudshield-cw2t.onrender.com)
### Usage
Users can enter transaction details manually or upload a CSV file for batch analysis. The system processes the transaction data, predicts whether a transaction is fraudulent or genuine, generates a risk score, and displays the results through an interactive real-time dashboard with analytics and monitoring features.
