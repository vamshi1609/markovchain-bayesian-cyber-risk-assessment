from django.db import models
from mainapp.models import *

# Create your models here.
class SpatialModel(models.Model):
    
    sp_id = models.AutoField(primary_key=True)
    user_url = models.ForeignKey(UserModel,null=True, on_delete=models.CASCADE,related_name='user_url')
    UEI = models.TextField()
    start_date=models.TextField()
    end_date=models.TextField()
    duration=models.TextField()
    main_cause=models.TextField()
    location=models.TextField()
    districts=models.TextField()
    state=models.TextField()
    latitude=models.TextField()
    longitude=models.TextField()
    saverity=models.TextField()
    Area_Affected=models.TextField()
    Human_fatality=models.TextField()
    event_source=models.TextField()
    event_id=models.TextField()
    class Meta:
        db_table = 'spatial_Details'

class PredictModel(models.Model):
    
    sp_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserModel,null=True, on_delete=models.CASCADE,related_name='user_url_id')
    UEI = models.TextField()
    start_date=models.TextField()
    end_date=models.TextField()
    duration=models.TextField()
    main_cause=models.TextField()
    location=models.TextField()
    districts=models.TextField()
    state=models.TextField()
    latitude=models.TextField()
    longitude=models.TextField()
    saverity=models.TextField()
    Area_Affected=models.TextField()
    Human_fatality=models.TextField()
    event_source=models.TextField()
    event_id=models.TextField()


    class Meta:
        db_table = 'predict_Details'
