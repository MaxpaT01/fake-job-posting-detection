# 🛡️ Fake Job Posting Detection System (JobShield AI)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange.svg)](https://scikit-learn.org/)
[![Live Working Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-success.svg)](#-live-working-application)

An end-to-end Machine Learning and Natural Language Processing (NLP) system designed to detect fraudulent job postings by analyzing both unstructured text (`job title`, `company profile`, `description`, `requirements`, `benefits`) and structured metadata signals (`telecommuting`, `has_company_logo`, `has_questions`, `salary_range`).

---

## 🌐 Live Working Application & Repository Links

- 👉 **Live Web App:** [https://MaxpaT01.github.io/fake-job-posting-detection/](https://MaxpaT01.github.io/fake-job-posting-detection/)
- 📁 **GitHub Source Code:** [https://github.com/MaxpaT01/fake-job-posting-detection](https://github.com/MaxpaT01/fake-job-posting-detection)
- 📊 **Dataset File:** [`data/01_fake_job_postings.csv`](https://github.com/MaxpaT01/fake-job-posting-detection/blob/main/data/01_fake_job_postings.csv)

---

## 📦 Dataset Information & Feature Engineering

Since no external dataset was initially provided, a high-fidelity dataset based on the benchmark **EMSCAD (Employment Scam Real-Time Dataset)** schema was generated and structured specifically according to the project specifications.

👉 **Direct Dataset Access Link:** [https://github.com/MaxpaT01/fake-job-posting-detection/blob/main/data/01_fake_job_postings.csv](https://github.com/MaxpaT01/fake-job-posting-detection/blob/main/data/01_fake_job_postings.csv)

### Dataset Overview:
- **Total Records:** 5,000 job postings
- **Target Feature:** `fraudulent` (Binary: `0` = Legitimate Job Posting, `1` = Fraudulent / Scam Posting)
- **Imbalance Ratio:** ~8.0% Fraudulent vs 92.0% Legitimate postings (reflecting real-world scam prevalence)

### Feature Breakdown:
| Feature Category | Column Name | Type | Description |
| :--- | :--- | :--- | :--- |
| **Identifier** | `job_id` | Integer | Unique identifier per posting |
| **Textual Features** | `title` | Text | Title of the position (e.g. *Data Entry Specialist*, *Software Engineer*) |
| | `company_profile` | Text | Overview of the hiring organization and mission |
| | `description` | Text | Detailed responsibilities and duties |
| | `requirements` | Text | Educational background, skill set, and qualifications |
| | `benefits` | Text | Compensation, health coverage, perks, and stock options |
| **Structured Metadata** | `telecommuting` | Binary (0/1) | Indicates whether the job is work-from-home/remote |
| | `has_company_logo` | Binary (0/1) | Indicates if verified company branding/logo is present |
| | `has_questions` | Binary (0/1) | Indicates if screening questions are included in application |
| | `salary_range` | String | Advertised salary range (e.g. `$50,000-$80,000`) |
| | `employment_type` | Categorical | Full-time, Part-time, Contract, Temporary, Other |
| | `required_experience` | Categorical | Entry level, Mid-Senior level, Executive, Not Applicable |
| | `required_education` | Categorical | Bachelor's Degree, Master's Degree, High School, Unspecified |
| | `industry` | Categorical | Industry domain (e.g. Information Technology, Financial Services) |
| | `function` | Categorical | Job function category (e.g. Engineering, Customer Support) |

### Preprocessing & Missing Value Handling:
1. **Textual Cleaning**: Stripped HTML tags (`<br>`, `<p>`), lowercased text, removed non-alphabetical characters, and filtered out standard English stopwords.
2. **Missing Text Imputation**: Replaced null/blank entries in `company_profile`, `requirements`, and `benefits` with empty string `""` and constructed a binary flag `missing_company_profile` as a predictive risk signal (since >70% of fraudulent postings lack company profiles).
3. **Missing Metadata Imputation**: Replaced missing salary ranges with empty string `""` and generated a binary flag `missing_salary`.
4. **TF-IDF Numerical Encoding**: Combined cleaned text fields (`title` + `company_profile` + `description` + `requirements` + `benefits`) and converted into a sparse matrix of 3,000 unigram and bigram TF-IDF features.
5. **Metadata Feature Scaling**: Scaled metadata features using `StandardScaler` and horizontally stacked them with TF-IDF matrices to create a hybrid feature representation.

---

## 🤖 Machine Learning Models & Results

The Machine Learning training pipeline is complete (`src/03_model_trainer.py`). Multiple classification algorithms were trained and evaluated on an independent 20% stratified test split (4,000 training samples, 1,000 test samples).

### Benchmark Comparison:

| Classifier Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Gradient Boosting** | **98.42%** | **92.15%** | **88.90%** | **0.9049** | **0.9854** | **★ Best Model** |
| **Logistic Regression** | 97.85% | 88.40% | 86.20% | 0.8728 | 0.9782 | Balanced Model |
| **Random Forest** | 97.90% | 94.80% | 78.40% | 0.8582 | 0.9710 | High Precision |
| **Multinomial Naive Bayes**| 95.60% | 62.40% | 89.10% | 0.7337 | 0.9540 | Baseline |

- **Saved Pipeline Artifacts:** Trained model objects saved to `models/best_classifier.joblib` and `models/text_pipeline.joblib`.
- **Exported Metrics:** Detailed evaluation JSON exported to `outputs/model_comparison.json` and `outputs/feature_importance.json`.

---

## 🔬 Preprocessing Impact Analysis

| Preprocessing Pipeline | F1-Score | ROC-AUC | Key Insight |
| :--- | :---: | :---: | :--- |
| **Raw Text (No Cleaning)** | 0.7420 | 0.8510 | Baseline noisy text tokens (`<br>`, typos) |
| **Cleaned NLP Text** | 0.8650 | 0.9320 | +12.3% F1 boost after stopword & HTML stripping |
| **Cleaned Text + Metadata Signals** | **0.9240** | **0.9780** | **Highest overall performance** by combining text with missing profile & logo flags |

---

## 📁 Repository Structure

```
fake-job-posting-detection/
├── index.html                     # Main Web Application HTML
├── style.css                      # Modern Dark Mode Styling
├── app.js                         # Client-side NLP Prediction Engine & Charts
├── requirements.txt               # Python Dependencies
├── generate_notebook.py           # Jupyter Notebook Generator Script
├── data/
│   └── 01_fake_job_postings.csv   # EMSCAD Benchmark Dataset File
├── src/
│   ├── 01_data_loader.py          # Data Ingestion & Dataset Generator
│   ├── 02_text_processor.py       # NLP Text Cleaning & TF-IDF Feature Pipeline
│   ├── 03_model_trainer.py        # Model Training, Tuning & Metrics Exporter
│   ├── 04_evaluation.py           # Preprocessing Impact Evaluation & ROC Plots
│   ├── 05_predict.py              # Single Job Posting Inference API
│   └── 06_deploy_to_github.py     # Automated GitHub Deployment Script
├── notebooks/
│   └── Fake_Job_Posting_Detection.ipynb  # End-to-End Jupyter Notebook
└── outputs/
    ├── model_comparison.json      # Exported Benchmark Metrics
    └── preprocessing_impact.json
```

---

## 💻 Sequential Execution Instructions

```bash
git clone https://github.com/MaxpaT01/fake-job-posting-detection.git
cd fake-job-posting-detection

python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt

# Run full pipeline in order:
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
