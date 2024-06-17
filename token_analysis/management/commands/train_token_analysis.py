# token_analysis/management/commands/train_token_analysis.py

import pandas as pd
import torch
from transformers import BertTokenizer, BertModel
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import pickle
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Train the token analysis model'

    def handle(self, *args, **kwargs):
        # Load and preprocess data from CSV file
        csv_file = 'extracted_whitepapers.csv'
        df = pd.read_csv(csv_file)

        # Manual labeling for demonstration (replace with real labels)
        df['label'] = np.random.randint(0, 2, df.shape[0])  # Replace with real labels

        X = df['text']
        y = df['label']

        # Load BERT tokenizer and model
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        model = BertModel.from_pretrained('bert-base-uncased')

        # Tokenize data
        def tokenize(text):
            inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
            outputs = model(**inputs)
            return outputs.last_hidden_state.mean(dim=1).detach().numpy()

        X = X.apply(tokenize)
        X = np.vstack(X.values)

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a simple logistic regression model
        clf = LogisticRegression(max_iter=1000)  # Increase max_iter to ensure convergence
        clf.fit(X_train, y_train)

        # Evaluate the model
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        self.stdout.write(self.style.SUCCESS(f'Accuracy: {accuracy * 100:.2f}%'))

        # Save the model
        with open('token_analysis_model.pkl', 'wb') as f:
            pickle.dump(clf, f)

        self.stdout.write(self.style.SUCCESS('Model training completed and saved as token_analysis_model.pkl'))
