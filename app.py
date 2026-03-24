import streamlit as st
import joblib
import pandas as pd
import numpy as np
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============== LOAD MODEL ==============
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "invoice_flagging" / "models" / "predict_flag_invoice.pkl"
SCALER_PATH = BASE_DIR / "invoice_flagging" / "models" / "scaler.pkl"

@st.cache_resource
def load_model():
    """Load model and scaler from pickle files"""
    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        logger.info("Model and scaler loaded successfully")
        return {"model": model, "scaler": scaler}
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        st.error("Failed to load model")
        return None

def predict(data):
    """Make predictions on input data"""
    try:
        if st.session_state.model is None:
            return "Model not loaded"
        
        model = st.session_state.model["model"]
        scaler = st.session_state.model["scaler"]
        
        # Convert to DataFrame if needed
        if isinstance(data, pd.Series):
            data = data.to_frame().T
        
        # Scale the data
        scaled_data = scaler.transform(data)
        
        # Make prediction
        prediction = model.predict(scaled_data)
        return prediction[0]
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return f"Error: {str(e)}"

def validate_inputs(inputs):
    """Validate input data"""
    try:
        if isinstance(inputs, pd.Series):
            # Check for required columns and data types
            if inputs.isna().any():
                return False
            return True
        return False
    except Exception as e:
        logger.error(f"Input validation error: {e}")
        return False

# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = load_model()

# Page configuration
st.set_page_config(page_title='Invoice Intelligent System', layout='wide')

# Sidebar navigation
st.sidebar.title('Navigation')
page = st.sidebar.radio('Select a Page', ['Dashboard', 'Predict', 'Batch Upload'])

if page == 'Dashboard':
    st.title('Dashboard')
    st.metric(label='Metric 1', value='Value 1')
    st.metric(label='Metric 2', value='Value 2')

elif page == 'Predict':
    st.title('Predict Page')
    # TODO: Replace with form inputs for invoice features
    inputs = st.text_input('Enter your input:')
    if st.button('Predict'):
        if validate_inputs(inputs):
            prediction = predict(inputs)
            st.success(f'Prediction: {prediction}')
        else:
            st.error('Invalid inputs. Please check your data.')

elif page == 'Batch Upload':
    st.title('Batch Upload Page')
    uploaded_file = st.file_uploader('Upload CSV file', type='csv')
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            results = []
            for index, row in df.iterrows():
                if validate_inputs(row):
                    prediction = predict(row)
                    results.append(prediction)
                else:
                    results.append('Invalid input')
            
            results_df = pd.DataFrame({'Predictions': results})
            st.download_button(
                label='Download Results',
                data=results_df.to_csv(index=False).encode('utf-8'),
                file_name='results.csv',
                mime='text/csv',
                key='download_results'
            )
        except Exception as e:
            logger.error(f"Error processing CSV: {e}")
            st.error('Error processing the uploaded file.')
