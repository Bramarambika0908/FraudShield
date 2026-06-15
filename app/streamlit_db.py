import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from prediction import prediction_risk,expected_columns
from upi_prediction import (
    prediction_risk_upi,
    expected_columns as upi_columns
)


# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="FraudShield",
    page_icon="🛡️",
    layout="wide"
)


# SESSION STATE
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = []


# SIDEBAR
# =========================================================

st.sidebar.title("🛡️ FraudShield")
st.sidebar.caption("Real-Time Fraud Detection")

detection_mode = st.sidebar.selectbox(
    "Detection Type",
    [
        "💳 Credit Card Fraud",
        "🆙 UPI Fraud"
    ]
)

prediction_mode = st.sidebar.radio(
    "Prediction Mode",
    [
        "Manual Entry",
        "Upload CSV"
    ]
)

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🔍 Predict",
        "📊 Dashboard",
        "ℹ️ About"
    ]
)
st.sidebar.success("Model Loaded Successfully")
#st.sidebar.write("XGBoost Classifier")


# Home page 
# -----------------------------------------------------
if menu == "🏠 Home":

    col1, col2 = st.columns([4,1])

    with col1:
        st.title("🛡️ Real-Time Fraud Detection System")
        st.write(
            "Enter transaction details to predict fraud probability in real-time."
        )

    with col2:
        st.info(
            datetime.now().strftime("%d %b %Y\n%I:%M:%S %p")
        )

    st.markdown(
        f"""
        ### Selected Configuration

        **Detection Type:** {detection_mode}

        **Prediction Mode:** {prediction_mode}

        Use the sidebar to choose a fraud model and prediction method.
        """
    )
# 

#MENU PREDTCION
elif menu == "🔍 Predict":
    
   # credit + MANUAL
    
    if detection_mode == "💳 Credit Card Fraud" and prediction_mode == "Manual Entry":

        st.header("💳 Credit Card Fraud Detection")

    # Existing credit card input fields
        with st.container(border=True):

            st.subheader("💳 Transaction Details")

        # RESET BUTTON

            if st.button("🔄 Reset Features"):

                st.session_state["Amount"] = 0.0

                for i in range(1,9):
                    st.session_state[f"V{i}"] = 0.0

                st.rerun()

        
        # INPUT FEATURES
            cols = st.columns(4)

        # Amount input

            amount = cols[0].number_input(
                "Amount",
                value=0.0,
                key="Amount"
            )
        # Other features

            features = {}

            feature_columns = [
                col for col in expected_columns
                if col != "Amount"
            ]

            for i, col_name in enumerate(feature_columns):

                col = cols[i % 4]

                features[col_name] = col.number_input(
                    col_name,
                    value=0.0,
                    key=col_name
                )
            st.caption(
                "Provide all features for better fraud prediction."
            )

            predict = st.button("🔍 Predict Fraud")
            
            if predict:
                transaction = {}

                for col in expected_columns:
                    if col == "Amount":
                        transaction[col] = amount

                    else:
                        transaction[col] = features[col]
                    
                transaction = pd.DataFrame([transaction])

                transaction = transaction[expected_columns]
        
        #transaction = pd.DataFrame([transaction])
        #columns = ["Amount"] + [f"V{i}" for i in range(1,9)]

        #transaction = transaction[columns]
                prediction, risk_score, risk_level = prediction_risk(transaction) 
        
                st.subheader("Prediction Result") 
        
                st.write("Prediction :", prediction)
        
                st.write("Fraud Probability :", round(risk_score, 2), "%") 
        
                st.write("Risk Level :", risk_level)
# risk level analysis
    
                if risk_level == "HIGH RISK":
            
                    st.error("High Risk Fraud Transaction")
                elif risk_level == "MEDIUM RISK":
            
                    st.warning("Medium Risk Transaction") 
                else: 
                    st.success("Low Risk Genuine Transaction")
    # Other features

                st.session_state.history.append({
                "timestamp": datetime.now(),
                "prediction": prediction,
                "risk_score": risk_score,
                "risk_level": risk_level
                })

## credit + CSV
    elif detection_mode == "💳 Credit Card Fraud" and prediction_mode == "Upload CSV":

        st.header("📁 Upload Credit Card CSV")
        uploaded_file = st.file_uploader("Upload Credit Card CSV",type=["csv"])
        
        if uploaded_file:

            df = pd.read_csv(uploaded_file)

            st.dataframe(df.head())
# prediction ---------------------------------------------
            results = []

            for _, row in df.iterrows():
                    
                transaction = pd.DataFrame([row])

                pred, prob, risk = prediction_risk(transaction)

                results.append(
                {
                    "Prediction": pred,
                    "Probability": prob,
                    "Risk": risk
                }
                )

                st.session_state.history.append({
                    "timestamp": datetime.now(),
                    "prediction": pred,
                    "risk_score": prob,
                    "risk_level": risk
                })
                
                

            results_df = pd.concat(
                [df, pd.DataFrame(results)],
                axis=1
            )

            st.dataframe(results_df)
# download result of csv -------------------------

            #st.dataframe(results_df)                
            csv = results_df.to_csv(index=False)

            st.download_button(
                "📥 Download Results",
                csv,
                "credit_predictions.csv",
                "text/csv"
            )
# UPI+ MANUAL ----------------------

    elif detection_mode == "🆙 UPI Fraud" and prediction_mode == "Manual Entry":

        st.header("🆙 UPI Fraud Detection")

        cols = st.columns(4)

        values = {}

        for i, feature in enumerate(upi_columns):

            values[feature] = cols[i % 4].number_input(
                feature,
                value=0.0
            )
       
    # PREDICTION

        if st.button("Predict UPI Fraud"):

            transaction = pd.DataFrame([values])

            pred, prob, risk = prediction_risk_upi(transaction)

            st.success(f"Prediction : {pred}")
            st.write(f"Probability : {prob:.2f}%")
            st.write(f"Risk Level : {risk}")

            st.session_state.history.append({
                "timestamp": datetime.now(),
                "prediction": pred,
                "risk_score": prob,
                "risk_level": risk
            })

    #  UPI+ CSV ------------

    elif detection_mode == "🆙 UPI Fraud" and prediction_mode == "Upload CSV":

        uploaded_file = st.file_uploader(
            "Upload UPI CSV",
            type=["csv"]
        )

        if uploaded_file:

            df = pd.read_csv(uploaded_file)

            st.dataframe(df.head())

            results = []

            for _, row in df.iterrows():

                transaction = pd.DataFrame([row])

                pred, prob, risk = prediction_risk_upi(transaction)

                results.append(
                    {
                        "Prediction": pred,
                        "Probability": prob,
                        "Risk": risk
                    }
                )

                st.session_state.history.append({
                    "timestamp": datetime.now(),
                    "prediction": pred,
                    "risk_score": prob,
                    "risk_level": risk
                })

            results_df = pd.concat(
                [df, pd.DataFrame(results)],
                axis=1
            )
            st.dataframe(results_df)
    ## download results of upi 

            csv = results_df.to_csv(index=False)

            st.download_button(
                "📥 Download Results",
                csv,
                "upi_predictions.csv",
                "text/csv"
            )

# =========================================================
# DASHBOARD PAGE
# =========================================================

elif menu == "📊 Dashboard":

    st.title("📊 Dashboard")

    # -----------------------------------------------------
    # FEATURE IMPORTANCE
    # -----------------------------------------------------
    st.metric(
        "Total Predictions",
        len(st.session_state.get(
            "history", []
        ))
    )

    history_df = pd.DataFrame(st.session_state.history)
    
    if history_df.empty:

        st.info("No predictions available")

    else:
    # charts
    
        total = len(history_df)
    
        frauds = len(
            history_df[
                history_df["prediction"] == "Fraud"
            ]
        )
    
        st.metric("Total Transactions", total)
    
        st.metric("Fraud Detected", frauds)
    
        st.metric(
            "Fraud Rate",
            f"{(frauds/total)*100:.2f}%"
            if total else "0%"
        )
    

    # -----------------------------------------------------
    # FRAUD TREND
    # -----------------------------------------------------

        trend_df = history_df.copy()

        trend_df["hour"] = pd.to_datetime(
            trend_df["timestamp"]
        ).dt.hour
    
        trend = (
            trend_df
            .groupby("hour")
            .size()
            .reset_index(name="transactions")
        )
    
        fig = px.line(
            trend,
            x="hour",
            y="transactions"
        )
    
        st.plotly_chart(fig)
    
    
        fig = px.histogram(
        history_df,
        x="risk_score",
        nbins=20
        )
    
        st.plotly_chart(fig)
    
    st.subheader("Recent Transactions")
    
    st.dataframe(
            history_df.tail(10)
    )
# =========================================================
# ANALYTICS PAGE
# =========================================================

# =========================================================
# ABOUT PAGE
# =========================================================

elif menu == "ℹ️ About":

    st.title("ℹ️ About FraudShield")

    with st.container(border=True):

        st.write("""
        FraudShield is a Real-Time Fraud Detection
        System developed using Machine Learning
        and Streamlit.
        FraudShield is a multi-model fraud
        detection platform supporting:

        • Credit Card Fraud Detection
        • UPI Fraud Detection
        • Manual Predictions
        • CSV Batch Predictions

        Features:
        - Fraud Prediction
        - Risk Analysis
        - Dashboard Visualizations
        - Transaction History
        - Feature Analytics
        - Real-Time Prediction Interface
        """)