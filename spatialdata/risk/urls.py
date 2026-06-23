from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.risk_dashboard, name="risk_dashboard"),
]
