from django.shortcuts import render,redirect
from django.contrib import messages
from userapp.models import *
from mainapp.models import *
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Create your views here.
def user_dashboard(request):
    return render(request,'user/user-dashboard.html')


def user_predict(request):
    user_id = request.session['user_id']
    user = UserModel.objects.get(user_id=user_id)

    if request.method == 'POST':
       # Get cyber risk features from form
       asset_name = request.POST.get("asset_name")
       uptime_percent = float(request.POST.get("uptime_percent", 0))
       patch_level = float(request.POST.get("patch_level", 0))
       vulnerabilities_unpatched = float(request.POST.get("vulnerabilities_unpatched", 0))
       response_time_sec = float(request.POST.get("response_time_sec", 0))
       attack_frequency_per_week = float(request.POST.get("attack_frequency_per_week", 0))
       avg_time_to_compromise_hours = float(request.POST.get("avg_time_to_compromise_hours", 0))
       daily_risk_score = float(request.POST.get("daily_risk_score", 0))
       
       try:
           # Load trained models and data
           df = pd.read_csv('dataset/ml_cyber_risk_training.csv')
           
           feature_cols = ['uptime_percent', 'patch_level', 'vulnerabilities_unpatched', 
                          'response_time_sec', 'attack_frequency_per_week', 
                          'avg_time_to_compromise_hours', 'daily_risk_score']
           
           # Prepare input features
           X = df[feature_cols].fillna(0)
           y = df['risk_category']
           X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
           
           # Scale features
           scaler = StandardScaler()
           X_train_scaled = scaler.fit_transform(X_train)
           
           # Create input array
           input_features = np.array([[uptime_percent, patch_level, vulnerabilities_unpatched,
                                      response_time_sec, attack_frequency_per_week,
                                      avg_time_to_compromise_hours, daily_risk_score]])
           
           # Scale input
           input_scaled = scaler.transform(input_features)
           
           # Train all 4 models and get predictions
           dt = DecisionTreeClassifier(max_depth=5, random_state=42)
           dt.fit(X_train, y_train)
           dt_pred = dt.predict(input_features)[0]
           dt_prob = max(dt.predict_proba(input_features)[0]) * 100
           
           nb = GaussianNB()
           nb.fit(X_train, y_train)
           nb_pred = nb.predict(input_features)[0]
           nb_prob = max(nb.predict_proba(input_features)[0]) * 100
           
           lr = LogisticRegression(max_iter=1000, random_state=42, solver='lbfgs')
           lr.fit(X_train_scaled, y_train)
           lr_pred = lr.predict(input_scaled)[0]
           lr_prob = max(lr.predict_proba(input_scaled)[0]) * 100
           
           rf = RandomForestClassifier(n_estimators=10, max_depth=5, random_state=42)
           rf.fit(X_train, y_train)
           rf_pred = rf.predict(input_features)[0]
           rf_prob = max(rf.predict_proba(input_features)[0]) * 100
           
           # Store predictions in session
           prediction_data = {
               'asset_name': asset_name,
               'uptime_percent': uptime_percent,
               'patch_level': patch_level,
               'vulnerabilities_unpatched': vulnerabilities_unpatched,
               'response_time_sec': response_time_sec,
               'attack_frequency_per_week': attack_frequency_per_week,
               'avg_time_to_compromise_hours': avg_time_to_compromise_hours,
               'daily_risk_score': daily_risk_score,
               'dt_pred': dt_pred,
               'dt_prob': round(dt_prob, 2),
               'nb_pred': nb_pred,
               'nb_prob': round(nb_prob, 2),
               'lr_pred': lr_pred,
               'lr_prob': round(lr_prob, 2),
               'rf_pred': rf_pred,
               'rf_prob': round(rf_prob, 2),
           }
           
           request.session['prediction_data'] = prediction_data
           messages.success(request, 'Cyber risk prediction completed successfully')
           return redirect('user_result')
           
       except Exception as e:
           messages.error(request, f'Error during prediction: {str(e)}')
           return redirect('user_predict')

    return render(request,'user/user-predict.html')


def user_profile(req):
    user_id = req.session['user_id']
    user = UserModel.objects.get(user_id=user_id)
    if req.method == 'POST':
            username = req.POST.get("user_username")
            email = req.POST.get("user_email")
            contact = req.POST.get("user_contact")
            password = req.POST.get("user_password")
            if len(req.FILES) != 0:
                        image = req.FILES["image"]
                        user.user_username = username
                        user.user_contact = contact
                        user.user_password = password
                        user.user_image = image
                        user.save()
                        messages.success(req,'Updated Successfully')
            else:
                        user.user_username = username
                        
                        user.user_contact = contact
                        user.user_username = username
                        user.user_contact = contact
                        user.user_password = password
                        user.save()
                        messages.success(req,'Updated Successfully')
            
                        
            return redirect('user_profile')
    return render(req,'user/user-profile.html',{'user':user})


def user_result(request, id=None):
    user_id = request.session.get('user_id')
    
    # Get prediction data from session (for cyber risk predictions)
    prediction_data = request.session.get('prediction_data')
    
    if prediction_data:
        # Display cyber risk prediction results
        context = prediction_data
        messages.success(request, 'Cyber Risk Assessment Complete')
        return render(request, 'user/user-result.html', context)
    
    # Legacy flood prediction handling (fallback)
    try:
        user = UserModel.objects.get(user_id=user_id)
        predict = SpatialModel.objects.get(pk=id)
        
        X_test = [predict.UEI + predict.start_date + predict.end_date + predict.duration + predict.main_cause +
                  predict.location + predict.districts + predict.state + predict.latitude + predict.longitude + predict.saverity +
                  predict.Area_Affected + predict.Human_fatality + predict.event_source + predict.event_id]
        
        import joblib
        file = open('job_vc_rf.pkl', 'rb')
        vc = joblib.load(file)
        X_test1 = vc.transform(X_test)
        
        file = open('job_rf.pkl', 'rb')
        rfmodel = joblib.load(file)
        y_pred = rfmodel.predict(X_test1)
        
        predict.job_status = y_pred[0]
        predict.save()
        
        messages.success(request, 'Predicted Successfully')
        return render(request, 'user/user-result.html', {'job': predict})
    
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('user_predict')