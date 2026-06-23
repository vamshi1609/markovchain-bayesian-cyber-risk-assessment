from django.db import models

# Create your models here.
class Dataset(models.Model):
    data_id = models.AutoField(primary_key=True)
    data_set = models.FileField(upload_to='files/')
    dt_Accuracy = models.FloatField(null=True)
    dt_Precision = models.FloatField(null=True)
    dt_Recall = models.FloatField(null=True)
    dt_F1_Score = models.FloatField(null=True)
    dt_algo = models.CharField(max_length=50,default='DecisionTreeClassifier',null=True)
    
    nb_Accuracy = models.FloatField(null=True)
    nb_Precision = models.FloatField(null=True)
    nb_Recall = models.FloatField(null=True)
    nb_F1_Score = models.FloatField(null=True)
    nb_algo = models.CharField(max_length=50,default='Naive-Bayes',null=True)
    
    lr_Accuracy = models.FloatField(null=True)
    lr_Precision = models.FloatField(null=True)
    lr_Recall = models.FloatField(null=True)
    lr_F1_Score = models.FloatField(null=True)
    lr_algo = models.CharField(max_length=50,default='Logistic Regression',null=True)
    
    rf_Accuracy = models.FloatField(null=True)
    rf_Precision = models.FloatField(null=True)
    rf_Recall = models.FloatField(null=True)
    rf_F1_Score = models.FloatField(null=True)
    rf_algo = models.CharField(max_length=50,default='RandomForestClassifier',null=True)
    
    class Meta:
        db_table = 'dataset'
