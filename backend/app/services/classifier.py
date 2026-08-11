import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from typing import Dict, List, Tuple, Any

# Path to the data
DATA_PATH = "H:/intern/project/nyaya-ai/data/demo/legal_cases.csv"

class LegalClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.classifier = LogisticRegression(max_iter=200, C=1.0)
        self.is_trained = False
        self.categories = []
        
    def train(self, filepath: str = DATA_PATH):
        """Train the classifier using the synthetic dataset."""
        try:
            if not os.path.exists(filepath):
                print(f"Data file not found at {filepath}. Skipping training.")
                return False
                
            df = pd.read_csv(filepath)
            if df.empty or 'facts' not in df.columns or 'case_type' not in df.columns:
                print("Data file is empty or missing required columns. Skipping training.")
                return False
                
            X = df['facts'].fillna("")
            y = df['case_type'].fillna("Civil Law")
            
            # Record category names
            self.categories = list(y.unique())
            
            # Fit TF-IDF Vectorizer
            X_vec = self.vectorizer.fit_transform(X)
            
            # Fit Logistic Regression Classifier
            self.classifier.fit(X_vec, y)
            
            self.is_trained = True
            print(f"LegalClassifier successfully trained on {len(X)} cases. Categories: {self.categories}")
            return True
        except Exception as e:
            print(f"Error training LegalClassifier: {str(e)}")
            return False

    def predict(self, text: str) -> List[Dict[str, Any]]:
        """
        Predict case categories and confidence scores.
        Returns a sorted list of categories with probabilities.
        """
        # Fallback keyword classification if model is not trained
        if not self.is_trained:
            return self._predict_fallback(text)
            
        try:
            # Transform text
            text_vec = self.vectorizer.transform([text])
            
            # Get class probabilities
            probs = self.classifier.predict_proba(text_vec)[0]
            
            # Sort categories by probability
            results = []
            for cat, prob in zip(self.classifier.classes_, probs):
                results.append({
                    "category": str(cat),
                    "confidence": float(round(prob * 100, 2))
                })
                
            results = sorted(results, key=lambda x: x["confidence"], reverse=True)
            return results[:3]  # Return top 3 categories
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return self._predict_fallback(text)

    def _predict_fallback(self, text: str) -> List[Dict[str, Any]]:
        """Fallback rule-based keyword classifier if ML training fails."""
        text_lower = text.lower()
        scores = {
            "Landlord/Tenant disputes": 0.0,
            "Cheque/payment disputes": 0.0,
            "Cybercrime": 0.0,
            "Contract Law": 0.0,
            "Family Law": 0.0,
            "Criminal Law": 0.0,
            "Property Law": 0.0,
            "Consumer Law": 0.0
        }
        
        # Rule-based score calculation
        if "tenant" in text_lower or "landlord" in text_lower or "rent" in text_lower or "deposit" in text_lower or "lease" in text_lower:
            scores["Landlord/Tenant disputes"] += 0.8
            scores["Property Law"] += 0.4
        if "cheque" in text_lower or "bounce" in text_lower or "dishonour" in text_lower or "banker" in text_lower:
            scores["Cheque/payment disputes"] += 0.9
        if "hacked" in text_lower or "otp" in text_lower or "cyber" in text_lower or "online" in text_lower or "phishing" in text_lower or "card" in text_lower:
            scores["Cybercrime"] += 0.8
        if "agreement" in text_lower or "breach" in text_lower or "signed" in text_lower or "contract" in text_lower or "invoice" in text_lower:
            scores["Contract Law"] += 0.7
        if "wife" in text_lower or "husband" in text_lower or "maintenance" in text_lower or "marriage" in text_lower or "abuse" in text_lower or "domestic" in text_lower:
            scores["Family Law"] += 0.8
        if "murder" in text_lower or "ipc" in text_lower or "theft" in text_lower or "police" in text_lower or "arrest" in text_lower or "bail" in text_lower:
            scores["Criminal Law"] += 0.7
            
        # Normalize scores to look like percentages
        total = sum(scores.values())
        if total == 0:
            return [{"category": "Civil Law", "confidence": 100.0}]
            
        results = []
        for cat, val in scores.items():
            if val > 0:
                results.append({
                    "category": cat,
                    "confidence": float(round((val / total) * 100, 2))
                })
                
        results = sorted(results, key=lambda x: x["confidence"], reverse=True)
        return results[:3]

# Create global instance
classifier = LegalClassifier()
# Train immediately upon importing
classifier.train()
