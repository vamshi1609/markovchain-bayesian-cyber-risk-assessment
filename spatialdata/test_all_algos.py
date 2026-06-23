import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spatialdata.settings')
django.setup()

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("\n" + "="*70)
print("🧪 TESTING ALL 4 ALGORITHMS IN SEQUENCE")
print("="*70)

try:
    df = pd.read_csv('dataset/ml_cyber_risk_training.csv')
    print(f"✅ CSV loaded: {df.shape}")
    
    feature_cols = ['uptime_percent', 'patch_level', 'vulnerabilities_unpatched', 
                   'response_time_sec', 'attack_frequency_per_week', 
                   'avg_time_to_compromise_hours', 'daily_risk_score']
    X = df[feature_cols].fillna(0)
    y = df['risk_category']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    print(f"✅ Data split: train={X_train.shape}, test={X_test.shape}")
    
    # Scale features for algorithms that benefit from it
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("\n" + "-"*70)
    print("1. Decision Tree")
    print("-"*70)
    dt = DecisionTreeClassifier(max_depth=5, random_state=42)
    dt.fit(X_train, y_train)
    dt_acc = accuracy_score(y_test, dt.predict(X_test))
    print(f"✅ Trained successfully - Accuracy: {dt_acc:.4f}")
    
    print("\n" + "-"*70)
    print("2. Naive Bayes (Gaussian)")
    print("-"*70)
    nb = GaussianNB()
    nb.fit(X_train, y_train)
    nb_acc = accuracy_score(y_test, nb.predict(X_test))
    print(f"✅ Trained successfully - Accuracy: {nb_acc:.4f}")
    
    print("\n" + "-"*70)
    print("3. Logistic Regression")
    print("-"*70)
    lr = LogisticRegression(max_iter=1000, random_state=42, solver='lbfgs')
    lr.fit(X_train_scaled, y_train)
    lr_acc = accuracy_score(y_test, lr.predict(X_test_scaled))
    print(f"✅ Trained successfully - Accuracy: {lr_acc:.4f}")
    
    print("\n" + "-"*70)
    print("4. Random Forest")
    print("-"*70)
    rf = RandomForestClassifier(n_estimators=10, max_depth=5, random_state=42)
    rf.fit(X_train, y_train)
    rf_acc = accuracy_score(y_test, rf.predict(X_test))
    print(f"✅ Trained successfully - Accuracy: {rf_acc:.4f}")
    
    print("\n" + "="*70)
    print("✅ ALL 4 ALGORITHMS WORKING WITHOUT ERRORS!")
    print("="*70 + "\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
