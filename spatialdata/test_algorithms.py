#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spatialdata.settings')
django.setup()

from adminapp.models import Dataset
from django.test import RequestFactory
from adminapp.views import DecisionTree, navie_bayes, LogisticRegression, RandomForest

factory = RequestFactory()

print("\n🧪 Testing all 4 algorithm functions individually...\n")

# Test DecisionTree
print("1️⃣ Testing DecisionTree()...")
try:
    request = factory.get('/admin-dectree')
    response = DecisionTree(request)
    print("   ✅ DecisionTree executed successfully")
except Exception as e:
    print(f"   ❌ DecisionTree ERROR: {str(e)}")

# Test Naive Bayes
print("\n2️⃣ Testing navie_bayes()...")
try:
    request = factory.get('/admin-nb')
    response = navie_bayes(request)
    print("   ✅ Naive Bayes executed successfully")
except Exception as e:
    print(f"   ❌ Naive Bayes ERROR: {str(e)}")

# Test Logistic Regression
print("\n3️⃣ Testing LogisticRegression()...")
try:
    request = factory.get('/admin-lr')
    response = LogisticRegression(request)
    print("   ✅ Logistic Regression executed successfully")
except Exception as e:
    print(f"   ❌ Logistic Regression ERROR: {str(e)}")

# Test Random Forest
print("\n4️⃣ Testing RandomForest()...")
try:
    request = factory.get('/admin-randfor')
    response = RandomForest(request)
    print("   ✅ Random Forest executed successfully")
except Exception as e:
    print(f"   ❌ Random Forest ERROR: {str(e)}")

print("\n" + "="*70)
print("✅ All algorithm functions tested!")
print("="*70 + "\n")
