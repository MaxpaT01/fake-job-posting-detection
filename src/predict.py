import os
import joblib
import pandas as pd
import numpy as np

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))

def load_pipeline_and_model():
    pipeline_path = os.path.join(MODEL_DIR, "text_pipeline.joblib")
    model_path = os.path.join(MODEL_DIR, "best_classifier.joblib")
    
    if not os.path.exists(pipeline_path) or not os.path.exists(model_path):
        raise FileNotFoundError("Model artifacts not found. Run model_trainer.py first.")
        
    pipeline = joblib.load(pipeline_path)
    model = joblib.load(model_path)
    return pipeline, model

def predict_job_posting(job_dict):
    """
    Input job_dict example:
    {
        "title": "Data Entry Specialist",
        "company_profile": "",
        "description": "Earn $50/hr working from home processing payments.",
        "requirements": "No experience needed.",
        "benefits": "Daily payout via PayPal.",
        "telecommuting": 1,
        "has_company_logo": 0,
        "has_questions": 0,
        "salary_range": ""
    }
    """
    pipeline, model = load_pipeline_and_model()
    
    df_sample = pd.DataFrame([job_dict])
    X_sample = pipeline.transform(df_sample)
    
    prob_fake = float(model.predict_proba(X_sample)[0][1])
    is_fake = int(prob_fake >= 0.5)
    
    risk_level = "Low Risk (Legitimate)"
    if prob_fake >= 0.65:
        risk_level = "High Risk (Fraudulent Scam)"
    elif prob_fake >= 0.35:
        risk_level = "Moderate Risk (Caution Advised)"

    return {
        "fraud_probability": round(prob_fake, 4),
        "is_fraudulent": is_fake,
        "risk_level": risk_level
    }

if __name__ == "__main__":
    test_job = {
        "title": "Remote Data Entry Clerk - Urgent Payout",
        "company_profile": "",
        "description": "Work from home 2 hours daily processing orders. Instant payment via Zelle or wire transfer.",
        "requirements": "Must have computer and bank account.",
        "benefits": "Daily bonuses up to $500.",
        "telecommuting": 1,
        "has_company_logo": 0,
        "has_questions": 0,
        "salary_range": ""
    }
    print("[*] Running inference test on sample scam posting...")
    res = predict_job_posting(test_job)
    print("Prediction Result:", res)
