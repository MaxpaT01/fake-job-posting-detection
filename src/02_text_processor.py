import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from scipy.sparse import hstack, csr_matrix

STOPWORDS = set([
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
    "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't",
    "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have",
    "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself",
    "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is",
    "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
    "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should",
    "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them",
    "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't",
    "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "whatever", "when",
    "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with",
    "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves"
])

def clean_text(text):
    if not isinstance(text, str) or pd.isna(text):
        return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = [w for w in text.split() if w not in STOPWORDS and len(w) > 1]
    return " ".join(tokens)

def prepare_combined_text(df):
    df = df.copy()
    text_cols = ["title", "company_profile", "description", "requirements", "benefits"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str)
        else:
            df[col] = ""
    
    combined = (
        df["title"] + " " + 
        df["company_profile"] + " " + 
        df["description"] + " " + 
        df["requirements"] + " " + 
        df["benefits"]
    )
    return combined.apply(clean_text)

class TextMetadataPipeline:
    def __init__(self, max_tfidf_features=3000, use_metadata=True):
        self.max_tfidf_features = max_tfidf_features
        self.use_metadata = use_metadata
        self.tfidf_vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=self.max_tfidf_features,
            sublinear_tf=True
        )
        self.scaler = StandardScaler()
        
    def fit_transform(self, df):
        cleaned_text = prepare_combined_text(df)
        X_text = self.tfidf_vectorizer.fit_transform(cleaned_text)
        
        if not self.use_metadata:
            return X_text
            
        metadata_matrix = self._extract_metadata_matrix(df, is_fit=True)
        return hstack([X_text, metadata_matrix]).tocsr()
        
    def transform(self, df):
        cleaned_text = prepare_combined_text(df)
        X_text = self.tfidf_vectorizer.transform(cleaned_text)
        
        if not self.use_metadata:
            return X_text
            
        metadata_matrix = self._extract_metadata_matrix(df, is_fit=False)
        return hstack([X_text, metadata_matrix]).tocsr()

    def _extract_metadata_matrix(self, df, is_fit=False):
        telecommuting = df["telecommuting"].fillna(0).astype(float).values
        has_logo = df["has_company_logo"].fillna(0).astype(float).values
        has_questions = df["has_questions"].fillna(0).astype(float).values
        
        missing_profile = df["company_profile"].isna() | (df["company_profile"].astype(str).str.strip() == "")
        missing_profile = missing_profile.astype(float).values
        
        missing_salary = df["salary_range"].isna() | (df["salary_range"].astype(str).str.strip() == "")
        missing_salary = missing_salary.astype(float).values
        
        raw_meta = np.column_stack([
            telecommuting,
            has_logo,
            has_questions,
            missing_profile,
            missing_salary
        ])
        
        if is_fit:
            scaled_meta = self.scaler.fit_transform(raw_meta)
        else:
            scaled_meta = self.scaler.transform(raw_meta)
            
        return csr_matrix(scaled_meta)
