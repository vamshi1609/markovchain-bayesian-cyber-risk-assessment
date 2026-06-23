from django.shortcuts import render,redirect,get_object_or_404
from mainapp.models import UserModel
from adminapp.models import Dataset
from userapp.models import *
import pandas as pd
# from django.shortcuts import render,redirect
from adminapp.models import *
from mainapp.models import *
from userapp.models import *
from django.contrib import messages
#Importing Libraries
import re
import string
import numpy as np
import pandas as pd
import random
import missingno
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.base import TransformerMixin
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from wordcloud import WordCloud
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score,f1_score, recall_score, precision_score


# Create your views here.
from django.shortcuts import render, redirect
 
# Helper to locate the label/target column in uploaded CSVs. Tries a
# list of common names and falls back to the last column while warning
# the user via Django messages.
def get_label_series(df, request=None):
    candidates = [
        'Spatial_Data', 'Spatial Data', 'spatial_data', 'SpatialData',
        'label', 'target', 'y'
    ]
    for c in candidates:
        if c in df.columns:
            return df[c]
    # fallback to last column
    if request is not None:
        try:
            from django.contrib import messages
            messages.warning(request, f"Label column not found. Using fallback column '{df.columns[-1]}'")
        except Exception:
            pass
    return df[df.columns[-1]]


# Ensure feature and label series have no NaNs; return cleaned X (pd.Series)
# and y (pd.Series). Raises ValueError if no valid rows remain.
def sanitize_training_data(df, feature_col, label_series, request=None):
    if feature_col not in df.columns:
        if request is not None:
            messages.error(request, f"Feature column '{feature_col}' not found in uploaded dataset.")
        raise ValueError(f"Feature column '{feature_col}' not found")

    # Align label_series index with df
    label_series = label_series.reindex(df.index)

    mask = df[feature_col].notna() & label_series.notna()
    if not mask.any():
        if request is not None:
            messages.error(request, "No rows with valid feature and label data found (contains NaN).")
        raise ValueError("No valid training rows after dropping NaNs")

    X_clean = df.loc[mask, feature_col].astype(str)
    y_clean = label_series.loc[mask]
    return X_clean, y_clean


def admin_dash(request):
    dataset=Dataset.objects.all().count()
    user=UserModel.objects.all().count()
    test=SpatialModel.objects.all().count()
    return render(request,'admin/admin-dash.html',{'Dataset':dataset,'user':user,'test':test})


def cyber_risk(request):
    """Redirect to the dedicated risk dashboard in the new `risk` app."""
    return redirect('risk_dashboard')

def admin_algocomp(request):
    try:
        # Get latest dataset with all algorithm results
        data = Dataset.objects.filter(data_set='ml_cyber_risk_training.csv').order_by('-data_id').first()
        
        if not data:
            messages.warning(request, 'Run all 4 algorithms to compare values')
            return redirect('admin_view')
        
        # Extract metrics (convert to percentage)
        dt_ac = (data.dt_Accuracy or 0) * 100
        dt_pr = (data.dt_Precision or 0) * 100
        dt_re = (data.dt_Recall or 0) * 100
        dt_fs = (data.dt_F1_Score or 0) * 100
        
        lr_ac = (data.lr_Accuracy or 0) * 100
        lr_pr = (data.lr_Precision or 0) * 100
        lr_re = (data.lr_Recall or 0) * 100
        lr_fs = (data.lr_F1_Score or 0) * 100
        
        nb_ac = (data.nb_Accuracy or 0) * 100
        nb_pr = (data.nb_Precision or 0) * 100
        nb_re = (data.nb_Recall or 0) * 100
        nb_fs = (data.nb_F1_Score or 0) * 100
        
        rf_ac = (data.rf_Accuracy or 0) * 100
        rf_pr = (data.rf_Precision or 0) * 100
        rf_re = (data.rf_Recall or 0) * 100
        rf_fs = (data.rf_F1_Score or 0) * 100
        
        context = {
            'lr_ac': lr_ac,
            'lr_pr': lr_pr,
            'lr_re': lr_re,
            'lr_fs': lr_fs,
            'nb_ac': nb_ac,
            'nb_pr': nb_pr,
            'nb_re': nb_re,
            'nb_fs': nb_fs,
            'dt_ac': dt_ac,
            'dt_pr': dt_pr,
            'dt_re': dt_re,
            'dt_fs': dt_fs,
            'rf_ac': rf_ac,
            'rf_pr': rf_pr,
            'rf_re': rf_re,
            'rf_fs': rf_fs,
        }
        return render(request, 'admin/admin-algocomp.html', context)
    except Exception as e:
        messages.warning(request, f'Error loading results: {str(e)}')
        return redirect('admin_view')


def admin_allusers(request):
    user=UserModel.objects.filter(user_status='accepted').order_by('user_id')
    return render(request,'admin/admin-allusers.html',{'user':user})
 

def admin_dectree(request):

    data=Dataset.objects.all().order_by('-data_id').first()
    return render(request,'admin/admin-dectree.html',{'data':data})

def admin_lr(request):
    data = Dataset.objects.all().order_by('-data_id').first()
    print(data,type(data),'dataaaaaaaaaaa')

    return render(request,'admin/admin-lr.html',{'data':data})

def admin_nb(request):
    data = Dataset.objects.all().order_by('-data_id').first()
    return render(request,'admin/admin-nb.html',{'data':data})

def admin_pendingusers(request):
    items = UserModel.objects.filter(user_status='pending').order_by('-user_id')
    return render(request,'admin/admin-pendingusers.html' ,{'items':items})

def admin_randfor(request):
    data = Dataset.objects.all().order_by('-data_id').first()
    return render(request,'admin/admin-randfor.html',{'data':data})

def admin_upload(request):
    from risk.models import Asset, Vulnerability, AssetVulnerability, AssetDependency
    import os
    import numpy as np
    
    if request.method == 'POST':
        dataset_file = request.FILES.get('dataset')
        dataset_type = request.POST.get('dataset_type')  # vuln_assets, asset_dependencies, etc.
        
        if not dataset_file:
            messages.error(request, "❌ No file uploaded.")
            return render(request, 'admin/admin-upload.html')
        
        if not dataset_type:
            messages.error(request, "❌ Please select a dataset type.")
            return render(request, 'admin/admin-upload.html')
        
        # Save uploaded file to media directory
        filename = dataset_file.name
        filepath = f'media/{filename}'
        
        try:
            with open(filepath, 'wb+') as destination:
                for chunk in dataset_file.chunks():
                    destination.write(chunk)
        except Exception as e:
            messages.error(request, f"❌ File upload failed: {str(e)}")
            return render(request, 'admin/admin-upload.html')
        
        try:
            df = pd.read_csv(filepath)
            
            # Remove completely empty rows
            df = df.dropna(how='all')
            
            # Process cyber risk datasets
            if dataset_type == 'vuln_assets':
                # Validate required columns
                if 'asset' not in df.columns or 'cve' not in df.columns:
                    messages.error(request, "❌ Required columns missing: 'asset' and 'cve' are required")
                    return render(request, 'admin/admin-upload.html')
                
                success_count = 0
                error_rows = []
                
                for idx, row in df.iterrows():
                    try:
                        asset_name = str(row.get("asset", "")).strip()
                        cve_name = str(row.get("cve", "")).strip()
                        
                        # Skip empty rows
                        if not asset_name or asset_name.lower() == 'nan' or not cve_name or cve_name.lower() == 'nan':
                            continue
                        
                        criticality = row.get("criticality")
                        if pd.isna(criticality):
                            criticality = 5.0
                        else:
                            criticality = float(criticality)
                        
                        # Create or get Asset
                        asset, _ = Asset.objects.get_or_create(
                            name=asset_name,
                            defaults={"criticality": criticality}
                        )
                        
                        epss = row.get("epss_score")
                        if pd.isna(epss):
                            epss = 0.0
                        else:
                            epss = float(epss)
                        
                        # Create or get Vulnerability
                        vuln, _ = Vulnerability.objects.get_or_create(
                            cve=cve_name,
                            defaults={"epss_score": epss}
                        )
                        
                        # Link asset to vulnerability
                        AssetVulnerability.objects.get_or_create(asset=asset, vuln=vuln)
                        success_count += 1
                        
                    except Exception as row_error:
                        error_rows.append(f"Row {idx + 1}: {str(row_error)}")
                
                if success_count > 0:
                    messages.success(request, f"✅ Successfully loaded {success_count} asset-CVE mappings")
                if error_rows:
                    messages.warning(request, f"⚠️ Skipped {len(error_rows)} invalid rows")
                
                return render(request, 'admin/admin-upload.html', {'upload_success': True})
                
            elif dataset_type == 'asset_dependencies':
                # Validate required columns
                if 'source' not in df.columns or 'target' not in df.columns:
                    messages.error(request, "❌ Required columns missing: 'source' and 'target' are required")
                    return render(request, 'admin/admin-upload.html')
                
                success_count = 0
                error_rows = []
                
                for idx, row in df.iterrows():
                    try:
                        source_name = str(row.get("source", "")).strip()
                        target_name = str(row.get("target", "")).strip()
                        
                        # Skip empty rows
                        if not source_name or source_name.lower() == 'nan' or not target_name or target_name.lower() == 'nan':
                            continue
                        
                        # Get or create assets
                        src, _ = Asset.objects.get_or_create(name=source_name)
                        tgt, _ = Asset.objects.get_or_create(name=target_name)
                        
                        weight = row.get("weight")
                        if pd.isna(weight):
                            weight = 1.0
                        else:
                            weight = float(weight)
                        
                        # Create or update dependency
                        AssetDependency.objects.get_or_create(
                            source=src,
                            target=tgt,
                            defaults={"weight": weight}
                        )
                        success_count += 1
                        
                    except Exception as row_error:
                        error_rows.append(f"Row {idx + 1}: {str(row_error)}")
                
                if success_count > 0:
                    messages.success(request, f"✅ Successfully loaded {success_count} asset dependencies")
                if error_rows:
                    messages.warning(request, f"⚠️ Skipped {len(error_rows)} invalid rows")
                    
                return render(request, 'admin/admin-upload.html', {'upload_success': True})
            
            else:
                # ML Training dataset (Cyber Risk)
                if dataset_type == 'ml_training':
                    # Save to media and create dataset record
                    data = Dataset.objects.create(data_set=dataset_file)
                    messages.success(request, f"✅ ML Training dataset uploaded successfully (ID: {data.data_id})")
                    
                    # Automatically train all 4 ML models on this dataset
                    try:
                        df = pd.read_csv(filepath)
                        
                        # Feature columns for cyber risk
                        feature_cols = ['uptime_percent', 'patch_level', 'vulnerabilities_unpatched', 
                                       'response_time_sec', 'attack_frequency_per_week', 
                                       'avg_time_to_compromise_hours', 'daily_risk_score']
                        target_col = 'risk_category'
                        
                        # Check if all columns exist
                        if not all(col in df.columns for col in feature_cols + [target_col]):
                            missing = [c for c in feature_cols + [target_col] if c not in df.columns]
                            messages.warning(request, f"⚠️ Missing columns: {', '.join(missing)}")
                            return render(request, 'admin/admin-upload.html', {'upload_success': True})
                        
                        # Extract X and y
                        X = df[feature_cols].fillna(0)
                        y = df[target_col]
                        
                        # Train-test split
                        from sklearn.model_selection import train_test_split
                        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
                        
                        # 1. Decision Tree
                        from sklearn.tree import DecisionTreeClassifier
                        dt = DecisionTreeClassifier(max_depth=5, random_state=42)
                        dt.fit(X_train, y_train)
                        dt_pred = dt.predict(X_test)
                        dt_acc = accuracy_score(y_test, dt_pred)
                        dt_prec = precision_score(y_test, dt_pred, average='weighted', zero_division=0)
                        dt_rec = recall_score(y_test, dt_pred, average='weighted', zero_division=0)
                        dt_f1 = f1_score(y_test, dt_pred, average='weighted', zero_division=0)
                        
                        # 2. Naive Bayes
                        from sklearn.naive_bayes import GaussianNB
                        nb = GaussianNB()
                        nb.fit(X_train, y_train)
                        nb_pred = nb.predict(X_test)
                        nb_acc = accuracy_score(y_test, nb_pred)
                        nb_prec = precision_score(y_test, nb_pred, average='weighted', zero_division=0)
                        nb_rec = recall_score(y_test, nb_pred, average='weighted', zero_division=0)
                        nb_f1 = f1_score(y_test, nb_pred, average='weighted', zero_division=0)
                        
                        # Scale features for Logistic Regression convergence
                        from sklearn.preprocessing import StandardScaler
                        scaler = StandardScaler()
                        X_train_scaled = scaler.fit_transform(X_train)
                        X_test_scaled = scaler.transform(X_test)
                        
                        # 3. Logistic Regression (with scaled features)
                        from sklearn.linear_model import LogisticRegression
                        lr = LogisticRegression(max_iter=1000, random_state=42, solver='lbfgs')
                        lr.fit(X_train_scaled, y_train)
                        lr_pred = lr.predict(X_test_scaled)
                        lr_acc = accuracy_score(y_test, lr_pred)
                        lr_prec = precision_score(y_test, lr_pred, average='weighted', zero_division=0)
                        lr_rec = recall_score(y_test, lr_pred, average='weighted', zero_division=0)
                        lr_f1 = f1_score(y_test, lr_pred, average='weighted', zero_division=0)
                        
                        # 4. Random Forest
                        from sklearn.ensemble import RandomForestClassifier
                        rf = RandomForestClassifier(n_estimators=10, max_depth=5, random_state=42)
                        rf.fit(X_train, y_train)
                        rf_pred = rf.predict(X_test)
                        rf_acc = accuracy_score(y_test, rf_pred)
                        rf_prec = precision_score(y_test, rf_pred, average='weighted', zero_division=0)
                        rf_rec = recall_score(y_test, rf_pred, average='weighted', zero_division=0)
                        rf_f1 = f1_score(y_test, rf_pred, average='weighted', zero_division=0)
                        
                        # Update dataset record with all metrics
                        data.dt_algo = 'DecisionTreeClassifier'
                        data.dt_Accuracy = dt_acc
                        data.dt_Precision = dt_prec
                        data.dt_Recall = dt_rec
                        data.dt_F1_Score = dt_f1
                        
                        data.nb_algo = 'GaussianNB'
                        data.nb_Accuracy = nb_acc
                        data.nb_Precision = nb_prec
                        data.nb_Recall = nb_rec
                        data.nb_F1_Score = nb_f1
                        
                        data.lr_algo = 'LogisticRegression'
                        data.lr_Accuracy = lr_acc
                        data.lr_Precision = lr_prec
                        data.lr_Recall = lr_rec
                        data.lr_F1_Score = lr_f1
                        
                        data.rf_algo = 'RandomForestClassifier'
                        data.rf_Accuracy = rf_acc
                        data.rf_Precision = rf_prec
                        data.rf_Recall = rf_rec
                        data.rf_F1_Score = rf_f1
                        
                        data.save()
                        
                        messages.success(request, f"✅ All 4 ML models trained successfully! View results at /admin-algocomp")
                        
                    except Exception as train_error:
                        messages.warning(request, f"⚠️ Dataset uploaded but training failed: {str(train_error)}")
                    
                    return render(request, 'admin/admin-upload.html', {'upload_success': True})
                else:
                    # Generic dataset
                    data = Dataset.objects.create(data_set=dataset_file)
                    messages.success(request, f"✅ Dataset uploaded successfully (ID: {data.data_id})")
                    return render(request, 'admin/admin-upload.html', {'upload_success': True})
            
        except pd.errors.ParserError as e:
            messages.error(request, f"❌ CSV parsing error: {str(e)}")
            if os.path.exists(filepath):
                os.remove(filepath)
            return render(request, 'admin/admin-upload.html')
            
        except Exception as e:
            messages.error(request, f"❌ Error processing file: {str(e)}")
            if os.path.exists(filepath):
                os.remove(filepath)
            return render(request, 'admin/admin-upload.html')
    
    return render(request, 'admin/admin-upload.html')

def admin_view(request):
    data = Dataset.objects.all().order_by('-data_id').first()
    print(data,type(data),'sssss')
    file = str(data.data_set)
    df = pd.read_csv(f'./media/{file}')
    table = df.to_html(table_id='data_table')


    return render(request,'admin/admin-view.html',{'i':data,'t':table})

def accept_user(request,id):
    accept = get_object_or_404(UserModel,user_id=id)
    accept.user_status = "accepted"
    accept.save(update_fields=["user_status"])
    accept.save()

    return redirect('admin_pendingusers')

def decline_user(request,id):
    decline = get_object_or_404(UserModel,user_id=id)
    decline.user_status = "declined"
    decline.save(update_fields=["user_status"])
    decline.save()

    return redirect('admin_pendingusers')

def RandomForest(request):
    """Train Random Forest on cyber risk dataset"""
    try:
        # Load cyber risk training dataset
        df = pd.read_csv('dataset/ml_cyber_risk_training.csv')
        
        feature_cols = ['uptime_percent', 'patch_level', 'vulnerabilities_unpatched', 
                       'response_time_sec', 'attack_frequency_per_week', 
                       'avg_time_to_compromise_hours', 'daily_risk_score']
        target_col = 'risk_category'
        
        if not all(col in df.columns for col in feature_cols + [target_col]):
            messages.error(request, "❌ Required columns missing in ml_cyber_risk_training.csv")
            return redirect('admin_dash')
        
        X = df[feature_cols].fillna(0)
        y = df[target_col]
        
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=10, max_depth=5, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        Accuracy = accuracy_score(y_test, y_pred)
        Precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        Recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        F1_Score = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        # Get or create dataset record
        data = Dataset.objects.filter(rf_algo='RandomForestClassifier').order_by('-data_id').first()
        if not data:
            data = Dataset.objects.create(data_set='ml_cyber_risk_training.csv')
        
        data.rf_algo = 'RandomForestClassifier'
        data.rf_Accuracy = Accuracy
        data.rf_Precision = Precision
        data.rf_Recall = Recall
        data.rf_F1_Score = F1_Score
        data.save()
        
        messages.success(request, f"✅ Random Forest trained! Accuracy: {Accuracy:.4f}")
        
        return render(request, 'admin/admin-randfor.html', {'data': data})
        
    except Exception as e:
        messages.error(request, f"❌ Error training Random Forest: {str(e)}")
        return redirect('admin_dash')

def LogisticRegression(request):
    """Train Logistic Regression on cyber risk dataset"""
    try:
        # Load cyber risk training dataset
        df = pd.read_csv('dataset/ml_cyber_risk_training.csv')
        
        feature_cols = ['uptime_percent', 'patch_level', 'vulnerabilities_unpatched', 
                       'response_time_sec', 'attack_frequency_per_week', 
                       'avg_time_to_compromise_hours', 'daily_risk_score']
        target_col = 'risk_category'
        
        if not all(col in df.columns for col in feature_cols + [target_col]):
            messages.error(request, "❌ Required columns missing in ml_cyber_risk_training.csv")
            return redirect('admin_dash')
        
        X = df[feature_cols].fillna(0)
        y = df[target_col]
        
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # Scale features to improve convergence
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        
        from sklearn.linear_model import LogisticRegression as LR
        model = LR(max_iter=1000, random_state=42, solver='lbfgs')
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        Accuracy = accuracy_score(y_test, y_pred)
        Precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        Recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        F1_Score = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        # Get or create dataset record
        data = Dataset.objects.filter(lr_algo='LogisticRegression').order_by('-data_id').first()
        if not data:
            data = Dataset.objects.create(data_set='ml_cyber_risk_training.csv')
        
        data.lr_algo = 'LogisticRegression'
        data.lr_Accuracy = Accuracy
        data.lr_Precision = Precision
        data.lr_Recall = Recall
        data.lr_F1_Score = F1_Score
        data.save()
        
        messages.success(request, f"✅ Logistic Regression trained! Accuracy: {Accuracy:.4f}")
        
        return render(request, 'admin/admin-lr.html', {'data': data})
        
    except Exception as e:
        messages.error(request, f"❌ Error training Logistic Regression: {str(e)}")
        return redirect('admin_dash')

def navie_bayes(request):
    """Train Naive Bayes on cyber risk dataset"""
    try:
        # Load cyber risk training dataset
        df = pd.read_csv('dataset/ml_cyber_risk_training.csv')
        
        feature_cols = ['uptime_percent', 'patch_level', 'vulnerabilities_unpatched', 
                       'response_time_sec', 'attack_frequency_per_week', 
                       'avg_time_to_compromise_hours', 'daily_risk_score']
        target_col = 'risk_category'
        
        if not all(col in df.columns for col in feature_cols + [target_col]):
            messages.error(request, "❌ Required columns missing in ml_cyber_risk_training.csv")
            return redirect('admin_dash')
        
        X = df[feature_cols].fillna(0)
        y = df[target_col]
        
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        from sklearn.naive_bayes import GaussianNB
        model = GaussianNB()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        Accuracy = accuracy_score(y_test, y_pred)
        Precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        Recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        F1_Score = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        # Get or create dataset record
        data = Dataset.objects.filter(nb_algo='GaussianNB').order_by('-data_id').first()
        if not data:
            data = Dataset.objects.create(data_set='ml_cyber_risk_training.csv')
        
        data.nb_algo = 'GaussianNB'
        data.nb_Accuracy = Accuracy
        data.nb_Precision = Precision
        data.nb_Recall = Recall
        data.nb_F1_Score = F1_Score
        data.save()
        
        messages.success(request, f"✅ Naive Bayes trained! Accuracy: {Accuracy:.4f}")
        
        return render(request, 'admin/admin-nb.html', {'data': data})
        
    except Exception as e:
        messages.error(request, f"❌ Error training Naive Bayes: {str(e)}")
        return redirect('admin_dash')

def DecisionTree(request):
    """Train Decision Tree on cyber risk dataset"""
    try:
        # Load cyber risk training dataset
        df = pd.read_csv('dataset/ml_cyber_risk_training.csv')
        
        feature_cols = ['uptime_percent', 'patch_level', 'vulnerabilities_unpatched', 
                       'response_time_sec', 'attack_frequency_per_week', 
                       'avg_time_to_compromise_hours', 'daily_risk_score']
        target_col = 'risk_category'
        
        if not all(col in df.columns for col in feature_cols + [target_col]):
            messages.error(request, "❌ Required columns missing in ml_cyber_risk_training.csv")
            return redirect('admin_dash')
        
        X = df[feature_cols].fillna(0)
        y = df[target_col]
        
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        from sklearn.tree import DecisionTreeClassifier
        model = DecisionTreeClassifier(max_depth=5, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        Accuracy = accuracy_score(y_test, y_pred)
        Precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        Recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        F1_Score = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        # Get or create dataset record
        data = Dataset.objects.filter(dt_algo='DecisionTreeClassifier').order_by('-data_id').first()
        if not data:
            data = Dataset.objects.create(data_set='ml_cyber_risk_training.csv')
        
        data.dt_algo = 'DecisionTreeClassifier'
        data.dt_Accuracy = Accuracy
        data.dt_Precision = Precision
        data.dt_Recall = Recall
        data.dt_F1_Score = F1_Score
        data.save()
        
        messages.success(request, f"✅ Decision Tree trained! Accuracy: {Accuracy:.4f}")
        
        return render(request, 'admin/admin-dectree.html', {'data': data})
        
    except Exception as e:
        messages.error(request, f"❌ Error training Decision Tree: {str(e)}")
        return redirect('admin_dash')
   


def button(request,id):
    predict=SpatialModel.objects.get(pk=id)
    print(predict,'ooooooooooooo')
    X_test=[predict.UEI + predict.start_date + predict.end_date + predict.duration + predict.main_cause +
             predict.location + predict.latitude + predict. longitude + predict.saverity +
             predict.Area_Affected + predict.event_source]
    print(X_test)
    import joblib
    file=open('job_vc_rf.pkl','rb')
    vc=joblib.load(file)
    X_test1=vc.transform(X_test)
    print(X_test1,'gggggggggggggggggggggggg')
    import joblib
    file=open('job_rf.pkl','rb')
    rfmodel=joblib.load(file)
    from sklearn.svm import SVC
    y_pred=rfmodel.predict(X_test1)
    print(y_pred[0])
    return redirect('user_result',id=id)


# ============================================
# Cyber Risk ML Training Functions (NEW)
# ============================================

def train_cyber_risk_models(request):
    """Train all 4 ML models on cyber risk data and display results."""
    try:
        # Load the cyber risk training dataset
        df = pd.read_csv('dataset/ml_cyber_risk_training.csv')
        
        if df.empty:
            messages.error(request, "❌ Cyber risk training dataset is empty")
            return redirect('admin_dash')
        
        # Feature columns (numeric)
        feature_cols = ['uptime_percent', 'patch_level', 'vulnerabilities_unpatched', 
                       'response_time_sec', 'attack_frequency_per_week', 
                       'avg_time_to_compromise_hours', 'daily_risk_score']
        
        # Target variable
        target_col = 'risk_category'
        
        if target_col not in df.columns:
            messages.error(request, f"❌ Target column '{target_col}' not found in dataset")
            return redirect('admin_dash')
        
        # Extract features and target
        X = df[feature_cols].fillna(0)
        y = df[target_col]
        
        if X.empty or y.empty:
            messages.error(request, "❌ Invalid training data")
            return redirect('admin_dash')
        
        # Train-test split
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        results = {}
        
        # 1. Decision Tree
        from sklearn.tree import DecisionTreeClassifier
        dt_model = DecisionTreeClassifier(max_depth=5, random_state=42)
        dt_model.fit(X_train, y_train)
        dt_pred = dt_model.predict(X_test)
        results['DecisionTree'] = {
            'accuracy': accuracy_score(y_test, dt_pred),
            'precision': precision_score(y_test, dt_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, dt_pred, average='weighted', zero_division=0),
            'f1': f1_score(y_test, dt_pred, average='weighted', zero_division=0)
        }
        
        # 2. Naive Bayes (use GaussianNB for numeric features)
        from sklearn.naive_bayes import GaussianNB
        nb_model = GaussianNB()
        nb_model.fit(X_train, y_train)
        nb_pred = nb_model.predict(X_test)
        results['NaiveBayes'] = {
            'accuracy': accuracy_score(y_test, nb_pred),
            'precision': precision_score(y_test, nb_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, nb_pred, average='weighted', zero_division=0),
            'f1': f1_score(y_test, nb_pred, average='weighted', zero_division=0)
        }
        
        # 3. Logistic Regression
        from sklearn.linear_model import LogisticRegression
        lr_model = LogisticRegression(max_iter=200, random_state=42)
        lr_model.fit(X_train, y_train)
        lr_pred = lr_model.predict(X_test)
        results['LogisticRegression'] = {
            'accuracy': accuracy_score(y_test, lr_pred),
            'precision': precision_score(y_test, lr_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, lr_pred, average='weighted', zero_division=0),
            'f1': f1_score(y_test, lr_pred, average='weighted', zero_division=0)
        }
        
        # 4. Random Forest
        from sklearn.ensemble import RandomForestClassifier
        rf_model = RandomForestClassifier(n_estimators=10, max_depth=5, random_state=42)
        rf_model.fit(X_train, y_train)
        rf_pred = rf_model.predict(X_test)
        results['RandomForest'] = {
            'accuracy': accuracy_score(y_test, rf_pred),
            'precision': precision_score(y_test, rf_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, rf_pred, average='weighted', zero_division=0),
            'f1': f1_score(y_test, rf_pred, average='weighted', zero_division=0)
        }
        
        # Store results in database for persistent retrieval
        data = Dataset.objects.create(
            data_set='ml_cyber_risk_training.csv',
            dt_algo='DecisionTreeClassifier',
            dt_Accuracy=results['DecisionTree']['accuracy'],
            dt_Precision=results['DecisionTree']['precision'],
            dt_Recall=results['DecisionTree']['recall'],
            dt_F1_Score=results['DecisionTree']['f1'],
            navie_bayes_algo='GaussianNB',
            navie_bayes_Accuracy=results['NaiveBayes']['accuracy'],
            navie_bayes_Precision=results['NaiveBayes']['precision'],
            navie_bayes_Recall=results['NaiveBayes']['recall'],
            navie_bayes_F1_Score=results['NaiveBayes']['f1'],
            lr_algo='LogisticRegression',
            lr_Accuracy=results['LogisticRegression']['accuracy'],
            lr_Precision=results['LogisticRegression']['precision'],
            lr_Recall=results['LogisticRegression']['recall'],
            lr_F1_Score=results['LogisticRegression']['f1'],
            rf_algo='RandomForestClassifier',
            rf_Accuracy=results['RandomForest']['accuracy'],
            rf_Precision=results['RandomForest']['precision'],
            rf_Recall=results['RandomForest']['recall'],
            rf_F1_Score=results['RandomForest']['f1']
        )
        
        messages.success(request, "✅ All 4 ML models trained successfully on cyber risk dataset!")
        
        # Prepare context with results
        context = {
            'data': data,
            'results': results,
            'is_cyber_risk': True
        }
        
        return render(request, 'admin/admin-algocomp.html', context)
        
    except Exception as e:
        messages.error(request, f"❌ Error training models: {str(e)}")
        import traceback
        traceback.print_exc()
        return redirect('admin_dash')
    





