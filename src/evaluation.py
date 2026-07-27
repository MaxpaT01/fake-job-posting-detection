import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve

from data_loader import fetch_or_generate_dataset
from text_processor import prepare_combined_text, TextMetadataPipeline

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs"))

def evaluate_preprocessing_impact():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("[*] Evaluating impact of preprocessing techniques...")

    df = fetch_or_generate_dataset()
    y = df["fraudulent"].values
    
    # 1. Raw Text vs Cleaned Text
    raw_text = (df["title"].fillna("") + " " + df["description"].fillna("") + " " + df["requirements"].fillna("")).astype(str)
    cleaned_text = prepare_combined_text(df)

    X_train_raw, X_test_raw, y_train, y_test = train_test_split(raw_text, y, test_size=0.2, random_state=42, stratify=y)
    X_train_cln, X_test_cln, _, _ = train_test_split(cleaned_text, y, test_size=0.2, random_state=42, stratify=y)

    # Vectorize Raw vs Cleaned
    vec_raw = TfidfVectorizer(max_features=3000)
    X_tr_r = vec_raw.fit_transform(X_train_raw)
    X_te_r = vec_raw.transform(X_test_raw)

    vec_cln = TfidfVectorizer(max_features=3000)
    X_tr_c = vec_cln.fit_transform(X_train_cln)
    X_te_c = vec_cln.transform(X_test_cln)

    # Train Logistic Regression on both
    clf_raw = LogisticRegression(class_weight="balanced", random_state=42).fit(X_tr_r, y_train)
    clf_cln = LogisticRegression(class_weight="balanced", random_state=42).fit(X_tr_c, y_train)

    pred_r = clf_raw.predict(X_te_r)
    pred_c = clf_cln.predict(X_te_c)

    impact_data = {
        "Raw Text (No Cleaning)": {
            "accuracy": round(float(accuracy_score(y_test, pred_r)), 4),
            "precision": round(float(precision_score(y_test, pred_r, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, pred_r, zero_division=0)), 4),
            "f1_score": round(float(f1_score(y_test, pred_r, zero_division=0)), 4),
            "roc_auc": round(float(roc_auc_score(y_test, clf_raw.predict_proba(X_te_r)[:, 1])), 4)
        },
        "Cleaned NLP Text": {
            "accuracy": round(float(accuracy_score(y_test, pred_c)), 4),
            "precision": round(float(precision_score(y_test, pred_c, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, pred_c, zero_division=0)), 4),
            "f1_score": round(float(f1_score(y_test, pred_c, zero_division=0)), 4),
            "roc_auc": round(float(roc_auc_score(y_test, clf_cln.predict_proba(X_te_c)[:, 1])), 4)
        }
    }

    # 2. Text-Only vs Text + Metadata
    pipeline = TextMetadataPipeline(max_tfidf_features=3000, use_metadata=True)
    X_raw_df = df.drop(columns=["fraudulent"])
    X_train_df, X_test_df, _, _ = train_test_split(X_raw_df, y, test_size=0.2, random_state=42, stratify=y)
    
    X_tr_hybrid = pipeline.fit_transform(X_train_df)
    X_te_hybrid = pipeline.transform(X_test_df)

    clf_hybrid = LogisticRegression(class_weight="balanced", random_state=42).fit(X_tr_hybrid, y_train)
    pred_h = clf_hybrid.predict(X_te_hybrid)

    impact_data["Cleaned Text + Metadata Signals"] = {
        "accuracy": round(float(accuracy_score(y_test, pred_h)), 4),
        "precision": round(float(precision_score(y_test, pred_h, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, pred_h, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_test, pred_h, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, clf_hybrid.predict_proba(X_te_hybrid)[:, 1])), 4)
    }

    print("[+] Preprocessing impact comparison:")
    for k, v in impact_data.items():
        print(f"    - {k}: Acc={v['accuracy']}, Prec={v['precision']}, Rec={v['recall']}, F1={v['f1_score']}, AUC={v['roc_auc']}")

    impact_path = os.path.join(OUTPUT_DIR, "preprocessing_impact.json")
    with open(impact_path, "w") as f:
        json.dump(impact_data, f, indent=2)
    print(f"[+] Saved preprocessing impact results to {impact_path}")

    # Plot impact bar chart
    plt.figure(figsize=(10, 5))
    metrics_df = pd.DataFrame(impact_data).T
    metrics_df[["f1_score", "roc_auc", "precision", "recall"]].plot(kind="bar", figsize=(10, 6))
    plt.title("Preprocessing & Feature Combination Impact Analysis", fontsize=14, fontweight="bold")
    plt.ylabel("Score")
    plt.ylim(0.5, 1.05)
    plt.xticks(rotation=15, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "preprocessing_impact_plot.png"), dpi=300)
    plt.close()
    print("[+] Saved preprocessing impact plot.")

if __name__ == "__main__":
    evaluate_preprocessing_impact()
