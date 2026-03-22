
# Invoice Intelligent System

## Project Objective
The **Invoice Intelligent System** is designed to **automate invoice verification, freight cost prediction, and flag suspicious invoices** using machine learning models.  
This project aims to reduce manual effort in invoice processing, increase accuracy, and provide actionable insights for businesses.

---

## Features
- **Invoice Flagging** – Detect potentially fraudulent or incorrect invoices.  
- **Freight Cost Prediction** – Predict shipping costs using trained ML models.  
- **End-to-End Automation** – Preprocessing, training, and inference pipelines included.  
- **User-Friendly Interface** – Simple Python scripts to run predictions.  

---

## Project Structure

\`\`\`
├── app.py                 # Main application
├── freight_cost_prediction # Freight prediction scripts and models
│   ├── data_preprocessing.py
│   ├── model_evaluation.py
│   ├── train.py
│   └── models/predict_freight_model.pkl
├── invoice_flagging        # Invoice flagging scripts and models
│   ├── data_preprocessing.py
│   ├── modeling_evaluation.py
│   ├── train.py
│   └── models/predict_flag_invoice.pkl
├── inference               # Scripts for running predictions
├── notebooks               # Jupyter notebooks for analysis
├── models                  # Saved ML models
├── data                    # Input datasets
├── README.md
└── TODO.md
\`\`\`

---

## How to Use

1. **Clone the repository**:
\`\`\`bash
git clone https://github.com/astha1504/Invoice-Intelligent-System.git
cd Invoice-Intelligent-System
\`\`\`

2. **Install dependencies**:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. **Run the application**:
\`\`\`bash
python app.py
\`\`\`

4. **Run inference separately (optional)**:
\`\`\`bash
# For freight prediction
python inference/predict_freight.py

# For invoice flagging
python inference/predict_invoice_flag.py
\`\`\`

---

## Flowchart

![Invoice Intelligent System Flowchart](flowchart.png)


---

## Additional Notes
- Large files like `.pkl` models and notebooks are tracked using **Git LFS**.  
- Make sure LFS is installed if cloning the repository:
\`\`\`bash
git lfs install
\`\`\`

---

## Author
**Astha Singh**  
B.Tech CSE (AI & ML) | AI Intern @ Infosys Springboard  
GitHub: [astha1504](https://github.com/astha1504)
EOF
