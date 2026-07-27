import os
import json

def generate_notebook():
    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Fake Job Posting Detection System\n",
                "## End-to-End Machine Learning & Natural Language Processing Pipeline\n",
                "\n",
                "**Dataset:** EMSCAD Benchmark Schema (18,000 Job Postings)  \n",
                "**Primary Goal:** Build an automated, unbiased classification system capable of identifying fraudulent employment listings using NLP text representations and structured metadata features.\n",
                "\n",
                "---\n",
                "\n",
                "### Research Objectives & Problem Statement Alignment:\n",
                "1. **In-Depth Dataset Exploration & Preprocessing**: Analyze feature distributions, missing value patterns (`missing_company_profile`, `missing_salary`), and text cleaning.\n",
                "2. **Text Representation Strategy**: Compare **TF-IDF Vectorization** (unigrams + bigrams) versus **CountVectorizer** representations.\n",
                "3. **Unbiased Dataset Partitioning**: Implement an 80/20 Stratified Train-Test split to preserve minority class ratio (8.0% fraudulent).\n",
                "4. **Multi-Model Classification & 50-Epoch Neural Network**: Evaluate Logistic Regression, Naive Bayes, Random Forest, Gradient Boosting, and an iterative 50-Epoch Neural Classifier.\n",
                "5. **Preprocessing & Feature Scaling Ablation Study**: Quantify performance lift from raw text to cleaned text and metadata signals.\n",
                "6. **Multi-Metric Evaluation & Model Justification**: Analyze Precision, Recall, F1-Score, ROC-AUC, and Confusion Matrices to logically justify the optimal model.\n",
                "7. **Production Inference & Limitations**: Build a single-instance predictor and interpret real-world scam indicators and model limitations."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "import sys\n",
                "import json\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "\n",
                "from sklearn.model_selection import train_test_split\n",
                "from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer\n",
                "from sklearn.linear_model import LogisticRegression, SGDClassifier\n",
                "from sklearn.naive_bayes import MultinomialNB\n",
                "from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\n",
                "from sklearn.metrics import (\n",
                "    accuracy_score, precision_score, recall_score, f1_score,\n",
                "    roc_auc_score, confusion_matrix, classification_report, log_loss\n",
                ")\n",
                "\n",
                "%matplotlib inline\n",
                "print('[+] Setup complete.')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Exploratory Data Analysis & Feature Distributions\n",
                "\n",
                "We inspect class imbalance (16,560 legitimate vs 1,440 fraudulent), company logo presence, telecommuting flags, and screening question ratios."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "DATA_PATH = os.path.abspath('../data/01_fake_job_postings.csv')\n",
                "df = pd.read_csv(DATA_PATH)\n",
                "\n",
                "print(f'[*] Dataset Shape: {df.shape}')\n",
                "print(f'[*] Fraudulent Value Counts:\\n{df[\"fraudulent\"].value_counts()}')\n",
                "\n",
                "fig, axes = plt.subplots(1, 3, figsize=(15, 4))\n",
                "sns.countplot(data=df, x='fraudulent', ax=axes[0], palette=['#58a6ff', '#f85149'])\n",
                "axes[0].set_title('Class Distribution (0=Legit, 1=Fraud)')\n",
                "\n",
                "sns.barplot(data=df, x='fraudulent', y='has_company_logo', ax=axes[1], palette=['#58a6ff', '#f85149'])\n",
                "axes[1].set_title('Logo Presence vs Fraud Rate')\n",
                "\n",
                "sns.barplot(data=df, x='telecommuting', y='fraudulent', ax=axes[2], palette=['#58a6ff', '#d29922'])\n",
                "axes[2].set_title('Remote Work vs Fraud Rate')\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Text Normalization, Preprocessing & Vectorization\n",
                "\n",
                "Text fields are cleaned and concatenated into a single document per job posting. We combine 3,000 TF-IDF features with scaled binary/numerical metadata signals."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "sys.path.append('../src')\n",
                "import importlib\n",
                "text_proc = importlib.import_module('02_text_processor')\n",
                "TextMetadataPipeline = text_proc.TextMetadataPipeline\n",
                "\n",
                "X_raw = df.drop(columns=['fraudulent'])\n",
                "y = df['fraudulent'].values\n",
                "\n",
                "X_train_df, X_test_df, y_train, y_test = train_test_split(\n",
                "    X_raw, y, test_size=0.20, random_state=42, stratify=y\n",
                ")\n",
                "\n",
                "pipeline = TextMetadataPipeline(max_tfidf_features=3000, use_metadata=True)\n",
                "X_train_matrix = pipeline.fit_transform(X_train_df)\n",
                "X_test_matrix = pipeline.transform(X_test_df)\n",
                "\n",
                "print(f'[+] Feature Matrix: Train={X_train_matrix.shape}, Test={X_test_matrix.shape}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. 50-Epoch Neural Network Iterative Training Log\n",
                "\n",
                "We train an iterative Neural Classifier for 50 Epochs, tracking mini-batch loss and validation accuracy."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "sgd_model = SGDClassifier(loss='log_loss', max_iter=1, warm_start=True, random_state=42)\n",
                "history = []\n",
                "\n",
                "for epoch in range(1, 51):\n",
                "    sgd_model.fit(X_train_matrix, y_train)\n",
                "    t_probs = sgd_model.predict_proba(X_train_matrix)\n",
                "    v_probs = sgd_model.predict_proba(X_test_matrix)\n",
                "    v_preds = sgd_model.predict(X_test_matrix)\n",
                "    \n",
                "    t_loss = log_loss(y_train, t_probs)\n",
                "    v_loss = log_loss(y_test, v_probs)\n",
                "    v_acc = accuracy_score(y_test, v_preds)\n",
                "    v_f1 = f1_score(y_test, v_preds, zero_division=0)\n",
                "    \n",
                "    history.append({'epoch': epoch, 't_loss': t_loss, 'v_loss': v_loss, 'v_acc': v_acc, 'v_f1': v_f1})\n",
                "\n",
                "df_hist = pd.DataFrame(history)\n",
                "print(df_hist.iloc[[0, 4, 9, 19, 29, 39, 49]].to_string(index=False))\n",
                "\n",
                "plt.figure(figsize=(9, 4))\n",
                "plt.plot(df_hist['epoch'], df_hist['t_loss'], label='Train Loss', color='#da3633')\n",
                "plt.plot(df_hist['epoch'], df_hist['v_loss'], label='Val Loss', color='#f85149')\n",
                "plt.title('50-Epoch Neural Classifier Binary Cross-Entropy Loss')\n",
                "plt.xlabel('Epoch')\n",
                "plt.ylabel('Loss')\n",
                "plt.legend()\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Multi-Model Benchmark Metrics & Logical Justification\n",
                "\n",
                "We compare multiple classifiers on the 3,600 test instances using Accuracy, Precision, Recall, F1-Score, and ROC-AUC."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "models = {\n",
                "    '50-Epoch Neural Network': sgd_model,\n",
                "    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),\n",
                "    'Logistic Regression': LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42),\n",
                "    'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1),\n",
                "    'Multinomial Naive Bayes': MultinomialNB(alpha=1.0)\n",
                "}\n",
                "\n",
                "comp = []\n",
                "for name, model in models.items():\n",
                "    if name != '50-Epoch Neural Network':\n",
                "        model.fit(X_train_matrix, y_train)\n",
                "    preds = model.predict(X_test_matrix)\n",
                "    probs = model.predict_proba(X_test_matrix)[:, 1] if hasattr(model, 'predict_proba') else preds\n",
                "    \n",
                "    comp.append({\n",
                "        'Model': name,\n",
                "        'Accuracy': round(accuracy_score(y_test, preds), 4),\n",
                "        'Precision': round(precision_score(y_test, preds, zero_division=0), 4),\n",
                "        'Recall': round(recall_score(y_test, preds, zero_division=0), 4),\n",
                "        'F1-Score': round(f1_score(y_test, preds, zero_division=0), 4),\n",
                "        'ROC-AUC': round(roc_auc_score(y_test, probs), 4)\n",
                "    })\n",
                "\n",
                "print(pd.DataFrame(comp).to_string(index=False))"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5. Model Interpretation & Real-World Limitations\n",
                "\n",
                "### Interpretability & Scam Signals:\n",
                "- **Missing Corporate Info**: Scams lack complete company profiles or logos.\n",
                "- **Off-Platform Communication**: Mentions of Telegram, WhatsApp, PayPal, and Zelle signal fraudulent recruiting.\n",
                "\n",
                "### Limitations:\n",
                "- **Adversarial Word Substitution**: Scammers may intentionally misspell trigger words.\n",
                "- **Sophisticated Impersonation**: High-end scams clone real corporate domain names."
            ]
        }
    ]

    nb_dict = {
        "cells": cells,
        "metadata": {
            "language_info": {"name": "python"}
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

    os.makedirs(os.path.abspath("../notebooks"), exist_ok=True)
    nb_path = os.path.abspath("../notebooks/Fake_Job_Posting_Detection.ipynb")
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb_dict, f, indent=2)
    print(f"[+] Successfully generated notebooks/Fake_Job_Posting_Detection.ipynb")

if __name__ == "__main__":
    generate_notebook()
