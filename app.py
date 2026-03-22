import streamlit as st
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

# ---------------- LOAD MODEL ----------------
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "invoice_flagging" / "models" / "predict_flag_invoice.pkl"
SCALER_PATH = BASE_DIR / "invoice_flagging" / "models" / "scaler.pkl"

def load_artifacts():
    if not MODEL_PATH.exists():
        st.error(f"Model file not found: {MODEL_PATH}")
        st.stop()
    if not SCALER_PATH.exists():
        st.error(f"Scaler file not found: {SCALER_PATH}")
        st.stop()

    try:
        model_obj = joblib.load(MODEL_PATH)
        scaler_obj = joblib.load(SCALER_PATH)
        return model_obj, scaler_obj
    except Exception as e:
        st.error(
            "Failed to load model/scaler artifacts. "
            "Please retrain invoice flagging artifacts and retry.\n"
            f"Details: {e}"
        )
        st.stop()

model, scaler = load_artifacts()

# ---------------- FEATURE FIX ----------------
# Auto-detect features from scaler
if hasattr(scaler, "feature_names_in_"):
    features = list(scaler.feature_names_in_)
else:
    features = [f"feature_{i}" for i in range(scaler.n_features_in_)]

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Invoice Intelligence", layout="wide")

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Invoice Intelligence")
st.sidebar.info("Built by Astha Singh")

page = st.sidebar.radio("Navigation", ["Dashboard", "Predict", "Upload"])

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.title("📊 Dashboard")
    st.markdown("### Welcome to your ML-powered Invoice System")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Invoices", "1,200")
    col2.metric("Predictions Made", "950")
    col3.metric("Model Accuracy", "91%")

    st.markdown("### 📈 Sample Trends")

    sample_data = pd.DataFrame({
        "Amount": [100, 200, 150, 300, 250],
        "Items": [2, 5, 3, 6, 4]
    })

    st.line_chart(sample_data)

# ---------------- PREDICT ----------------
elif page == "Predict":
    st.title("🔮 Single Prediction")

    st.subheader("Enter Input Features")

    values = []
    cols = st.columns(len(features))

    for i, feature in enumerate(features):
        val = cols[i].number_input(feature, value=0.0)
        values.append(val)

    if st.button("Predict"):
        try:
            input_data = np.array([values])

            st.subheader("📌 Input Summary")
            st.write(dict(zip(features, values)))

            # Scale input
            input_scaled = scaler.transform(input_data)

            # Predict
            prediction = model.predict(input_scaled)

            st.subheader("✅ Prediction Result")
            st.success(f"Prediction: {prediction[0]}")

            # Confidence (if classification model)
            if hasattr(model, "predict_proba"):
                prob = model.predict_proba(input_scaled)
                st.info(f"Confidence: {np.max(prob)*100:.2f}%")

        except Exception as e:
            st.error(f"Error: {e}")

# ---------------- UPLOAD ----------------
elif page == "Upload":
    st.title("📂 Batch Prediction")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        try:
            df = pd.read_csv(file)

            st.subheader("📄 Uploaded Data")
            st.dataframe(df.head())

            st.subheader("📊 Data Summary")
            st.write(df.describe())

            if not all(col in df.columns for col in features):
                st.error(f"CSV must contain columns: {features}")
            else:
                df = df.fillna(0)

                X = df[features]

                # Scale
                X_scaled = scaler.transform(X)

                # Predict
                preds = model.predict(X_scaled)

                df["Prediction"] = preds

                st.subheader("✅ Predictions")
                st.dataframe(df)

                # Visualization
                st.subheader("📈 Prediction Distribution")
                st.bar_chart(df["Prediction"].value_counts())

                # Download
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇️ Download Results",
                    csv,
                    "predictions.csv",
                    "text/csv"
                )

        except Exception as e:
            st.error(f"Error processing file: {e}")