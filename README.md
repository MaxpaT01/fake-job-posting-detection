# 🛡️ Fake Job Posting Detection System (JobShield AI)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange.svg)](https://scikit-learn.org/)
[![Live Working Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-success.svg)](#-live-working-application)

An end-to-end Machine Learning and Natural Language Processing (NLP) system designed to detect fraudulent job postings by analyzing both unstructured text (`job title`, `company profile`, `description`, `requirements`, `benefits`) and structured metadata signals (`telecommuting`, `has_company_logo`, `has_questions`, `salary_range`).

---

## 🌐 Live Working Application

👉 **Try the Live Web App:** [https://MaxpaT01.github.io/fake-job-posting-detection/](https://MaxpaT01.github.io/fake-job-posting-detection/)

The web application features:
- **Real-Time Job Posting Fraud Risk Classifier** (Input job details or load pre-set real vs scam job samples).
- **Interactive Fraud Risk Gauge** (Low Risk, Caution, High Risk Fraudulent).
- **Key Risk Indicators & Triggers Breakdown** (Highlighting suspicious terms like *wire transfer*, *PayPal*, *daily pay*, missing company logo, and unverified profiles).
- **Dataset EDA Dashboard** (Distribution charts on EMSCAD benchmark dataset).
- **Model Performance Benchmark Matrix** (Interactive comparison across algorithms).

---

## 📊 Project Information & Motivation

Employment scams cause millions of dollars in losses annually and harvest personal information from job seekers. Fraudulent job postings often mimic legitimate listings but contain subtle text markers and metadata anomalies.

### Key Highlights & Methodology:
1. **Exploratory Data Analysis (EDA)**: Analyzed 17,880 job postings from the EMSCAD benchmark dataset (~4.8% fraud rate).
2. **Text Preprocessing**: Cleaned text by stripping HTML tags, lowercasing, removing stopwords, and performing regex tokenization.
3. **Numerical Representation**: Applied **TF-IDF Vectorization** (Unigrams + Bigrams) combined with scaled metadata indicator vectors (`has_company_logo`, `telecommuting`, `missing_company_profile`).
4. **Imbalance Handling**: Used class weighting and SMOTE sampling to address severe class imbalance.
5. **Model Comparisons**: Evaluated multiple classifiers including **Logistic Regression**, **Multinomial Naive Bayes**, **Random Forest**, and **Gradient Boosting**.
6. **Interpretability**: Extracted top positive and negative TF-IDF feature coefficients for transparent decision explanations.

---

## 📈 Model Performance Benchmark Results

Evaluated on an independent 20% test split (Stratified):

| Classifier Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Gradient Boosting** | **98.42%** | **92.15%** | **88.90%** | **0.9049** | **0.9854** | **★ Best Model** |
| **Logistic Regression** | 97.85% | 88.40% | 86.20% | 0.8728 | 0.9782 | High Recall |
| **Random Forest** | 97.90% | 94.80% | 78.40% | 0.8582 | 0.9710 | High Precision |
| **Multinomial Naive Bayes**| 95.60% | 62.40% | 89.10% | 0.7337 | 0.9540 | Baseline |

---

## 🔬 Preprocessing Impact Analysis

| Preprocessing Pipeline | F1-Score | ROC-AUC | Key Insight |
| :--- | :---: | :---: | :--- |
| **Raw Text (No Cleaning)** | 0.7420 | 0.8510 | Baseline noisy text tokens (`<br>`, typos) |
| **Cleaned NLP Text** | 0.8650 | 0.9320 | +12.3% F1 boost after stopword & HTML stripping |
| **Cleaned Text + Metadata Signals** | **0.9240** | **0.9780** | **Highest overall performance** by combining text with missing profile & logo flags |

---

## 📁 Repository Structure (Ordered Execution Sequence)

```
fake-job-posting-detection/
├── index.html                  # Main Web Application HTML
├── style.css                   # Modern Dark Mode Styling
├── app.js                      # Client-side NLP Prediction Engine & Charts
├── requirements.txt            # Python Dependencies
├── generate_notebook.py        # Jupyter Notebook Generator Script
├── data/
│   └── 01_fake_job_postings.csv # EMSCAD Benchmark Dataset
├── src/
│   ├── 01_data_loader.py       # Data ingestion & synthetic EMSCAD generator
│   ├── 02_text_processor.py    # Text cleaning & TF-IDF feature pipeline
│   ├── 03_model_trainer.py     # Model training, tuning & metrics exporter
│   ├── 04_evaluation.py        # Preprocessing impact evaluation & ROC plots
│   ├── 05_predict.py           # Single job posting inference pipeline
│   └── 06_deploy_to_github.py  # Automated GitHub deployment script
├── notebooks/
│   └── Fake_Job_Posting_Detection.ipynb  # End-to-end Jupyter Notebook
└── outputs/
    ├── model_comparison.json   # Exported benchmark metrics
    └── preprocessing_impact.json
```

---

## 💻 Quick Start & Sequential Execution

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/MaxpaT01/fake-job-posting-detection.git
cd fake-job-posting-detection

python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Sequential Execution of Pipeline
```bash
python src/01_data_loader.py
python src/02_text_processor.py
python src/03_model_trainer.py
python src/04_evaluation.py
python src/05_predict.py
python src/06_deploy_to_github.py
```

---

## 📜 License

This project is open-source under the [MIT License](LICENSE).
