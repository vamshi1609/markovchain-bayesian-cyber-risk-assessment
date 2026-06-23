#!/usr/bin/env python
import os
import sys
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
print(f"📊 Dataset loaded: {len(df)} rows, {len(df.columns)} columns\n")

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

# Scale features for better convergence (especially for LogisticRegression)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train models
models = {}

# 1. Decision Tree (no scaling needed)
print("🌳 Training Decision Tree...")
dt = DecisionTreeClassifier(max_depth=5, random_state=42)
dt.fit(X_train, y_train)
dt_pred = dt.predict(X_test)
models['DecisionTree'] = {
    'accuracy': accuracy_score(y_test, dt_pred),
    'precision': precision_score(y_test, dt_pred, average='weighted', zero_division=0),
    'recall': recall_score(y_test, dt_pred, average='weighted', zero_division=0),
    'f1': f1_score(y_test, dt_pred, average='weighted', zero_division=0)
}
print(f"   Accuracy: {models['DecisionTree']['accuracy']:.4f}")
print(f"   Precision: {models['DecisionTree']['precision']:.4f}")
print(f"   Recall: {models['DecisionTree']['recall']:.4f}")
print(f"   F1 Score: {models['DecisionTree']['f1']:.4f}\n")

# 2. Naive Bayes (no scaling needed)
print("🎲 Training Naive Bayes (Gaussian)...")
nb = GaussianNB()
nb.fit(X_train, y_train)
nb_pred = nb.predict(X_test)
models['NaiveBayes'] = {
    'accuracy': accuracy_score(y_test, nb_pred),
    'precision': precision_score(y_test, nb_pred, average='weighted', zero_division=0),
    'recall': recall_score(y_test, nb_pred, average='weighted', zero_division=0),
    'f1': f1_score(y_test, nb_pred, average='weighted', zero_division=0)
}
print(f"   Accuracy: {models['NaiveBayes']['accuracy']:.4f}")
print(f"   Precision: {models['NaiveBayes']['precision']:.4f}")
print(f"   Recall: {models['NaiveBayes']['recall']:.4f}")
print(f"   F1 Score: {models['NaiveBayes']['f1']:.4f}\n")

# 3. Logistic Regression (using scaled features)
print("📈 Training Logistic Regression...")
lr = LogisticRegression(max_iter=1000, random_state=42, solver='lbfgs')
lr.fit(X_train_scaled, y_train)
lr_pred = lr.predict(X_test_scaled)
models['LogisticRegression'] = {
    'accuracy': accuracy_score(y_test, lr_pred),
    'precision': precision_score(y_test, lr_pred, average='weighted', zero_division=0),
    'recall': recall_score(y_test, lr_pred, average='weighted', zero_division=0),
    'f1': f1_score(y_test, lr_pred, average='weighted', zero_division=0)
}
print(f"   Accuracy: {models['LogisticRegression']['accuracy']:.4f}")
print(f"   Precision: {models['LogisticRegression']['precision']:.4f}")
print(f"   Recall: {models['LogisticRegression']['recall']:.4f}")
print(f"   F1 Score: {models['LogisticRegression']['f1']:.4f}\n")

# 4. Random Forest
print("🌲 Training Random Forest...")
rf = RandomForestClassifier(n_estimators=10, max_depth=5, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
models['RandomForest'] = {
    'accuracy': accuracy_score(y_test, rf_pred),
    'precision': precision_score(y_test, rf_pred, average='weighted', zero_division=0),
    'recall': recall_score(y_test, rf_pred, average='weighted', zero_division=0),
    'f1': f1_score(y_test, rf_pred, average='weighted', zero_division=0)
}
print(f"   Accuracy: {models['RandomForest']['accuracy']:.4f}")
print(f"   Precision: {models['RandomForest']['precision']:.4f}")
print(f"   Recall: {models['RandomForest']['recall']:.4f}")
print(f"   F1 Score: {models['RandomForest']['f1']:.4f}\n")

# Summary
print("\n" + "="*60)
print("📊 CYBER RISK ML MODEL COMPARISON SUMMARY")
print("="*60)
print(f"{'Model':<25} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
print("-"*60)
for name, metrics in models.items():
    print(f"{name:<25} {metrics['accuracy']:<12.4f} {metrics['precision']:<12.4f} {metrics['recall']:<12.4f} {metrics['f1']:<12.4f}")

# Store in database
from adminapp.models import Dataset

data = Dataset.objects.create(
    data_set='ml_cyber_risk_training.csv',
    dt_algo='DecisionTreeClassifier',
    dt_Accuracy=models['DecisionTree']['accuracy'],
    dt_Precision=models['DecisionTree']['precision'],
    dt_Recall=models['DecisionTree']['recall'],
    dt_F1_Score=models['DecisionTree']['f1'],
    nb_algo='GaussianNB',
    nb_Accuracy=models['NaiveBayes']['accuracy'],
    nb_Precision=models['NaiveBayes']['precision'],
    nb_Recall=models['NaiveBayes']['recall'],
    nb_F1_Score=models['NaiveBayes']['f1'],
    lr_algo='LogisticRegression',
    lr_Accuracy=models['LogisticRegression']['accuracy'],
    lr_Precision=models['LogisticRegression']['precision'],
    lr_Recall=models['LogisticRegression']['recall'],
    lr_F1_Score=models['LogisticRegression']['f1'],
    rf_algo='RandomForestClassifier',
    rf_Accuracy=models['RandomForest']['accuracy'],
    rf_Precision=models['RandomForest']['precision'],
    rf_Recall=models['RandomForest']['recall'],
    rf_F1_Score=models['RandomForest']['f1']
)

print(f"\n✅ Results saved to database (Dataset ID: {data.data_id})")
print(f"✅ All 4 ML models trained successfully on cyber risk data!")
print(f"\nView results at: http://127.0.0.1:8000/admin-algocomp")
