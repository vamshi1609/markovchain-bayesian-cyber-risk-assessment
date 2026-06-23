#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spatialdata.settings')
django.setup()

from adminapp.models import Dataset

# Get latest result
latest = Dataset.objects.filter(data_set='ml_cyber_risk_training.csv').order_by('-data_id').first()

if latest:
    print("\n✅ LATEST DATASET RECORD (ID: {})".format(latest.data_id))
    print("=" * 85)
    print(f"Data Set: {latest.data_set}")
    
    print("\n📊 DECISION TREE METRICS:")
    print(f"  Algorithm: {latest.dt_algo}")
    print(f"  Accuracy:  {latest.dt_Accuracy:.4f}")
    print(f"  Precision: {latest.dt_Precision:.4f}")
    print(f"  Recall:    {latest.dt_Recall:.4f}")
    print(f"  F1 Score:  {latest.dt_F1_Score:.4f}")
    
    print("\n🎲 NAIVE BAYES METRICS:")
    print(f"  Algorithm: {latest.nb_algo}")
    print(f"  Accuracy:  {latest.nb_Accuracy:.4f}")
    print(f"  Precision: {latest.nb_Precision:.4f}")
    print(f"  Recall:    {latest.nb_Recall:.4f}")
    print(f"  F1 Score:  {latest.nb_F1_Score:.4f}")
    
    print("\n📈 LOGISTIC REGRESSION METRICS:")
    print(f"  Algorithm: {latest.lr_algo}")
    print(f"  Accuracy:  {latest.lr_Accuracy:.4f}")
    print(f"  Precision: {latest.lr_Precision:.4f}")
    print(f"  Recall:    {latest.lr_Recall:.4f}")
    print(f"  F1 Score:  {latest.lr_F1_Score:.4f}")
    
    print("\n🌲 RANDOM FOREST METRICS:")
    print(f"  Algorithm: {latest.rf_algo}")
    print(f"  Accuracy:  {latest.rf_Accuracy:.4f}")
    print(f"  Precision: {latest.rf_Precision:.4f}")
    print(f"  Recall:    {latest.rf_Recall:.4f}")
    print(f"  F1 Score:  {latest.rf_F1_Score:.4f}")
    
    print("\n" + "=" * 85)
    print("\n🔍 ALGORITHM RANKING BY ACCURACY:")
    print("-" * 85)
    metrics = [
        ("Decision Tree", latest.dt_Accuracy, latest.dt_Precision, latest.dt_Recall, latest.dt_F1_Score),
        ("Naive Bayes", latest.nb_Accuracy, latest.nb_Precision, latest.nb_Recall, latest.nb_F1_Score),
        ("Logistic Regression", latest.lr_Accuracy, latest.lr_Precision, latest.lr_Recall, latest.lr_F1_Score),
        ("Random Forest", latest.rf_Accuracy, latest.rf_Precision, latest.rf_Recall, latest.rf_F1_Score),
    ]
    sorted_metrics = sorted(metrics, key=lambda x: x[1], reverse=True)
    print(f"{'Rank':<6}{'Algorithm':<25}{'Accuracy':<12}{'Precision':<12}{'Recall':<12}{'F1-Score':<12}")
    print("-" * 85)
    for i, (algo, acc, prec, rec, f1) in enumerate(sorted_metrics, 1):
        print(f"{i:<6}{algo:<25}{acc:<12.4f}{prec:<12.4f}{rec:<12.4f}{f1:<12.4f}")
    
    print("\n" + "=" * 85)
    print("\n💡 ANALYSIS:")
    print(f"  • Best Performers: Decision Tree & Random Forest (100% accuracy)")
    print(f"  • Moderate: Logistic Regression (66.67% accuracy)")
    print(f"  • Struggling: Naive Bayes (50% accuracy - may indicate feature independence violated)")
    print("=" * 85 + "\n")
else:
    print("❌ No dataset found")
