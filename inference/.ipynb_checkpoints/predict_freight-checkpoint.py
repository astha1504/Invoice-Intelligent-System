import joblib
import pandas as pd
import os

# Keep your structure, just fix variable naming
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# FIX: define MODEL_PATH (you were missing this)
MODEL_PATH = os.path.join(BASE_DIR, "models", "predict_freight_model.pkl")


def load_model(model_path: str = MODEL_PATH):
    """
    Load trained freight cost prediction model.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ Model not found at: {model_path}")
    
    with open(model_path, "rb") as f:
        model = joblib.load(f)
    
    return model


def predict_freight_cost(input_data):
    """
    Predict freight cost for new vendor invoices.

    Parameters
    ----------
    input_data : dict

    Returns
    -------
    pd.DataFrame with predicted freight cost
    """
    model = load_model()  # your logic kept same
    input_df = pd.DataFrame(input_data)
    input_df['Predicted_Freight'] = model.predict(input_df).round()
    return input_df


if __name__ == "__main__":
    
    # Example inference run (local testing)
    sample_data = {
        "Dollars": [18500, 9000]
    }
    
    prediction = predict_freight_cost(sample_data)
    print(prediction)