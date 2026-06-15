import joblib

# LOAD MODEL AND SCALER

model = joblib.load("C:/Users/vadlu/AIML/projects/FraudShield/models/fraud_model.pkl")

scaler = joblib.load("C:/Users/vadlu/AIML/projects/FraudShield/models/scaler.pkl")

# TRAINED FEATURE NAMES

expected_columns = scaler.feature_names_in_

# PREDICTION FUNCTION

def prediction_risk(transaction):

    # SCALE INPUT

    scaled_transaction = scaler.transform(
        transaction
    )

    # PREDICT CLASS

    prediction = model.predict(
        scaled_transaction
    )[0]

    prediction_label = (
        "Fraud"
        if prediction == 1
        else "Genuine"
    )

    # PREDICT PROBABILITY

    probability = model.predict_proba(
        scaled_transaction
    )[0][1] * 100

    # RISK LEVEL

    if probability > 80:

        risk = "HIGH RISK"

    elif probability > 40:

        risk = "MEDIUM RISK"

    else:

        risk = "LOW RISK"

    return prediction_label, probability, risk
