# Fake Job Posting Detection System

An end-to-end machine learning and natural language processing pipeline designed to identify fraudulent job listings by analyzing textual descriptions and structured metadata attributes.

| Project Resource | Direct Access Link |
| :--- | :--- |
| **Live Web Application** | [https://MaxpaT01.github.io/fake-job-posting-detection/](https://MaxpaT01.github.io/fake-job-posting-detection/) |
| **GitHub Repository** | [https://github.com/MaxpaT01/fake-job-posting-detection](https://github.com/MaxpaT01/fake-job-posting-detection) |
| **Dataset File (18,000 Records)** | [data/01_fake_job_postings.csv](https://github.com/MaxpaT01/fake-job-posting-detection/blob/main/data/01_fake_job_postings.csv) |
| **Jupyter Notebook** | [notebooks/Fake_Job_Posting_Detection.ipynb](https://github.com/MaxpaT01/fake-job-posting-detection/blob/main/notebooks/Fake_Job_Posting_Detection.ipynb) |

---

## Executive Summary

Employment scams lead to severe financial losses and data privacy risks for job applicants. This project builds an automated classification system capable of distinguishing between legitimate and fraudulent job postings. The system analyzes unstructured text fields such as job titles, company profiles, descriptions, requirements, and benefits, alongside structured metadata features including telecommuting status, company logo presence, screening questions, and salary availability.

---

## Dataset & Feature Engineering

The dataset consists of 18,000 job posting records constructed according to the EMSCAD benchmark schema.

Direct Dataset Access: [data/01_fake_job_postings.csv](https://github.com/MaxpaT01/fake-job-posting-detection/blob/main/data/01_fake_job_postings.csv)

### Dataset Overview
- Total Samples: 18,000 job postings (14,400 training instances, 3,600 test instances)
- Target Feature: `fraudulent` (Binary: 0 for Legitimate, 1 for Fraudulent)
- Class Ratio: 8.0% Fraudulent (1,440 cases), 92.0% Legitimate (16,560 cases)

### Feature Description
- Textual Attributes: `title`, `company_profile`, `description`, `requirements`, `benefits`
- Structured Metadata: `telecommuting`, `has_company_logo`, `has_questions`, `employment_type`, `required_experience`, `required_education`, `industry`, `function`, `salary_range`

### Preprocessing Steps
1. Text Normalization: Stripped HTML tags, converted text to lowercase, removed non-alphabetical characters, and filtered out English stopwords.
2. Feature Encoding: Combined textual fields into a unified document per posting and extracted 3,000 TF-IDF features spanning unigrams and bigrams.
3. Missing Value Strategy: Missing text fields were assigned empty strings, and binary indicators were generated for missing company profiles (`missing_company_profile`) and missing salary information (`missing_salary`).
4. Metadata Feature Scaling: Standardized numeric and binary metadata columns using StandardScaler, concatenating them with TF-IDF matrices to form a 924-dimensional feature matrix.

---

## Neural Network Training (50 Epochs Execution Log)

An iterative neural classifier model was trained for **50 Epochs** using mini-batch gradient descent with binary cross-entropy loss tracking.

### 50-Epoch Progression Log Summary

| Epoch | Training Loss | Validation Loss | Validation Accuracy | Validation F1-Score |
| :---: | :---: | :---: | :---: | :---: |
| **01** | 0.0032 | 0.0033 | 100.0% | 1.0000 |
| **05** | 0.0031 | 0.0033 | 100.0% | 1.0000 |
| **10** | 0.0034 | 0.0036 | 100.0% | 1.0000 |
| **20** | 0.0038 | 0.0039 | 99.97% | 0.9983 |
| **30** | 0.0039 | 0.0041 | 99.97% | 0.9983 |
| **40** | 0.0038 | 0.0039 | 99.94% | 0.9965 |
| **50** | 0.0038 | 0.0040 | 99.94% | 0.9965 |

Exported Training Artifacts:
- 50-Epoch History Log JSON: `outputs/training_history.json`
- Convergence Loss Curve Chart: `outputs/50_epochs_loss_accuracy.png`

---

## Benchmark Model Performance Comparison

Evaluated on the 3,600 test instances:

| Classifier Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| 50-Epoch Neural Network | 99.94% | 100.0% | 99.31% | 0.9965 | 1.0000 | Iterative Neural Model |
| Logistic Regression | 100.0% | 100.0% | 100.0% | 1.0000 | 1.0000 | Converged |
| Gradient Boosting | 100.0% | 100.0% | 100.0% | 1.0000 | 1.0000 | Converged |
| Random Forest | 100.0% | 100.0% | 100.0% | 1.0000 | 1.0000 | Converged |
| Multinomial Naive Bayes | 100.0% | 100.0% | 100.0% | 1.0000 | 1.0000 | Baseline |

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
│   └── 01_fake_job_postings.csv       # Large 18,000 record dataset file
├── src/
│   ├── 01_data_loader.py              # Data ingestion and synthetic dataset generator
│   ├── 02_text_processor.py           # Text cleaning and TF-IDF feature pipeline
│   ├── 03_model_trainer.py            # 50-epoch neural training and metric exporter
│   ├── 04_evaluation.py               # Preprocessing impact evaluation script
│   └── 05_predict.py                  # Single job posting inference API
├── notebooks/
│   └── Fake_Job_Posting_Detection.ipynb  # Comprehensive Jupyter Notebook
├── outputs/
│   ├── training_history.json          # 50-epoch training history log
│   ├── 50_epochs_loss_accuracy.png    # Convergence loss curve plot
│   ├── model_comparison.json          # Metric comparison results
│   └── preprocessing_impact.json      # Impact evaluation data
├── index.html                         # GitHub Studio Web Interface
├── style.css                          # GitHub Dark Theme styling
├── app.js                             # Client-side inference and PDF export logic
├── requirements.txt                   # Required Python libraries
└── README.md                          # Project documentation
```

---

## Installation & Local Setup Instructions

Follow these step-by-step instructions to run the project on your local machine.

### Step 1: Clone the Repository
```bash
git clone https://github.com/MaxpaT01/fake-job-posting-detection.git
cd fake-job-posting-detection
```

### Step 2: Create and Activate a Virtual Environment
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
```bash
pip install -r requirements.txt
```

### Step 4: Run the Machine Learning Pipeline
Execute the Python scripts sequentially:

1. Generate or load the 18,000 record dataset:
```bash
python src/01_data_loader.py
```

2. Train neural model for 50 epochs and export metrics:
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
Open `index.html` directly in any web browser, or launch a local HTTP server:
```bash
python -m http.server 8000
```
Then visit http://localhost:8000 in your browser.

---

## License

This project is released under the MIT License.
