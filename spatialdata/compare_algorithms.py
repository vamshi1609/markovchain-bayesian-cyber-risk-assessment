#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import io

# Fix encoding for Windows Command Prompt
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spatialdata.settings')

import django
django.setup()

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load cyber risk training dataset
df = pd.read_csv('dataset/ml_cyber_risk_training.csv')
print(f"[DATA] Dataset loaded: {len(df)} rows, {len(df.columns)} columns\n")

# Feature columns
feature_cols = ['uptime_percent', 'patch_level', 'vulnerabilities_unpatched', 
               'response_time_sec', 'attack_frequency_per_week', 
               'avg_time_to_compromise_hours', 'daily_risk_score']
target_col = 'risk_category'

# Extract X and y
X = df[feature_cols].fillna(0)
y = df[target_col]

print(f"Features: {feature_cols}")
print(f"Target: {target_col}")
print(f"Classes: {y.unique()}\n")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(f"Training set: {len(X_train)} samples, Test set: {len(X_test)} samples\n")

# Scale features for better convergence
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train models
models = {}

# 1. Decision Tree
print("[1] Training Decision Tree...")
dt = DecisionTreeClassifier(max_depth=5, random_state=42)
dt.fit(X_train, y_train)
dt_pred = dt.predict(X_test)
models['DecisionTree'] = {
    'accuracy': accuracy_score(y_test, dt_pred),
    'precision': precision_score(y_test, dt_pred, average='weighted', zero_division=0),
    'recall': recall_score(y_test, dt_pred, average='weighted', zero_division=0),
    'f1': f1_score(y_test, dt_pred, average='weighted', zero_division=0)
}
print(f"    Accuracy: {models['DecisionTree']['accuracy']:.4f}")
print(f"    Precision: {models['DecisionTree']['precision']:.4f}")
print(f"    Recall: {models['DecisionTree']['recall']:.4f}")
print(f"    F1 Score: {models['DecisionTree']['f1']:.4f}\n")

# 2. Naive Bayes
print("[2] Training Naive Bayes (Gaussian)...")
nb = GaussianNB()
nb.fit(X_train, y_train)
nb_pred = nb.predict(X_test)
models['NaiveBayes'] = {
    'accuracy': accuracy_score(y_test, nb_pred),
    'precision': precision_score(y_test, nb_pred, average='weighted', zero_division=0),
    'recall': recall_score(y_test, nb_pred, average='weighted', zero_division=0),
    'f1': f1_score(y_test, nb_pred, average='weighted', zero_division=0)
}
print(f"    Accuracy: {models['NaiveBayes']['accuracy']:.4f}")
print(f"    Precision: {models['NaiveBayes']['precision']:.4f}")
print(f"    Recall: {models['NaiveBayes']['recall']:.4f}")
print(f"    F1 Score: {models['NaiveBayes']['f1']:.4f}\n")

# 3. Logistic Regression
print("[3] Training Logistic Regression...")
lr = LogisticRegression(max_iter=1000, random_state=42, solver='lbfgs')
lr.fit(X_train_scaled, y_train)
lr_pred = lr.predict(X_test_scaled)
models['LogisticRegression'] = {
    'accuracy': accuracy_score(y_test, lr_pred),
    'precision': precision_score(y_test, lr_pred, average='weighted', zero_division=0),
    'recall': recall_score(y_test, lr_pred, average='weighted', zero_division=0),
    'f1': f1_score(y_test, lr_pred, average='weighted', zero_division=0)
}
print(f"    Accuracy: {models['LogisticRegression']['accuracy']:.4f}")
print(f"    Precision: {models['LogisticRegression']['precision']:.4f}")
print(f"    Recall: {models['LogisticRegression']['recall']:.4f}")
print(f"    F1 Score: {models['LogisticRegression']['f1']:.4f}\n")

# 4. Random Forest
print("[4] Training Random Forest...")
rf = RandomForestClassifier(n_estimators=10, max_depth=5, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
models['RandomForest'] = {
    'accuracy': accuracy_score(y_test, rf_pred),
    'precision': precision_score(y_test, rf_pred, average='weighted', zero_division=0),
    'recall': recall_score(y_test, rf_pred, average='weighted', zero_division=0),
    'f1': f1_score(y_test, rf_pred, average='weighted', zero_division=0)
}
print(f"    Accuracy: {models['RandomForest']['accuracy']:.4f}")
print(f"    Precision: {models['RandomForest']['precision']:.4f}")
print(f"    Recall: {models['RandomForest']['recall']:.4f}")
print(f"    F1 Score: {models['RandomForest']['f1']:.4f}\n")

# Display comparison
print("=" * 70)
print("CYBER RISK ML MODEL COMPARISON SUMMARY")
print("=" * 70)
print(f"{'Model':<25} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
print("-" * 70)

for model_name in sorted(models.keys(), key=lambda x: models[x]['accuracy'], reverse=True):
    metrics = models[model_name]
    print(f"{model_name:<25} {metrics['accuracy']:<12.4f} {metrics['precision']:<12.4f} {metrics['recall']:<12.4f} {metrics['f1']:<12.4f}")

print("=" * 70)

# Save to database
from adminapp.models import Dataset

data = Dataset.objects.filter(data_set='ml_cyber_risk_training.csv').order_by('-data_id').first()
if not data:
    data = Dataset.objects.create(data_set='ml_cyber_risk_training.csv')

data.dt_algo = 'DecisionTreeClassifier'
data.dt_Accuracy = models['DecisionTree']['accuracy']
data.dt_Precision = models['DecisionTree']['precision']
data.dt_Recall = models['DecisionTree']['recall']
data.dt_F1_Score = models['DecisionTree']['f1']

data.nb_algo = 'GaussianNB'
data.nb_Accuracy = models['NaiveBayes']['accuracy']
data.nb_Precision = models['NaiveBayes']['precision']
data.nb_Recall = models['NaiveBayes']['recall']
data.nb_F1_Score = models['NaiveBayes']['f1']

data.lr_algo = 'LogisticRegression'
data.lr_Accuracy = models['LogisticRegression']['accuracy']
data.lr_Precision = models['LogisticRegression']['precision']
data.lr_Recall = models['LogisticRegression']['recall']
data.lr_F1_Score = models['LogisticRegression']['f1']

data.rf_algo = 'RandomForestClassifier'
data.rf_Accuracy = models['RandomForest']['accuracy']
data.rf_Precision = models['RandomForest']['precision']
data.rf_Recall = models['RandomForest']['recall']
data.rf_F1_Score = models['RandomForest']['f1']

data.save()

print(f"\n[SUCCESS] Results saved to database (Dataset ID: {data.data_id})")
print(f"[SUCCESS] All 4 ML models trained successfully on cyber risk data!")
print(f"\nView results at: http://127.0.0.1:8000/admin-algocomp\n")
