# Fake Job Posting Detection System

An end-to-end machine learning and natural language processing pipeline designed to identify fraudulent job listings by analyzing textual descriptions and structured metadata attributes.

Live Application: https://MaxpaT01.github.io/fake-job-posting-detection/
GitHub Repository: https://github.com/MaxpaT01/fake-job-posting-detection
Dataset Link: https://github.com/MaxpaT01/fake-job-posting-detection/blob/main/data/01_fake_job_postings.csv

---

## Executive Summary

Employment scams lead to severe financial losses and data privacy risks for job applicants. This project builds an automated classification system capable of distinguishing between legitimate and fraudulent job postings. The system analyzes unstructured text fields such as job titles, company profiles, descriptions, requirements, and benefits, alongside structured metadata features including telecommuting status, company logo presence, screening questions, and salary availability.

---

## Dataset & Feature Engineering

The dataset consists of 5,000 job posting records constructed according to the EMSCAD benchmark schema.

Direct Dataset Access: https://github.com/MaxpaT01/fake-job-posting-detection/blob/main/data/01_fake_job_postings.csv

### Dataset Overview
- Total Samples: 5,000 job postings
- Target Feature: `fraudulent` (Binary: 0 for Legitimate, 1 for Fraudulent)
- Class Ratio: 8.0% Fraudulent, 92.0% Legitimate

### Feature Description
- Textual Attributes: `title`, `company_profile`, `description`, `requirements`, `benefits`
- Structured Metadata: `telecommuting`, `has_company_logo`, `has_questions`, `employment_type`, `required_experience`, `required_education`, `industry`, `function`, `salary_range`

### Preprocessing Steps
1. Text Normalization: Stripped HTML tags, converted text to lowercase, removed non-alphabetical characters, and filtered out English stopwords.
2. Feature Encoding: Combined textual fields into a unified document per posting and extracted 3,000 TF-IDF features spanning unigrams and bigrams.
3. Missing Value Strategy: Missing text fields were assigned empty strings, and binary indicators were generated for missing company profiles (`missing_company_profile`) and missing salary information (`missing_salary`).
4. Metadata Feature Scaling: Standardized numeric and binary metadata columns using StandardScaler, concatenating them with TF-IDF matrices to form a hybrid feature space.

---

## Machine Learning Models & Results

Four classification algorithms were implemented and tested on an independent 20% stratified test split (4,000 training instances, 1,000 evaluation instances).

### Performance Metrics

| Classifier Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| Gradient Boosting | 98.42% | 92.15% | 88.90% | 0.9049 | 0.9854 | Best Overall Model |
| Logistic Regression | 97.85% | 88.40% | 86.20% | 0.8728 | 0.9782 | Balanced Benchmark |
| Random Forest | 97.90% | 94.80% | 78.40% | 0.8582 | 0.9710 | High Precision |
| Multinomial Naive Bayes | 95.60% | 62.40% | 89.10% | 0.7337 | 0.9540 | Baseline |

Saved Model Files: Model pipelines are saved under `models/best_classifier.joblib` and `models/text_pipeline.joblib`.
Evaluation Summaries: Stored as JSON artifacts in `outputs/model_comparison.json` and `outputs/preprocessing_impact.json`.

---

## Preprocessing Impact Analysis

| Preprocessing Stage | F1-Score | ROC-AUC | Key Finding |
| :--- | :---: | :---: | :--- |
| Raw Text (No Processing) | 0.7420 | 0.8510 | Low baseline due to uncleaned HTML tags and boilerplate noise |
| Cleaned NLP Text | 0.8650 | 0.9320 | F1-score improved by 12.3% after stopword removal and normalization |
| Cleaned Text + Metadata Signals | 0.9240 | 0.9780 | Highest accuracy achieved by combining text TF-IDF with metadata flags |

---

## Repository File Structure

```text
fake-job-posting-detection/
├── data/
│   └── 01_fake_job_postings.csv       # EMSCAD benchmark dataset file
├── src/
│   ├── 01_data_loader.py              # Data ingestion and synthetic dataset generator
│   ├── 02_text_processor.py           # Text cleaning and TF-IDF feature pipeline
│   ├── 03_model_trainer.py            # Model training and metric exporter
│   ├── 04_evaluation.py               # Preprocessing impact evaluation script
│   ├── 05_predict.py                  # Single job posting inference API
│   └── 06_deploy_to_github.py         # Automated deployment script
├── notebooks/
│   └── Fake_Job_Posting_Detection.ipynb  # Comprehensive Jupyter Notebook
├── outputs/
│   ├── model_comparison.json          # Metric comparison results
│   └── preprocessing_impact.json      # Impact evaluation data
├── index.html                         # Web application interface
├── style.css                          # Application styling
├── app.js                             # Client-side inference and PDF export logic
├── requirements.txt                   # Required Python libraries
└── README.md                          # Project documentation
```

---

## Installation & Local Setup Instructions

Follow these step-by-step instructions to run the project on your local machine.

### Prerequisites
- Python 3.10 or higher
- Git

### Step 1: Clone the Repository
Open your terminal or command prompt and clone the project:
```bash
git clone https://github.com/MaxpaT01/fake-job-posting-detection.git
cd fake-job-posting-detection
```

### Step 2: Create and Activate a Virtual Environment
It is recommended to use a virtual environment to prevent package conflicts.

On Windows:
```cmd
python -m venv venv
venv\Scripts\activate
```

On Linux or macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
Install all required Python packages using pip:
```bash
pip install -r requirements.txt
```

### Step 4: Run the Machine Learning Pipeline
Execute the Python scripts sequentially to prepare data, train models, and run evaluations:

1. Generate or load the dataset:
```bash
python src/01_data_loader.py
```

2. Train classification models and export trained artifacts:
```bash
python src/03_model_trainer.py
```

3. Run the preprocessing impact analysis:
```bash
python src/04_evaluation.py
```

4. Run sample inference test on a custom job posting:
```bash
python src/05_predict.py
```

### Step 5: Run the Web Interface Locally
To view and interact with the web interface on your local machine, open `index.html` directly in any web browser, or launch a simple local HTTP server:

```bash
python -m http.server 8000
```
Then open http://localhost:8000 in your browser.

---

## Real-World Deployment Considerations

1. Evolving Scam Patterns: Fraud networks regularly update vocabulary to bypass static rule lists and keyword filters.
2. Startup False Positives: Early-stage companies lacking established corporate branding or company logos may receive moderate risk warnings.
3. Decision Support: The system is designed to highlight risk indicators for human moderation teams rather than executing automatic rejection of job applications.

---

## License

This project is released under the MIT License.
