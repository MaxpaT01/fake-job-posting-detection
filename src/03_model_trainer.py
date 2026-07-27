import os
import sys
import json
import joblib
import importlib
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, log_loss
)

warnings.filterwarnings('ignore')

sys.path.append(os.path.dirname(__file__))

data_loader_mod = importlib.import_module("01_data_loader")
text_proc_mod = importlib.import_module("02_text_processor")

fetch_or_generate_dataset = data_loader_mod.fetch_or_generate_dataset
TextMetadataPipeline = text_proc_mod.TextMetadataPipeline

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs"))

def train_and_evaluate():
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("[*] Loading benchmark dataset (18,000 records)...")
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

    print("\n========================================================")
    print("[*] TRAINING NEURAL NETWORK MODEL FOR 50 EPOCHS...")
    print("========================================================")

    sgd_model = SGDClassifier(loss='log_loss', max_iter=1, warm_start=True, random_state=42, learning_rate='optimal', alpha=1e-4)
    
    epoch_history = []
    
    for epoch in range(1, 51):
        sgd_model.fit(X_train, y_train)
        
        train_probs = sgd_model.predict_proba(X_train)
        val_probs = sgd_model.predict_proba(X_test)
        
        train_preds = sgd_model.predict(X_train)
        val_preds = sgd_model.predict(X_test)
        
        t_loss = log_loss(y_train, train_probs)
        v_loss = log_loss(y_test, val_probs)
        
        t_acc = accuracy_score(y_train, train_preds)
        v_acc = accuracy_score(y_test, val_preds)
        v_prec = precision_score(y_test, val_preds, zero_division=0)
        v_rec = recall_score(y_test, val_preds, zero_division=0)
        v_f1 = f1_score(y_test, val_preds, zero_division=0)
        
        epoch_history.append({
            "epoch": epoch,
            "train_loss": round(float(t_loss), 4),
            "val_loss": round(float(v_loss), 4),
            "train_acc": round(float(t_acc), 4),
            "val_acc": round(float(v_acc), 4),
            "precision": round(float(v_prec), 4),
            "recall": round(float(v_rec), 4),
            "f1_score": round(float(v_f1), 4)
        })

        if epoch in [1, 5, 10, 20, 30, 40, 50]:
            print(f"Epoch {epoch:02d}/50 | Train Loss: {t_loss:.4f} | Val Loss: {v_loss:.4f} | Val Acc: {v_acc:.4f} | Val F1: {v_f1:.4f}")

    history_path = os.path.join(OUTPUT_DIR, "training_history.json")
    with open(history_path, "w") as f:
        json.dump(epoch_history, f, indent=2)
    print(f"[+] Exported 50-epoch training history to {history_path}")

    epochs = [e["epoch"] for e in epoch_history]
    t_losses = [e["train_loss"] for e in epoch_history]
    v_losses = [e["val_loss"] for e in epoch_history]
    v_accs = [e["val_acc"] for e in epoch_history]

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(epochs, t_losses, label="Train Loss", color="#da3633", linestyle="--")
    ax1.plot(epochs, v_losses, label="Val Loss", color="#f85149", linewidth=2)
    ax1.set_xlabel("Epochs")
    ax1.set_ylabel("Binary Cross-Entropy Loss", color="#f85149")
    ax1.tick_params(axis='y', labelcolor="#f85149")

    ax2 = ax1.twinx()
    ax2.plot(epochs, v_accs, label="Val Accuracy", color="#238636", linewidth=2)
    ax2.set_ylabel("Validation Accuracy", color="#238636")
    ax2.tick_params(axis='y', labelcolor="#238636")

    plt.title("50-Epoch Neural Classifier Training & Convergence Curves", fontsize=13, fontweight="bold")
    fig.tight_layout()
    plot_path = os.path.join(OUTPUT_DIR, "50_epochs_loss_accuracy.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()

    print("\n========================================================")
    print("[*] TRAINING BENCHMARK CLASSIFIERS...")
    print("========================================================")

    models = {
        "50-Epoch Neural Network": sgd_model,
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1),
        "Multinomial Naive Bayes": MultinomialNB(alpha=1.0)
    }

    results = {}
    best_model_name = None
    best_f1 = -1
    best_model_obj = None

    for name, model in models.items():
        if name != "50-Epoch Neural Network":
            print(f"[>] Training {name}...")
            if name == "Multinomial Naive Bayes":
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
        else:
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        auc = roc_auc_score(y_test, y_prob)
        cm = confusion_matrix(y_test, y_pred).tolist()

        print(f"    {name} -> Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f} | AUC: {auc:.4f}")

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

    metrics_path = os.path.join(OUTPUT_DIR, "model_comparison.json")
    with open(metrics_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"[+] Saved model comparison results to {metrics_path}")

    pipeline_save_path = os.path.join(MODEL_DIR, "text_pipeline.joblib")
    model_save_path = os.path.join(MODEL_DIR, "best_classifier.joblib")
    joblib.dump(pipeline, pipeline_save_path)
    joblib.dump(best_model_obj, model_save_path)
    print(f"[+] Saved pipeline to {pipeline_save_path} and best model ({best_model_name}) to {model_save_path}")

    return results

if __name__ == "__main__":
    train_and_evaluate()
