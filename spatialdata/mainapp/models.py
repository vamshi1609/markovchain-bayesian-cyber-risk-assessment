from django.db import models

# Create your models here.
class UserModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_username = models.CharField(max_length=100)
    user_dob=models.DateField(max_length=20,null=True)
    user_email = models.EmailField(max_length=100)
    user_password = models.CharField(max_length=100)
    user_contact = models.CharField(max_length=15)
    user_occupation=models.TextField(null=True)
    user_image = models.ImageField(upload_to='user/images')
    user_status=models.CharField(help_text='user_status',max_length=50,null=True,default='pending')

 
    class Meta:
        db_table = 'User_Details'
