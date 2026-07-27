import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

from data_loader import fetch_or_generate_dataset
from text_processor import TextMetadataPipeline

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs"))

def train_and_evaluate():
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("[*] Loading dataset...")
    df = fetch_or_generate_dataset()
    
    X_raw = df.drop(columns=["fraudulent"])
    y = df["fraudulent"].values

    print(f"[*] Splitting dataset (Stratified 80/20)... Total samples: {len(df)}")
    X_train_df, X_test_df, y_train, y_test = train_test_split(
        X_raw, y, test_size=0.20, random_state=42, stratify=y
    )

    print("[*] Fitting TextMetadataPipeline (TF-IDF + Metadata Scaling)...")
    pipeline = TextMetadataPipeline(max_tfidf_features=3000, use_metadata=True)
    X_train = pipeline.fit_transform(X_train_df)
    X_test = pipeline.transform(X_test_df)
    
    print(f"[+] Feature matrix shape: Train={X_train.shape}, Test={X_test.shape}")

    # Define classification models
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42),
        "Naive Bayes": MultinomialNB(alpha=0.1),
        "Random Forest": RandomForestClassifier(n_estimators=150, class_weight="balanced", random_state=42, n_jobs=-1),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42)
    }

    results = {}
    best_model_name = None
    best_f1 = -1
    best_model_obj = None

    for name, model in models.items():
        print(f"\n[>] Training {name}...")
        
        if name == "Naive Bayes":
            tb_pipeline = TextMetadataPipeline(max_tfidf_features=3000, use_metadata=False)
            X_tr_nb = tb_pipeline.fit_transform(X_train_df)
            X_te_nb = tb_pipeline.transform(X_test_df)
            model.fit(X_tr_nb, y_train)
            y_pred = model.predict(X_te_nb)
            y_prob = model.predict_proba(X_te_nb)[:, 1]
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else y_pred

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        auc = roc_auc_score(y_test, y_prob)
        cm = confusion_matrix(y_test, y_pred).tolist()

        print(f"    Accuracy : {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f} | F1: {f1:.4f} | ROC-AUC: {auc:.4f}")

        results[name] = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "roc_auc": round(float(auc), 4),
            "confusion_matrix": cm
        }

        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_model_obj = model

    print(f"\n[*] Best performing model based on F1-Score: {best_model_name} (F1 = {best_f1:.4f})")

    # Save metrics JSON
    metrics_path = os.path.join(OUTPUT_DIR, "model_comparison.json")
    with open(metrics_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"[+] Saved model comparison results to {metrics_path}")

    # Save best model pipeline
    pipeline_save_path = os.path.join(MODEL_DIR, "text_pipeline.joblib")
    model_save_path = os.path.join(MODEL_DIR, "best_classifier.joblib")
    joblib.dump(pipeline, pipeline_save_path)
    joblib.dump(best_model_obj, model_save_path)
    print(f"[+] Saved pipeline to {pipeline_save_path} and best model ({best_model_name}) to {model_save_path}")

    # Feature Importance for Logistic Regression / Best Model
    if hasattr(best_model_obj, "coef_"):
        tfidf_feature_names = pipeline.tfidf_vectorizer.get_feature_names_out().tolist()
        meta_names = ["telecommuting", "has_company_logo", "has_questions", "missing_company_profile", "missing_salary"]
        all_features = tfidf_feature_names + meta_names
        
        coefs = best_model_obj.coef_[0]
        if len(coefs) == len(all_features):
            top_fake_idx = np.argsort(coefs)[-20:][::-1]
            top_real_idx = np.argsort(coefs)[:20]
            
            top_fake_words = [{"feature": all_features[i], "weight": round(float(coefs[i]), 4)} for i in top_fake_idx]
            top_real_words = [{"feature": all_features[i], "weight": round(float(coefs[i]), 4)} for i in top_real_idx]
            
            feat_imp_path = os.path.join(OUTPUT_DIR, "feature_importance.json")
            with open(feat_imp_path, "w") as f:
                json.dump({"top_fraudulent_features": top_fake_words, "top_legitimate_features": top_real_words}, f, indent=2)
            print(f"[+] Saved feature importance weights to {feat_imp_path}")

    return results

if __name__ == "__main__":
    train_and_evaluate()
