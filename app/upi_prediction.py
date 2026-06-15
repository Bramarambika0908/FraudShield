import joblib 

pipeline=joblib.load("C:/Users/vadlu/AIML/projects/FraudShield/models/fraud_upi_model.pkl")

expected_columns = pipeline.feature_names_in_

def prediction_risk_upi(transaction):


    #  PIPELINE PREDICT CLASS

    prediction = pipeline.predict(transaction)[0]

    prediction_label = (
        "Fraud"
        if prediction == 1
        else "Genuine"
    )

    # PREDICT PROBABILITY

    probability = pipeline.predict_proba(
        transaction
    )[0][1] * 100

    # RISK LEVEL

    if probability > 80:

        risk = "HIGH RISK"

    elif probability > 40:

        risk = "MEDIUM RISK"

    else:

        risk = "LOW RISK"

    return prediction_label, probability, risk