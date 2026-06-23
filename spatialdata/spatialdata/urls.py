"""fakejobdetectionproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from adminapp import views as adminapp_views
from userapp import views as userapp_views
from mainapp import views as mainapp_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-dash',adminapp_views.admin_dash,name='admin_dash'),
    path('admin-cyber-risk', adminapp_views.cyber_risk, name='admin_cyber_risk'),
    path('admin-algocomp',adminapp_views.admin_algocomp,name='admin_algocomp'),
    path('admin-allusers',adminapp_views.admin_allusers,name='admin_allusers'),
    path('admin-dectree',adminapp_views.admin_dectree,name='admin_dectree'),
    path('admin-lr',adminapp_views.admin_lr,name='admin_lr'),
    path('admin-nb',adminapp_views.admin_nb,name='admin_nb'),
    path('admin-pendingusers',adminapp_views.admin_pendingusers,name='admin_pendingusers'),

    path('admin-randfor',adminapp_views.admin_randfor,name='admin_randfor'),
    # path('admin-svm',adminapp_views.admin_svm,name='admin_svm'),
    path('admin-upload',adminapp_views.admin_upload,name='admin_upload'),
    path('admin-view',adminapp_views.admin_view,name='admin_view'),
    path('accepted-user/<int:id>/',adminapp_views.accept_user,name="accepted-user"),
    path('declined-user/<int:id>/',adminapp_views.decline_user,name="declined-user"),
    path('LogisticRegression',adminapp_views.LogisticRegression,name='LogisticRegression'),
   
    path('RandomForest',adminapp_views.RandomForest,name='RandomForest'),
    path('DecisionTree',adminapp_views.DecisionTree,name='DecisionTree'),
    path('navie_bayes',adminapp_views.navie_bayes,name='navie_bayes'),
    path('train-cyber-risk', adminapp_views.train_cyber_risk_models, name='train_cyber_risk'),
    path('button/<int:id>',adminapp_views.button,name='button'),
    # risk dashboard
    path('risk/', include('risk.urls')),
 




    path('',mainapp_views.main_home,name='main_home'),
    path('main-about',mainapp_views.main_about,name='main_about'),
    path('main-adminlogin',mainapp_views.main_adminlogin,name='main_adminlogin'),
    path('main-user-login',mainapp_views.main_user_login,name='main_user_login'),
    path('main-user-register',mainapp_views.main_user_register,name='main_user_register'),
    path('main-contact',mainapp_views.main_contact,name='main_contact'),

    path('user-dashboard',userapp_views.user_dashboard,name='user_dashboard'),
    path('user-predict',userapp_views.user_predict,name='user_predict'),
    path('user-profile',userapp_views.user_profile,name='user_profile'),
    # Allow both session-based result (no id) and legacy id-based result
    path('user-result', userapp_views.user_result, name='user_result'),
    path('user-result/<int:id>',userapp_views.user_result,name='user_result'),



    ]+ static (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
