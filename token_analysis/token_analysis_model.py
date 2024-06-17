# analysis/token_analysis_model.py

import torch
from transformers import BertTokenizer, BertModel
from transformers import pipeline
from sklearn.linear_model import LogisticRegression
import numpy as np
import pickle
import pandas as pd

class TokenAnalysisModel:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        self.sentiment_pipeline = pipeline('sentiment-analysis')
        self.ner_pipeline = pipeline('ner')

    def extract_features_whitepaper(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        outputs = self.model(**inputs)
        summary = outputs.last_hidden_state.mean(dim=1).detach().numpy()
        sentiment = self.sentiment_pipelpipine(text)
        return np.concatenate((summary, np.array([sentiment[0]['score']])))
    
    def extract_features_team(self, text):
        ner_results = self.ner_pipeline(text)
        entities = [result['word'] for result in ner_results]
        entity_embedding = self.model(**self.tokenizer(' '.join(entities), return_tensors='pt'))['last_hidden_state'].mean(dim=1).detach().numpy()
        return entity_embedding

    def extract_features_technology(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).detach().numpy()
    
    def extract_features_partnerships(self, text):
        sentiment = self.sentiment_pipeline(text)
        ner_results = self.ner_pipeline(text)
        entities = [result['word'] for result in ner_results if result['entity'] == 'ORG']
        entity_embedding = self.model(**self.tokenizer(' '.join(entities), return_tensors='pt'))['last_hidden_state'].mean(dim=1).detach().numpy()
        return np.concatenate((entity_embedding, np.array([sentiment[0]['score']])))
    
    def extract_features_roadmap(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        outputs = self.model(**inputs)
        summary = outputs.last_hidden_state.mean(dim=1).detach().numpy()
        sentiment = self.sentiment_pipeline(text)
        return np.concatenate((summary, np.array([sentiment[0]['score']])))
    
    def extract_features(self, text, aspect):
        if aspect == 'whitepaper':
            return self.extract_features_whitepaper(text)
        elif aspect == 'team':
            return self.extract_features_team(text)
        elif aspect == 'technology':
            return self.extract_features_technology(text)
        elif aspect == 'partnerships':
            return self.extract_features_partnerships(text)
        elif aspect == 'roadmap':
            return self.extract_features_roadmap(text)
        else:
            return np.zeros((1, 768))  # Default feature vector for unknown aspects

    def train(self, data, labels, aspect):
        features = [self.extract_features(text, aspect) for text in data]
        X = np.vstack(features)
        self.clf = LogisticRegression()
        self.clf.fit(X, labels)
        with open(f'{aspect}_clf.pkl', 'wb') as f:
            pickle.dump(self.clf, f)

    def predict(self, documents, aspect):
        features = [self.extract_features(text, aspect) for text in documents]
        X = np.vstack(features)
        with open(f'{aspect}_clf.pkl', 'rb') as f:
            clf = pickle.load(f)
        predictions = clf.predict(X)
        return predictions
